# Simple deployment to k8s

## Docs
https://github.com/cloudflare/argo-tunnel-examples/tree/master/named-tunnel-k8s  

Create Secret example:
```bash
cp /Users/cf000197/.cloudflared/ef824aef-7557-4b41-a398-4684585177ad.json /var/snap/microk8s/common/credentials.json
kubectl create secret generic tunnel-credentials --from-file=credentials.json=/var/snap/microk8s/common/credentials.json -n cloudflared
```
Copy over cert as well
```bash
cp /home/prestonb/.cloudflared/cert.pem /var/snap/microk8s/common/cert.pem
kubectl create secret generic cloudflared-cert --from-file=cert.pem=/var/snap/microk8s/common/cert.pem -n cloudflared
```

## k8s
```bash
kubectl apply -f namespace.yaml
kubectl config set-context --current --namespace=personal
```

If using kind push image to kind
```bash
kind load docker-image personal_site:latest  --name kind
```

```bash
kubectl apply -f deployment.yaml
kubectl port-forward svc/personal_site 8000:8000 
kubectl apply -f ingress.yaml
```

