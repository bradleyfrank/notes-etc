# Git

```sh
# clone by tag
git clone -b <tagname> <repository> .
```

---

```sh
git push --delete <remote_name> <branch_name> # delete remote branch
git branch -d <branch_name> # delete local branch

git branch –m <new_name> # rename local branch
git push origin -u <new_name> # rename remote branch
git push origin --delete <old_name> # delete old branch
```

---

```sh
git diff --staged # diff files already staged
git diff --stat # diff summary 
git diff --check # check for conflicts and whitespace errors
```

---

```sh
git reset --hard [HEAD|<hash>] # forget all the changes, clean start
git reset <hash> # edit, re-stage and re-commit files
git reset --soft <hash> # re-commit past commits, as one big commit
```

---

```sh
git log --full-history -- /path/to/file # search for file changes
git log --all --grep='Build 0051' # search the commit log (across all branches) for the given text
git grep 'Build 0051' $(git rev-list --all) # search the content of commits
```

---

```sh
# clone a repository containing submodules
git clone --recursive <repo>

# load submodules in a previously cloned repo
git submodule update --init
git submodule update --init --recursive # for nested submodules

# download eight submodules at once
git submodule update --init --recursive -j 8
git clone --recursive --jobs 8 <repo>

# pull all changes in submodules
git submodule update --remote

# add a child repository to a parent repository
git submodule add <repo>

# initialize an existing Git submodule
git submodule init

# update the commit of the submodule to the latest commit
git submodule update
```

---

```sh
gh api search/repositories\?q=org:<org>+language:<language>
gh api search/issues\?q=repo:<org>/<repo>+is:pr+is:merged
gh api search/issues\?q=repo:<org>/<repo>+is:pr+is:merged+merged:\>=<YYYY-MM-DD>
gh api search/repositories\?q=org:<org>+language:<language> | jq ' .items | .[] | .name'
gh api -X PATCH /repos/<org>/<repo> -f archived=true
```
