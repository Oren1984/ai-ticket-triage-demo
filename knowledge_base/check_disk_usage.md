# Check and Clean Disk Space

When disk usage alerts fire, follow this procedure:

1. Check overall usage: `df -h`
2. Find large directories: `du -sh /* | sort -rh | head -20`
3. Check for large log files: `find /var/log -type f -size +100M`
4. Clean old logs: `journalctl --vacuum-time=3d`
5. Remove old Docker images: `docker system prune -a --filter "until=168h"`
6. Check for old package caches: `apt-get clean` or `yum clean all`
7. Remove old temp files: `find /tmp -type f -mtime +7 -delete`
8. Verify space recovered: `df -h`
