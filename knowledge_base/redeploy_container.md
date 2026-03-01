# Redeploy a Docker Container

Steps to redeploy a Docker container with the latest image:

1. Pull the latest image: `docker pull <registry>/<image>:<tag>`
2. Stop the running container: `docker stop <container-name>`
3. Remove the old container: `docker rm <container-name>`
4. Start a new container with the same config: `docker run -d --name <container-name> -p <ports> <image>:<tag>`
5. Verify the container is running: `docker ps` and check health endpoint
6. Review startup logs: `docker logs -f <container-name>`

For docker-compose deployments: `docker compose pull && docker compose up -d`
