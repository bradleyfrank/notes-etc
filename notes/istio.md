# Istio

What Envoy version is Istio using?

```sh
kubectl exec -it prometheus-68b46fc8bb-dc965 -c istio-proxy -n istio-system pilot-agent request GET server_info
{
 "version": "12cfbda324320f99e0e39d7c393109fcd824591f/1.14.1/Clean/RELEASE/BoringSSL"
}
```

Ref: [what-envoy-version-is-istio-using](https://istio.io/v1.6/docs/ops/diagnostic-tools/proxy-cmd/#what-envoy-version-is-istio-using)

```sh
stern istio-ingressgateway -n istio-system -e health -e metrics -o json | jq -Sr '.message | fromjson'
```

Renew certs:

```bash
kubectl --context prod-gke -n istio-system rollout restart deploy/istio-ingressgateway
kubectl --context prod-gke -n istio-system rollout restart deploy/istio-ilbgateway
```



