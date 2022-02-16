# Google Cloud

```bash
# [okclean] remove contexts added by infractl
okclean() {
    local context current_context; current_context=$(kubectl config current-context)
    krename; kubectl config unset current-context &> /dev/null
    for context in $(kubectl config get-contexts | awk '(NR>1) {print $1}' | grep -E '^gke'); do
        kubectl config delete-context "$context"
    done
    kubectl config set current-context "$(grep -o '[^_]*$' <<< "$current_context")" &> /dev/null
}
```

---

```bash
# [gps] set the active GCP project
gps() {
    local projects
    projects="$(gcloud projects list | _inline_fzf | awk '{print $1}')"
    gcloud config set project "$projects"
}
```

