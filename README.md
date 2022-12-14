# Kubernetes Cluster setup case 1

## Operating system used:
- Windows(Host Machine)
- Centos(Guest Machine)

## Tools and Technologies used:
- [k3s](https://k3s.io/)
- [Vagrant](https://www.vagrantup.com/)
- [Ansible](https://www.ansible.com/)
- [Docker](https://www.docker.com/)

## Vagrant setup:
- Virtualization enabled
- Download vagrant installer from official website
- should have Hyper type 2 application like Oracle virtualbox, VMWare.
- any terminal for doing SSH like git bash, windows terminal etc.

## Issue faced:
### Related to k3s cluster
- while installing on Redhat 8 using `curl -sfL https://get.k3s.io | sh -` it failed.
- The error was `nothing provides container-selinux & selinux-policy-base needed by k3s-selinux`
- while setting up **workernode** ansible is taking so much time and *needs to re run the playbook by doing ssh*^@1^.

### Solution
- while calling the above command I passed two parameter mainly to skip k3s selinux installation and
- **INSTALL_K3S_SELINUX_WARN** and **INSTALL_K3S_SKIP_SELINUX_RPM** set to true.
- The command might work for you without these enviromental variables, give a try.
- For @1, it may not cause issue on your system but give a try if you face the same issue

# Kubernetes Cluster setup case 2

## Operating system used:
- Windows(Host Machine)
- Rocky 9(Guest Machine)

## Tools and Technologies used:
- [k3s](https://k3s.io/)
- [Rocky 9 ISO Image](https://rockylinux.org/download)
- [Oracle Virtual Box](https://www.virtualbox.org/wiki/Downloads)

## How to setup
- create two virtual machines i) Masternode ii) Workernode
- **Change the network type from NAT to Bridge.**
- **Change the hostname** `hostnamectl set-hostname master` and `hostnamectl set-hostname worker1`. **Hostname should be unique**
- reboot the machine
- install [EPEL repo](https://docs.fedoraproject.org/en-US/epel/#_almalinux_9_rocky_linux_9)
```
dnf config-manager --set-enabled powertools
dnf install epel-release epel-next-release -y
dnf install net-tools  vim -y
ifconfig enp0s3 # gives the IP address of your system
```
### Setup Masternode
- install [k3s](https://k3s.io/)
```
Sudo curl –sfL https://get.k3s.io | K3S_TOKEN="rocky" K3S_KUBECONFIG_MODE=644 sh –
# you can change the value of token. config mode allow kubctl to read the config file of k3s
# curl command will download the index.sh filde from the offical page.
systemctl status k3s
```
- `ifconfig enp0s3` gives the IP address of your masternode

### Setup Workernode
- install [k3s](https://k3s.io/)
```
Sudo curl –sfL https://get.k3s.io | K3S_TOKEN="rocky" K3S_KUBECONFIG_MODE=644 K3S_URL=https://192.168.1.3 sh -
# pass the same token as you did to master. Token used for validation
# K3S_URL takes the URL of masternode and only allows https request
systemctl status k3s-agent
```
> We are done setting up both nodes.

## Deployment
- First deploy the database.
- then deploy the webapp.
```
kubectl apply -f postgres_deployment.yml
kubectl apply -f postgres_deployment.yml
```
- First, It'll take time to deploy the pods as docker image is not locally present.
- To interact with K3s pods

```
kubectl exec  pod_name – command
#kubectl exec -it postgres-deployment-f4577c9b-b88rk --  sh
```

### Validate
- when deployment is successful, you can check the webapp on `http://workernode_ip:30124`

### Note
- The webapp is not fully functional yet. Auth is working fine but the dashboard is still a prototype.
- Also all the webapges has been taken from codepen
- [DashBoard](https://codepen.io/kristen17/pen/gOeyKyy)
- [Error Page](https://codepen.io/Navedkhan012/pen/vrWQMY)
- [Auth Page](https://codepen.io/colorlib/pen/rxddKy)
