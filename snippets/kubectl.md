# kubectl

```bash
# [kcxt] interactive kubectl context select
alias -g kcxt='--context $(_kc_helper)'
_kc_helper() { printf "%s" "$(kubectl config get-contexts | tr -d '\*' | tail -n+2 | awk '{print $1}' | fzf)"; }
```

---

```bash
# rename all contexts with shorter names
krename() {
    local context
    kubectl config unset current-context &> /dev/null
    for context in $(kubectl config get-contexts | awk '(NR>1) {print $1}'); do
        kubectl config rename-context "$context" "$(grep -o '[^_]*$' <<< "$context")" 2> /dev/null
    done
}
```
