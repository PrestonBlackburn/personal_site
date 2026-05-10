# Personal Site Helm Chart

![Version: 0.0.1](https://img.shields.io/badge/Version-0.0.1-informational?style=flat-square) ![Type: application](https://img.shields.io/badge/Type-application-informational?style=flat-square) ![AppVersion: 0.0.1](https://img.shields.io/badge/AppVersion-1.0.0-informational?style=flat-square)


**Homepage:** <https://prestonblackburn.com>

## Usage

```bash
helm install -f values.yaml personal-site .
```

## Maintainers

| Name | Email | Url |
| ---- | ------ | --- |
| preston | <prestonblckbrn@gmail.com> | <https://prestonblackburn.com> |

## Source Code

<https://github.com/PrestonBlackburn/personal_site>

## Dependencies

None


## Requirements

- helm
- kubernetes

## Values
 
Example Values:  
```yaml
app:
  deployment_name: personal-site-deployment-prod                           # name of the deployment
  name: personal-site                                                      # app label/root name
  port: 8000                                                               # port to expose app on 
  image_name: personal-site-prod-container                                 # Image name
  image_source: ghcr.io/prestonblackburn/personal_site/personal_site:main  # Image source
  requests:                                                                # directly passed to deployment
    memory: "512Mi" 
    cpu: "500m"
  limits:
    memory: "4096Mi"
    cpu: "4"
```

## Dev

dry run
```bash
helm lint
helm template .
helm install -f values.yaml pat . --dry-run --debug
```

Various ways to deploy
```bash
# requires secret to be created
kubectl create ns personal
kubectl create secret generic personal-site-secrets --from-literal=face-api-password=my-secret -n personal

# from /helm dir
helm install -f values.yaml personal-site . -n personal

# Update helm chart deployment
helm upgrade personal-site . -f values.yaml -n personal
```

Uninstall  
```bash
# uninstall if needed
helm uninstall personal-site -n personal
```

View the deployment  
```bash
kubectl port-forward svc personal-site -n personal -p 8000:8000
```

view at
```bash
http://localhost:8000
```