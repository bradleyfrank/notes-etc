# Google Cloud

## General

```sh
gcloud projects create $PROJECT_ID \
  --name="$PROJECT_NAME" \
  --set-as-default
```

```sh
gcloud projects describe $(gcloud config list --format 'value(core.project)') --format 'value(name)'
gcloud projects describe $(gcloud config get-value project) --format 'value(name)'
gcloud info --format='value(config.paths.active_config_path)'
gcloud info --format='value(config.paths.sdk_root'
gcloud config configurations list --filter='is_active=True' --format='value(name)'
gcloud config set project "$(gcloud projects list | _inline_fzf | awk '{print $1}')"
```

```sh
while read -r line; do
  base64 --decode <<< $line; printf '\n'
done <<< "$(kubectl --context $CONTEXT get secret $SECRET -n $NAMESPACE -o json \
  | jq -r '.data | with_entries(select(.key|match("DB_";"i")))[]')"
```

```sh
# remove duplicate contexts
current_context=$(kubectl config current-context)
kubectl config unset current-context &> /dev/null
for context in $(kubectl config get-contexts | awk '(NR>1) {print $1}' | grep -E '^gke'); do
    kubectl config delete-context "$context"
done
kubectl config set current-context "$(grep -o '[^_]*$' <<< "$current_context")" &> /dev/null
```

## Service Accounts

```sh
# update the description and the display name
gcloud iam service-accounts update $SERVICE_ACCOUNT --display-name "..." --description "..."

# check the IAM policy for a service account
gcloud iam service-accounts get-iam-policy SERVICE_ACCOUNT

# add a user to the policy
gcloud iam service-accounts add-iam-policy-binding $SERVICE_ACCOUNT --member <email> --role <roles/role>
```

### Access Tokens

The Service Account Token Creator role allows a user to run gcloud commands as a service account by tacking on the `--impersonate-service-account` flag along with the service account email address. The same functionality is extended to gsutil using the `-i` flag instead. Grant the Service Account Token Creator role to the user for the service account to be used:

```sh
gcloud iam service-accounts add-iam-policy-binding SERVICE_ACCOUNT --member MEMBER --role=roles/iam.serviceAccountTokenCreator
```

If you want to access the Google Cloud REST API as a service account using an access token, first get an access token for your own account and stick it in an environment variable:

```sh
export MYTOKEN=$(gcloud auth print-access-token)
```

> **`request.json`**
>
> ```json
> { "delegates": [ ], "scope": [ "https://www.googleapis.com/auth/cloud-platform", ], "lifetime": "3600s" }
> ```

* `delegates` are service accounts that are used to access one another
* `scope` is Oauth 2.0 scope; a full list of APIs and their [corresponding scopes](https://developers.google.com/identity/protocols/oauth2/scopes)
* `lifetime` is how many seconds token is valid for

```sh
curl -X POST \
  https://iamcredentials.googleapis.com/v1/projects/-/serviceAccounts/SERVICE_ACCOUNT@PROJECT_ID.iam.gserviceaccount.com:generateAccessToken \
  -H "Authorization: Bearer $MYTOKEN” \
  -H "Content-Type: application/json; charset=utf-8" \
  -d @request.json
```

The output will be the access token for the service account.
