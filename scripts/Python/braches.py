#!/usr/bin/env python3

import argparse
import os
import pygit2

def create_arguments():
    """Create script arguments."""

    arguments = argparse.ArgumentParser(
        description='Branch and worktree wrapper for Git.')

    tmux_open = arguments.add_mutually_exclusive_group(required=True)
    tmux_open.add_argument('-w', '--window', action='store_true',
                           help='open worktree in a new tmux window')
    tmux_open.add_argument('-p', '--pane', action='store_true',
                           help='open worktree in a tmux pane in the same window')

    return arguments

def branches():
    repo_path = pygit2.discover_repository(os.getcwd())
    if repo_path is not None:
        repo = pygit2.Repository(repo_path)

if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    branches()
