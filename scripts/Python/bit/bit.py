"""A CLI for managing Git worktrees with GitHub and tmux integration."""

import argparse
import datetime
import os
import tempfile
from functools import wraps
from pathlib import Path
from typing import Callable, List, Optional
from urllib.parse import urlparse

import libtmux
import questionary
import tomllib
from git import GitCommandError, Repo
from github import Github
from github.NamedUser import NamedUser
from github.Organization import Organization
from logzero import LogFormatter, logger, setup_logger
from rich.text import Text


_VERSION = "0.1.0"


def require_git_repo(func: Callable) -> Callable:
    """Decorator to ensure the function is run inside a Git repository."""

    @wraps(func)
    def wrapper(*args: object, **kwargs: object) -> object:
        try:
            repo_path = Path(
                Repo(Path.cwd(), search_parent_directories=True).git.rev_parse("--show-toplevel")
            )
            return func(*args, repo_path=repo_path, **kwargs)
        except GitCommandError:
            logger.error("Must be in a Git repository")

    return wrapper


def open_in_tmux(path: Path) -> None:
    """Open the given path in a new tmux window within the current session."""

    if not os.getenv("TMUX"):
        return

    server = libtmux.Server()
    this_session = Path(os.getenv("TMUX")).name.split(",")[-1]
    session = next(s for s in server.sessions if s.id == f"${this_session}")

    repo = Repo(path)
    url = urlparse(repo.remotes.origin.url).path
    name = Path(url).stem
    window_name = f"{name} ({repo.active_branch.name})"

    window = session.new_window(start_directory=str(path), window_name=window_name, attach=True)
    window.select_window()


@require_git_repo
def worktree_list(filter_str: str = "", repo_path: Path = None) -> List[Path]:
    """Return a list of worktree paths matching an optional filter string."""

    repo = Repo(repo_path)
    output = repo.git.worktree("list", "--porcelain")
    worktrees = [
        path
        for line in output.splitlines()
        if line.startswith("worktree ")
        and (path := Path(line.split()[1])) != repo_path
        and filter_str in str(path)
    ]
    return worktrees


@require_git_repo
def list_worktrees(repo_path: Path = None) -> None:
    """Print all worktree paths and a summary of their dirty state using rich."""

    if not (paths := worktree_list()):
        logger.error("No worktrees found.")
        return

    logger.info("Worktrees:", style="bold underline")
    for path in paths:
        repo = Repo(path)
        branch = repo.active_branch.name if not repo.head.is_detached else "detached HEAD"

        modified = len(repo.index.diff(None))
        staged = len(repo.index.diff("HEAD"))
        untracked = len(repo.untracked_files)

        if modified == 0 and staged == 0 and untracked == 0:
            status_summary = Text("[clean]", style="green")
        else:
            parts = []
            if staged:
                parts.append(f"S:{staged}")
            if modified:
                parts.append(f"M:{modified}")
            if untracked:
                parts.append(f"??:{untracked}")
            status_summary = Text("[" + " ".join(parts) + "]", style="yellow")

        line = Text(f"- {path} ")
        line.append(f"({branch})", style="cyan")
        line.append(" ")
        line.append(status_summary)
        print(line)


@require_git_repo
def delete_worktree(branch_name: str, repo_path: Path = None) -> None:
    """Delete the worktree and branch associated with the given branch name."""

    for path in worktree_list(branch_name):
        try:
            Repo(repo_path).git.worktree("remove", "--force", str(path))
            Repo(repo_path).git.branch("--delete", "--force", path.name)
        except GitCommandError as exc:
            logger.error(f"Error removing worktree: {exc}")


@require_git_repo
def create_branch(branch_name: Optional[str] = None, repo_path: Path = None) -> None:
    """Create a new branch and associated worktree. Auto-generates a name if not provided."""

    if not branch_name:
        now = datetime.datetime.now()
        branch_name = now.strftime("%Y-%b-%d-%H%M") + f"-{repo_path.name}"
    branch_path = repo_path.parent / branch_name
    repo = Repo(repo_path)
    try:
        repo.git.worktree("add", str(branch_path))
        open_in_tmux(branch_path)
    except GitCommandError as exc:
        logger.error(f"Failed to add worktree: {exc}")


@require_git_repo
def stash_changes(exclude_untracked: bool = False, repo_path: Path = None) -> None:
    """Stash tracked (and optionally untracked) changes across worktrees."""

    repo = Repo(repo_path)
    cmd = ["stash", "push"]
    if not exclude_untracked:
        cmd.append("--include-untracked")

    try:
        repo.git.execute(
            [
                "git",
                "--git-dir",
                repo.git.rev_parse("--git-common-dir"),
                "--work-tree",
                str(repo_path),
            ]
            + cmd
        )
    except GitCommandError as exc:
        logger.error(f"Error stashing changes: {exc}")


@require_git_repo
def commit_wip(repo_path: Path = None) -> None:
    """Stage all changes, commit as 'Work-In-Progress', and push to remote."""

    repo = Repo(repo_path)
    repo.git.add("--all")
    try:
        repo.git.commit("-m", "Work-In-Progress")
        repo.git.push()
    except GitCommandError as exc:
        logger.error(f"Error committing or pushing: {exc}")


@require_git_repo
def interactive_pull_remote_branch(repo_path: Path = None) -> None:
    """Interactively select and pull a remote branch into a new worktree."""

    repo = Repo(repo_path)
    repo.remotes.origin.fetch(prune=True)

    heads = [
        ref.name.split("origin/")[-1]
        for ref in repo.remotes.origin.refs
        if ref.name.startswith("origin/")
    ]
    branch_name = questionary.select("Select remote branch to pull:", choices=heads).ask()
    if not branch_name:
        return

    branch_path = repo_path.parent / branch_name
    try:
        repo.git.worktree("add", str(branch_path), f"origin/{branch_name}")
        with repo.git.custom_environment(GIT_WORK_TREE=str(branch_path)):
            repo.git.checkout("-b", branch_name, f"origin/{branch_name}")
            repo.git.branch("--set-upstream-to", f"origin/{branch_name}", branch_name)
            repo.git.pull()
            repo.git.reset("--hard", f"origin/{branch_name}")
        open_in_tmux(branch_path)
    except GitCommandError as exc:
        print(f"Error pulling remote branch: {exc}")


def interactive_switch_worktree() -> None:
    """Present a list of available worktrees and open the selected ones in tmux."""

    paths = worktree_list()
    if not paths:
        logger.error("No worktrees available to switch to.")
        return

    selected = questionary.checkbox(
        "Select worktrees to switch to:", choices=[str(p) for p in paths]
    ).ask()

    if not selected:
        return

    for path_str in selected:
        if (path := Path(path_str)).exists():
            open_in_tmux(path)
        else:
            logger.error(f"Path does not exist: {path}")


def interactive_github_clone(token: str, base_dir: Path) -> None:
    """
    Interactively clone a GitHub repository using the provided token and open the cloned worktree
    in tmux. Prompts the user to select an org/user, then a repo, and optionally a branch name.
    """

    def select_organization(github: Github) -> Optional[str]:
        user = github.get_user()
        choices = [org.login for org in user.get_orgs()]
        choices.insert(0, user.login)
        return questionary.select("Select organization or user:", choices=choices).ask()

    def select_repository(
        org: NamedUser | Organization,
    ) -> Optional[str]:
        repos = sorted(org.get_repos(), key=lambda r: r.full_name.lower())
        return questionary.autocomplete(
            "Select repository:",
            choices=[r.full_name for r in repos],
            validate=lambda val: val in [r.full_name for r in repos],
        ).ask()

    gh = Github(token)
    org_name = select_organization(gh)
    if not org_name:
        return

    user = gh.get_user()
    org = gh.get_organization(org_name) if org_name != user.login else user
    repo_name = select_repository(org)
    if not repo_name:
        return

    repo_url = f"git@github.com:{repo_name}.git"
    branch_name = questionary.text("Branch name (leave blank for default):").ask()

    tmpdir = Path(tempfile.mkdtemp())
    target_dir = tmpdir / repo_name.split("/")[-1]

    try:
        Repo.clone_from(repo_url, str(target_dir), branch=branch_name or None, single_branch=True)
    except GitCommandError as err:
        logger.error(f"Failed to clone repository: {err}")
        return

    if not branch_name:
        repo = Repo(target_dir)
        branch_name = repo.active_branch.name

    final_path = base_dir / repo_name.split("/")[-1] / branch_name
    final_path.parent.mkdir(parents=True, exist_ok=True)
    target_dir.rename(final_path)
    open_in_tmux(final_path)


def load_config() -> dict:
    """Load configuration from ~/.config/bit.toml or XDG-compliant path."""

    config_path = Path(os.getenv("XDG_CONFIG_HOME", Path.home() / ".config")) / "bit.toml"

    if not config_path.exists():
        return {}

    with config_path.open("rb") as f:
        return tomllib.load(f)


def main() -> None:
    """
    Entry point for the bit CLI. Handles argument parsing and dispatches subcommands.
    Also integrates config loading from env vars or a TOML config file.
    """

    config = load_config()

    parser = argparse.ArgumentParser(
        prog="bit",
        description=(
            "bit — A CLI for managing Git worktrees with GitHub and tmux integration.\n\n"
            "Configuration precedence for --token and --path (used with 'clone'):\n"
            "  1. CLI arguments\n"
            "  2. Environment variables: BIT_GITHUB_TOKEN, BIT_PROJECTS_PATH\n"
            "  3. Config file: ~/.config/bit/config.toml\n"
            "\nExample config.toml:\n"
            '  token = "ghp_yourgithubtoken"\n'
            '  path = "/home/user/Projects"\n'
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("--debug", "-d", action="store_true", help="Enable debug logging")
    parser.add_argument("--version", "-v", action="store_true", help="Show app version")

    subparsers = parser.add_subparsers(dest="command", required=True, metavar="command")

    branch_parser = subparsers.add_parser("branch", help="Create a new worktree and branch")
    branch_parser.add_argument("--name", "-n", help="Branch name to create")

    delete_parser = subparsers.add_parser("delete", help="Delete a worktree and branch")
    delete_parser.add_argument("--name", "-n", required=True, help="Branch name to delete")

    stash_parser = subparsers.add_parser("stash", help="Stash changes across all worktrees")
    stash_parser.add_argument(
        "--exclude-untracked", "-x", action="store_true", help="Exclude untracked files from stash"
    )

    subparsers.add_parser("wip", help="Add, commit, and push work-in-progress changes")

    clone_parser = subparsers.add_parser("clone", help="Interactively clone a GitHub repository")
    clone_parser.add_argument("--token", help="GitHub personal access token")
    clone_parser.add_argument("--path", help="Target base directory for the cloned repo")

    subparsers.add_parser("pull", help="Pull a remote branch into a new worktree")
    subparsers.add_parser("switch", help="Switch to an existing worktree")
    subparsers.add_parser("list", help="List all existing worktrees")

    args = parser.parse_args()

    if args.version:
        log.info(_VERSION)
        return

    formatter = LogFormatter(fmt="%(levelname)s: %(message)s")
    log_level = 10 if args.debug else 0

    setup_logger(formatter=formatter, level=log_level)

    match args.command:
        case "branch":
            create_branch(args.name)
        case "delete":
            delete_worktree(args.name)
        case "stash":
            stash_changes(exclude_untracked=args.exclude_untracked)
        case "wip":
            commit_wip()
        case "clone":
            token = args.token or os.getenv("BIT_GITHUB_TOKEN") or config.get("token")
            path = (
                args.path
                or os.getenv("BIT_PROJECTS_PATH")
                or config.get("path")
                or str(Path.home() / "Development" / "Projects")
            )
            if not token:
                logger.error(
                    "GitHub token not provided. Use --token, BIT_GITHUB_TOKEN, or config file."
                )
            else:
                interactive_github_clone(token, Path(path))
        case "pull":
            interactive_pull_remote_branch()
        case "switch":
            interactive_switch_worktree()
        case "list":
            list_worktrees()
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
