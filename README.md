# Kubernetes Cluster setup

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

