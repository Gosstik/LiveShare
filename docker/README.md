# Run application with docker-compose

Firstly, create `.env` file as in `.env.sample` to define docker-compose variables.

Run application is similar for every environment:

```bash
docker-compose up -d
```

### Production

Login to registry with created containers:

```bash
docker login
### For self-hosted registry
# docker login localhost:8080
```

Then just run application.

### Development

Do not forget to logout from dockerhub to prevent pulling images.

Clearing docker containers and images:

```bash
### remove stopped and unused containers
docker container prune

### remove only dangling images
docker rmi $(docker images -f "dangling=true" -q)
```

Specific for project:

```bash
# docker-compose rm -f
docker ps -a | grep -v liveshare_db | grep liveshare | awk '{print $1}' | xargs docker rm
docker images -a | grep -v liveshare_db | grep liveshare | awk '{print $3}' | xargs docker rmi -f

# Removing database container
docker rm liveshare_db
```

### Docker networks

There are three default networks in docker:

```bash
NETWORK ID     NAME                 DRIVER    SCOPE
314cb5d400c7   bridge               bridge    local
34daa9acf256   host                 host      local
6c37a875c04c   none                 null      local
```

During build stage (with `docker build -t <image_name> .`) the default network is `bridge`.

During container creation network depends on which way you create container: with `docker` or with `docker-compose`. If you use `docker`, default network is `bridge`. If you use `docker-compose`, default network is `<project>_default`, where `<project>` is the name of directory where `docker-compose.yaml` is located. You can redefine `project` name in `.env` file with `COMPOSE_PROJECT_NAME` (all predefined env variables are described [here](https://docs.docker.com/compose/how-tos/environment-variables/envvars/))

!!! Pay attention that all networks in `networks` section of `docker-compose.yaml` are created as `<project>_<network_name>`.

`bridge` network is a private docker network, separated from `host` network (don't confuse `bridge` network with `bridge` network driver). All containers in `bridge` network share the same network and has access to ports of each other.

!!! Pay attention that despite of the fact, that container in `bridge` network does not have access to host network (cannot use `localhost`), it still can use global network, if dns is properly configured (see below).

`host` network, in contrast, is the network of the host system. It means that container has full access to host network and host can use all ports from container without forwarding.

If there are some issues with network settings in docker, you may build and create container with host network to ensure that the key issue is with network:

`none` means not network at all.

```bash
# Setting networking mode during build
docker build --network host -t <image_name> .
# Connecting contauner to a network
docker create --network host --name <container_name> <image_name>
docker run --network host --name <container_name> <image_name>
```

Or in docker compose:

```yaml
  nginx:
    build:
      context: ./nginx
      dockerfile: Dockerfile
      network: host # use host network ONLY DURING BUILD
      args:
        APP_BUILD_ENV: dev
    network_mode: host # connect container to host network
    # other settings...
```

To use `bridge` or `host` network for services in docker-compose, you have to set the `network_mode` option:

```yaml
services:
  my_service:
    image: your_image
    container_name: your_container_name
    network_mode: bridge  # This connects to the default Docker bridge network
    # other service configurations...
```

!!! Note that you cannot use both `host` and `bridge` network at once. Moreover, you can set only one option of `networks` and `network_mode`.

In order to test which containers are connected to the network you may run (it shows only container ids):

```bash
docker network inspect <network_name>
docker network inspect test_network | grep -A 5 "EnableIPv6" # list five lines after `EnableIPv6` entries
```

Each container also contains information about all of the networks it is connected to:

```bash
docker inspect <container_name>
```

### Using container on cloud VM

By default, docker uses `ipv4` addresses for dns resolution, but on VM there may be only `ipv6` addresses. Therefore, `bridge` network will not have access to the network and you will be unable to download dependencies during image build and all containers without specific network would not have access to global network.

There are two solutions:

1) The most simple but the most dangerous. Always use `--network host` to build and create containers.
2) Enable `ipv6` for `bridge` network. You have to edit (possibly create) file `/etc/docker/daemon.json` and add the following content (seems that `ipv6` and `fixed-cidr-v6` is suficcient for enabling `ipv6`, other option can be removed):

```bash
{
  "ipv6": true,
  "experimental": true,
  "ip6tables": true,
  "fixed-cidr-v6": "2001:db8:1::/64"
}
```

To apply settings you have to restart docker:

```bash
sudo systemctl restart docker
docker network inspect bridge
```

```bash
# Check ipv4 is enabled
cat /proc/sys/net/ipv4/ip_forward

# Check if IPv6 is enabled at the kernel level
cat /proc/sys/net/ipv6/conf/all/disable_ipv6

# sudo sysctl -w net.ipv6.conf.all.forwarding=1 # temp changes
```

Run the following command to see what dns resolvers you are currently using:

```bash
/etc/resolv.conf
```

Run `docker network inspect bridge` and check that `"EnableIPv6": true,` and in `IPAM` config `Subnet` and `Gateway` options are set with `ipv6` addresses.

If you use `docker-compose.yaml`, it will create `<project>_default` network and connect all containers to it. There is no way to force `docker-compose` create that network with `ipv6` enabled, therefore the only solution is to create network with that name in advance. If it exists, `docker-compose` would not recreate it.

Pay attention that if you want to create default `docker-compose` network for project (in order to prevent docker-compose create it with its default settings), you have to add label `com.docker.compose.network`:

```bash
# In case docker-compose.yaml is located in "docker" folder
docker network create --ipv6 --subnet 2001:db8::/64 --gateway 2001:db8::1 --label com.docker.compose.network=default docker_default
```

Simple `ipv6` network can be created in the following way:

```bash
# --label options may be omitted
docker network create \
  --ipv6 \
  --subnet="2001:db8:1::/64" \
  --gateway="2001:db8:1::1" \
  --label environment=production \
  --label ipv6=enabled \
  ipv6_production_network
```

In `docker-compose.yaml` you may declare `ipv6` network:

```yaml
networks:
  my_ipv6_network:
     enable_ipv6: true
     ipam:
       config:
         - subnet: 2001:db8::/64
```

### Fun facts

Here you can find comprehensive guide on how to create networks in `docker-compose.yaml` and set `ipv4` and `ipv6` addresses for containers: [https://rohanzi.gitlab.io/balberin-clouds/project/composenetworking/](https://rohanzi.gitlab.io/balberin-clouds/project/composenetworking/)

When describing network in `networks` section of docker-compose.yaml file, you have two parameters: `internal` and `external`

```yaml
networks:
  backend:
    driver: bridge
    external: true # docker-compose will not create this network, it must be created manually by user
    internal: true  # This network cannot access global internet
```

ipv6: 8 groups each with 16 bytes (e.g. 2001:DB8:0:0:0:0:0:1).

To test that container has connection to the network, try the following:

```bash
# One shot, send 2 packages to `example.com`
docker exec <container_name> ping -c 2 example.com

# Or with entering inside container:
docker exec -it <container_name> /bin/bash
ping -c 2 example.com

# ipv6 loopback interface
curl http://[::1]:80
```

The address `2001:db8::` in most examples [IS RESERVED](https://en.wikipedia.org/wiki/Reserved_IP_addresses#IPv6) for use in documentation.

To send network request to service inside provate docker networks (created in section `networks` with default `bridge` driver) you have to use the following address: `http://<container_name>/<path>`. For example, testing the access to nginx container: `curl -v http://liveshare_nginx/test-location/token`.

`8.8.8.8` and `8.8.4.4` are default dns addresses of `google`
`1.1.1.1` is the default dns address of `cloudflare`
`77.88.8.8` and `77.88.8.1` are the default dns addresses of `yandex`

You may add the following option to `docker-compose.yaml` service:

```yaml
services:
  nginx:
    # options...
    extra_hosts:
      - "host.docker.internal:host-gateway"
    # other options...
```

Now inside `nginx` container you will be able to make requests to `host.docker.internal`, e.g. `http://host.docker.internal/test-location/token`. That request will be forwarded to `localhost` in the following way: `http://localhost/test-location/token`.


Enter container with root user:

```bash
docker exec -it -u root <container_name> /bin/bash
```
