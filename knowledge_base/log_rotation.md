# Setting Up and Fixing Log Rotation

When logs consume excessive disk space:

1. Check current logrotate config: `cat /etc/logrotate.d/<service>`
2. Verify logrotate is running: `cat /var/lib/logrotate/status`
3. Test rotation manually: `logrotate -d /etc/logrotate.d/<service>` (dry run)
4. Force rotation: `logrotate -f /etc/logrotate.d/<service>`
5. Standard config template: rotate 7 daily, compress, delaycompress, missingok
6. For Docker: configure logging driver with max-size and max-file options
7. For application logs: ensure the app handles SIGHUP for log file reopening
8. Set up monitoring alert when log directory exceeds threshold
