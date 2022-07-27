# Shell

```sh
# convert Ansible tags into selectable list
ansible-playbook playbook.yml --list-tags \
  | sed -rn 's/^\s+TASK\sTAGS:\s\[(.*)\]$/\1/p' \
  | sed 's/, /\n/g' \
  | fzf --multi --ansi -i -1 --height=50% --reverse -0 --border \
  | xargs \
  | tr ' ' ','
```

---

```sh
# split a file at REGEX into multiple files
while read -r line; do
  [[ $line =~ REGEX ]] && f=FILENAME
  echo "$line" >> "$f"
done < FILE
```

---

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

---

```sh
# Bash 4+ read file into array
mapfile -t foo < "file"
readarray -t foo < <( find . -name * )

# enter a password securely
read -r -s -p "Enter password: " my_password
```

---

```sh
frames="/ | \\ -"
while :; do
  for f in $frames; do printf "\r%s Loading..." "$f"; sleep 0.5; done
done
```

