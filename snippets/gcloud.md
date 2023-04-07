# Google Cloud

```bash
mapfile -t roles_desired <<< "$(jq -r '.service_accounts["image-exporter"][]' "$CONFIG_FILE" \
  | xargs -I{} echo "roles/{}")"
mapfile -t roles_present <<< "$(gcloud projects get-iam-policy "$PROJECT_ID" \
  --flatten="bindings[].members" \
  --filter="bindings.members:image-exporter@${PROJECT_ID}.iam.gserviceaccount.com" \
  --format="value(bindings.role)")"

if ! cmp -s <(echo "${roles_desired[@]}") <(echo "${roles_present[@]}"); then
  echo "The 'image-exporter' service account needs proper roles to continue." >&2
  exit 1
fi
```
