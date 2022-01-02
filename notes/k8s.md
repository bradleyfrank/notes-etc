# Kubernetes

## Managing

```sh
# filtering
kubectl get pods -n <namespace> \
    --selector=app=<app> \
    --no-headers \
    -o=custom-columns=NAME:.metadata.name

# patching
kubectl patch pod <pod> -p '{"metadata":{"finalizers":null}}'

# terminate gracefully, immediately, and forced
kubectl delete --wait=false pod <pod> --grace-period=<seconds>
kubectl delete --grace-period=1 pod <pod>
kubectl delete --grace-period=0 pod <pod> --force=true

# deployments
kubectl create deployment <app> --image=<image> [--dry-run --output=yaml]
kubectl scale --replicas=3 deployment <deployment>
kubectl rollout history deployment <deployment> [--revision=<num>]

# schedule/unschedule
kubectl cordon <node>
kubectl uncordon <node>

# create cronjob
kubectl create job --from=cronjob/<cronjob> <job>

# verify certificate
kubectl get secret <secret> -o json | jq -r '.data."tls.crt"' | base64 --decode | openssl x509 -noout -enddate

# api
kubectl api-resources
kubectl api-versions

kubectl proxy --port=8001
curl http://localhost:8001/api/v1/namespace/default/pods
```

---

## Troubleshooting

```sh
# Is something hogging resources?
$ k top pods --all-namespaces --sort-by=memory
$ k top pods --all-namespaces --sort-by=cpu
$ k top nodes --sort-by=memory
$ k top nodes --sort-by=cpu
```

---

## kubectl

Order of preference:

1. `--kubeconfig`
2. `KUBECONFIG`
3. `$HOME/.kube/config`

```sh
# temporarily stitch kubeconfig files together
export KUBECONFIG=file1:file2
kubectl get pods --context=cluster-1
kubectl get pods --context=cluster-2

# merge kubeconfig files
KUBECONFIG=file1:file2:file3 kubectl config view \
    --merge --flatten > out.txt

# extract specific context config
KUBECONFIG=in.txt kubectl config view \
    --minify --flatten --context=**context-1 > out.txt

# using kubectl without config file
KUBECONFIG= kubectl get nodes \
  --server https://localhost:6443 \
  --user <user> \
  --client-certificate <cert> \
  --client-key <key> \
  --insecure-skip-tls-verify
```

---

## Krew Plugins

```sh
# prints the cleaned kubeconfig to stdout, similar to running: kubectl config view
kubectl config-cleanup

# cleanup and save the result
kubectl config-cleanup --raw > ./kubeconfig-clean.yaml

# cleanup and print the configs that were removed
kubectl config-cleanup --print-removed --raw > ./kubeconfig-removed.yaml

# print only the context names that were removed
kubectl config-cleanup --print-removed -o=jsonpath='{ range.contexts[*] }{ .name }{"\n"}'

# verify the current context against v1.18.6 swagger.json
$ kubepug --k8s-version=v1.18.6

# get all resources
ketall --namespace=default
```
