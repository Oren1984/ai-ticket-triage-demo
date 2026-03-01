# Restart a Crashed Microservice

When a microservice becomes unresponsive or crashes repeatedly, follow these steps:

1. Check service status: `systemctl status <service-name>` or `docker ps -a`
2. Review recent logs: `journalctl -u <service-name> --since "10 min ago"` or `docker logs --tail 100 <container>`
3. Check for resource exhaustion: `free -m` and `df -h`
4. Restart the service: `systemctl restart <service-name>` or `docker restart <container>`
5. Verify it comes back healthy: check health endpoint or `systemctl is-active <service-name>`
6. If it crash-loops, check for config changes, dependency failures, or OOM kills in `dmesg`
