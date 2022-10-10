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
- On Vagrant the first adapter that is `eth0` and it is configured for **NAT**.
- Vagrant uses it for basic communication.
- But I have to use **bridge** network that can be *adapter2* or *adapter3* but as I said **workernode** will try to connect to `eth0`. 
- On github issues it is mentioned to run k3s like `k3s server   --node-external-ip 192.168.50.4 --node-ip 192.168.50.4`
- but I want to run it through systemctl instead of manually.
- So I read `/etc/systemd/system/k3s.service` file and checked for start command.
- Then I changed `ExecStart=/usr/local/bin/k3s server --node-external-ip 192.168.50.4  --node-ip 192.168.50.4 \` from `ExecStart=/usr/local/bin/k3s server`
- `192.168.50.4` is my master node IP.
- **After that connection was established and I was able to connect to pods shell**.

> If you don't want to use Ansible as a provisioner then you can setup k3s master by simply running 
```
curl -sfL https://get.k3s.io | INSTALL_K3S_SELINUX_WARN=true INSTALL_K3S_SKIP_SELINUX_RPM=true K3S_KUBECONFIG_MODE=644 K3S_TOKEN=YOUR_TOKEN_VALUE sh -
```
> INSTALL_K3S_SELINUX_WARN=true INSTALL_K3S_SKIP_SELINUX_RPM=true is optional. It may work without these in your case.