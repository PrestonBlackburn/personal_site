# Simple deployment to k8s


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