## kubernetes worker node

> If you don't want to use Ansible as a provisioner then you can setup k3s agent by simply running 
```
curl -sfL https://get.k3s.io | INSTALL_K3S_SELINUX_WARN=true INSTALL_K3S_SKIP_SELINUX_RPM=true K3S_KUBECONFIG_MODE=644 K3S_TOKEN=YOUR_TOKEN_VALUE K3S_URL=MASTERNODE_URI  sh -
# MASTERNODE_URI IN MY CASE = https://192.168.1.11:6443
```
> INSTALL_K3S_SELINUX_WARN=true INSTALL_K3S_SKIP_SELINUX_RPM=true is optional. It may work without these in your case.
