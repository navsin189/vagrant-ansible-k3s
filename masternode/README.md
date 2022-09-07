## Kubernetes Master Node
## I faced a issue regarding connection between masternode and workernode
- after installing k3s server on master and k3s agent on workernode, I was able to see that workernode is connected to master
```
#on master 
kubectl get nodes 
NAME         STATUS   ROLES                  AGE    VERSION
masternode   Ready    control-plane,master   5d3h   v1.24.4+k3s1
workernode   Ready    <none>                 14m    v1.24.4+k3s1
```
- I thought both are connected now and started deploying my app and database.
- But when i tried to get the terminal of one of the pods, I was unable to 
`kubectl exec -it postgres-deployment-5d775db9c9-2vznd -- bash`
- I was getting `503:connection refused` error and didn't know why.

## Findings:
- 