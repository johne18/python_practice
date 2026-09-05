Build a docker image  
- docker build -t <image_name>:<tag_of_image> .
- docker build -f path/to/Dockerfile -t <image_name>:<tag_of_image> .

Run the docker image (create a running container)  
- docker run --rm -p 8000:8000 <image_name>:<tag_of_image>
    - --rm removes volumes associated with the container at exit
    - -p publishes container's port(s) to host

kubernetes commands
- kind create cluster --name <name_of_k8s_cluster>
- kubectl get nodes
- kubectl cluster-info
- kind load docker-image <image_name>:<tag_of_image> -n <name_of_k8s_cluster>
- kubectl get pods
- kubectl delete pods --all

k8s deployment commands
- kubectl apply -f k8s/<kubernetes_related_file.yml> <- use this to restart deployment if any configuration changes
- kubectl apply -R -f ./k8s/

- kubectl port-forward svc/<name_of_k8s_deployment> 8000:80 - portforward from local machine port to k8s service
- kubectl apply -f k8s/ - Think about what you are deploying when doing this. If structured correctly, it should deploy only manifests for an app
    - ex structure:  
    k8s/app1/<manifest_files>  
    k8s/app2/<manifest_files>

k8s logging and debugging
- kubectl logs deployment/<name_of_k8s_deployment>
- kubectl logs <pod_name>
- kubectl describe pod <pod_name>

k8s rollouts and deletes
- kubectl set image deployment/<name_of_k8s_cluster> <name_of_k8s_cluster>=<newly_deployed_image> - rolling update
- kubectl rollout restart deployment/<name_of_k8s_cluster>
- kubectl rollout undo deployment/<name_of_k8s_cluster>
- kubectl rollout status deployment/<name_of_k8s_cluster>
- kind delete cluster -n <name_of_k8s_cluster>
