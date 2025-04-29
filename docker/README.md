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
