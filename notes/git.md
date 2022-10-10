# Git

## Cloning

```sh
# clone by tag
git clone -b <tagname> <repository> .
```

## Logs & Searching

```sh
git log --full-history -- /path/to/file # search for file changes
git log --all --grep='Build 0051' # search the commit log (across all branches) for the given text
git grep 'Build 0051' $(git rev-list --all) # search the content of commits

# find and retrieve a deleted file
file=/path/to/file
git checkout $(git rev-list -n 1 HEAD -- "$file")~1 -- "$file"

# find commiter and show commit
git log --format='%h %ae' | grep {{ email }} | awk '{print $1}' | xargs git show
```

## Branching

```sh
git push --delete <remote_name> <branch_name> # delete remote branch
git branch -d <branch_name> # delete local branch

git branch –m <new_name> # rename local branch
git push origin -u <new_name> # rename remote branch
git push origin --delete <old_name> # delete old branch
```

## Comparing

```sh
git diff --staged # diff files already staged
git diff --stat # diff summary 
git diff --check # check for conflicts and whitespace errors
```

## Fixing

```sh
git reset --hard [HEAD|<hash>] # forget all the changes, clean start
git reset <hash> # edit, re-stage and re-commit files
git reset --soft <hash> # re-commit past commits, as one big commit
```

## Signing

```sh
ssh-keygen -t rsa -b 4096 -C "bfrank@bfrank-demo-01"

git config --global user.name "Brad"
git config --global user.email "bfrank@oreilly.com"
git config --global user.signingkey "$(cat ~/.ssh/id_rsa.pub)"
git config --global commit.gpgsign true
git config --global gpg.format ssh
git config --global gpg.ssh.allowedSignersFile "$HOME/.ssh/allowed_signers"

cat ~/.ssh/id_rsa.pub >> ~/.ssh/allowed_signers

eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa
```

## Submodules

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

## GitHub

### API

```sh
gh api search/repositories\?q=org:<org>+language:<language>
gh api search/issues\?q=repo:<org>/<repo>+is:pr+is:merged
gh api search/issues\?q=repo:<org>/<repo>+is:pr+is:merged+merged:\>=<YYYY-MM-DD>
gh api search/repositories\?q=org:<org>+language:<language> | jq ' .items | .[] | .name'
gh api -X PATCH /repos/<org>/<repo> -f archived=true
```

```sh
# GET GitHub Gist
curl --fail --silent \
  --header "Accept: application/vnd.github.v3+json" \
  --header "Authorization: token <token>" \
  https://api.github.com/gists/<id>

# PATCH GitHub Gist
curl --fail --silent \
  --header "Accept: application/vnd.github.v3+json" \
  --header "Authorization: token <token>" \
  --request PATCH https://api.github.com/gists/<id> \
  --data "{\"files\": { \"filename\": { \"content\": \"...\" }}}"

# POST GitHub Gist
curl --fail --silent \
  --header "Accept: application/vnd.github.v3+json" \
  --header "Authorization: token <token>" \
  --request POST https://api.github.com/gists \
  --data "{\"files\": { \"cmarks\": { \"content\": \"...\" }}}"
```

### Docker Registry

```sh
# authenticating
cat ~/.github_token | docker login docker.pkg.github.com -u <username> --password-stdin
```
