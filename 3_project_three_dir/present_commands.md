kind create cluster --config ./3_project_three_dir/kind-config.yml -n pokemon-cluster
kind load docker-image pokemon-fastapi:v1 pokemon-fastapi:v2 pokemon-worker:v1 -n pokemon-cluster
kubectl apply -R -f ./3_project_three_dir/k8s
kubectl apply -f ./3_project_three_dir/pokemon_worker/worker-job.yml 



docker images
docker run --rm -p 8000:8000 pokemon-fastapi:v1



kubectl get pods
kubectl get endpoints
kubectl delete pod pod_name
kubectl get pods
kubectl get endpoints



kubectl exec -it POD_NAME -- cat ../etc/configs/example.properties



kubectl logs pod_name
kubectl exec -it deployment/postgres -- psql -U postgres -d pokemon -c "select * from pokemon limit 5;"
kubectl get pvc postgres-pvc
kubectl get pvc prometheus-pvc
pokemon_requests_total{endpoint="/health"}



kubectl get pods
kubectl describe pods pod_name | grep Image
kubectl apply -f ./3_project_three_dir/k8s/pokemon-api/deployment.yml 
kubectl rollout status deployment/pokemon-fastapi
kubectl get pods
kubectl describe pods pod_name | grep Image

kubectl rollout undo deployment/pokemon-fastapi
kubectl describe pods pod_name | grep Image



kubectl logs jobs/pokemon-worker