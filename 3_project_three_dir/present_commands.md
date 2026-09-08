kind create cluster --config ./3_project_three_dir/kind-config.yml -n pokemon-cluster
kind load docker-image pokemon-fastapi:v1 pokemon-fastapi:v2 pokemon-worker:v1 -n pokemon-cluster
kubectl apply -R -f ./3_project_three_dir/k8s


docker images
docker run --rm -p 8000:8000 pokemon-fastapi:v1


kubectl get pods
kubectl get endpoints


kubectl exec -it POD_NAME -- cat ../etc/configs/example.properties


kubectl get pvc prometheus-pvc
kubectl get pvc postgres-pvc
kubectl exec -it deployment/postgres -- psql -U postgres -d pokemon -c "select * from pokwmon limit 5;"
kubectl logs -f pod/pokemon-fastapi-5ccbc86dfc-t26p7
pokemon_requests_total{endpoint="/health"}