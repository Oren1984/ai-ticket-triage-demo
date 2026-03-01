# Common Nginx Configuration Fixes

Troubleshooting and fixing common Nginx issues:

1. Test config syntax: `nginx -t`
2. Fix 502 Bad Gateway: check upstream service is running, verify proxy_pass URL
3. Fix 413 Request Entity Too Large: increase `client_max_body_size` in nginx.conf
4. Fix SSL errors: verify cert chain is complete, check file permissions on key
5. Fix redirect loops: check `return` and `rewrite` rules for circular redirects
6. Enable access logs for debugging: `access_log /var/log/nginx/debug.log combined;`
7. Reload after changes: `systemctl reload nginx` (not restart, to avoid downtime)
8. Check worker connections if hitting limits: increase `worker_connections` in events block
