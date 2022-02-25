1. Test Syarpa
```django
python manage.py test
```

2. Build Container
```docker
docker build -f Dockerfile \
  -t registry.digitalocean.com/syarpa/syarpa-slim-burster:v1.0.0 
  -t registry.digitalocean.com/syarpa/syarpa-slim-burster:v1.0.1 
```

3. Push Container with 2 tags: latest and random

```docker
docker push registry.digitalocean.com/syarpa/syarpa-slim-burster --all-tags
```

4. Update secrets (if needed)

```kubernetes helm
kubectl delete secret syarpa-k8s-web-prod-env
kubectl create secret generic syarpa-k8s-web-prod-env --from-env-file=web/.env.prod
```

5. Update Deployment `k8s/apps/syarpa-slim-burster.yaml`:

Add in a rollout strategy:
`imagePullPolicy: Always`


### Four ways (given above) to trigger a deployment rollout (aka update the running pods):
- Forced rollout
Given a `imagePullPolicy: Always`, on your containers you can:

```kubernetes helm
kubectl rollout restart deployment/syarpa-slim-burster-deployment
```

- Image update:
```kubernetes helm
kubectl set image deployment/syarpa-slim-burster-deployment syarpa-slim-burster=registry.digitalocean.com/syarpa/syarpa-slim-burster:latest
```

- Update an Environment Variable (within Deployment yaml):

```yaml
env:
  - name: Version
    value: "abc123"
  - name: PORT
    value: "8002"
```

- Deployment yaml file update:

Change 
```
image: registry.digitalocean.com/syarpa/syarpa-slim-burster:latest
```
to
```
image: registry.digitalocean.com/syarpa/syarpa-slim-burster:v1 
```

Keep in mind you'll need to change `latest` to any new tag(s) you might have (not just `v1`)
```kubernetes helm
kubectl apply -f k8s/apps/syarpa-slim-burster.yaml
```


6. Roll Update:
```kubernetes helm
kubectl rollout status deployment/syarpa-slim-burster-deployment
```
7. Migrate database

Get a single pod (either method works)

```yaml
export SINGLE_POD_NAME=$(kubectl get pod -l app=syarpa-slim-burster-deployment -o jsonpath="{.items[0].metadata.name}")
```
or 
```yaml
export SINGLE_POD_NAME=$(kubectl get pod -l=app=syarpa-slim-burster-deployment -o NAME | tail -n 1)
```

Then run `migrate.sh` 

```kubernetes helm
kubectl exec -it $SINGLE_POD_NAME -- bash /app/migrate.sh
```