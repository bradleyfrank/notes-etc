# kubectl

```sh
# read secrets
while read -r line; do
  base64 --decode <<< $line; printf '\n'
done <<< "$(kubectl --context $CONTEXT get secret $SECRET -n $NAMESPACE -o json \
  | jq -r '.data | with_entries(select(.key|match("DB_";"i")))[]')"

# remove duplicate contexts
current_context=$(kubectl config current-context)
kubectl config unset current-context &> /dev/null
for context in $(kubectl config get-contexts | awk '(NR>1) {print $1}' | grep -E '^gke'); do
    kubectl config delete-context "$context"
done
kubectl config set current-context "$(grep -o '[^_]*$' <<< "$current_context")" &> /dev/null
```

