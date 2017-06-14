# Crate.io @ OSCON 2017 in Austin, TX

This is a demo that was featured on the Crate.io booth at OSCON in May 2017.

## Contents

A container based face tracking application that requires a Raspberry Pi and Raspberry Pi Camera to work; as well as a CrateDB cluster for the data to be inserted into. The demo will use the created Docker container to fetch images from the camera, apply a face-detection algorithm on each frame and store the results in a CrateDB cluster.

## Requirements

As for the hardware, the requirements are pretty simple:

 - Raspberry Pi 3, set up, with Docker installed
 - Raspberry Pi (NoIR) Camera
 - YUM-based Linux machine(s) with access to install CrateDB and software dependencies

## How to use

Please note that this is a demo that was created for an event and might not be maintained at the time you find this. It should stand as an interesting example and provide insights into integrating applications with CrateDB, Raspberry Pis, Ansible, Docker, etc. so expect some tinkering 😊

### Client

This repository is best used for exploring the source code and the deployment mechanisms. In order to deploy and use it, it's best to just download the [pre-built Docker container for ARMv6](https://hub.docker.com/r/crate/pi-facetracker/).

For those who venture into the realms of going deeper into creating the Docker container, please have a look at the [Dockerfile](Dockerfile). Building is very straightforward, but should be done on an ARM device (or your target CPU architecture), since OpenCV contains many natively compiled libraries. *On a Raspberry Pi 3 this could take ~1h*

### Server
On the server, there are two components to be installed: [CrateDB](https://crate.io) and [eden-server](https://github.com/celaus/eden-server), which will be done by using a [Docker compose v3 file](https://blog.docker.com/2017/01/whats-new-in-docker-1-13/#h.o5caosmpdn1z) the [Ansible](https://www.ansible.com/) script located in the deploy folder.

### Deploy

Run this:
```
ansible-playbook -i inventory deploy.yml```

This will install Docker on the server, create various configs, and place (and run) a `docker-compose.yml` in home directory of `root`. On the provided Raspberry Pi addresses this script will do similar things: Create configs/directories but also pull and start the [crate/pi-facetracker:arm](https://hub.docker.com/r/crate/pi-facetracker) Docker container from the Docker Hub.

**For all of this to work, adjust the provided configuration accordingly.** Some values (like server addresses) can't be pre-configured easily :). Set those values into the [inventory file](deploy/inventory)

### Build the container & 3rd Party requirements

In order to build the Docker container, several binary libraries are required. Since they are proprietary software, please download them from [their vendor](https://github.com/raspberrypi/firmware).
 - libbcm_host.so
 - libcontainers.so
 - libmmal.so
 - libmmal_components.so
 - libmmal_core.so
 - libmmal_util.so
 - libmmal_vc_client.so
 - libvchiq_arm.so
 - libvcos.so
 - libvcsm.so

## License

[Apache 2.0](LICENSE)
