# Renew SSL Certificates

To renew an expiring or expired SSL certificate:

1. Check current cert expiry: `openssl s_client -connect <host>:443 | openssl x509 -noout -dates`
2. If using Let's Encrypt: `certbot renew --dry-run` then `certbot renew`
3. If using a CA-signed cert: generate new CSR, submit to CA, download new cert
4. Install the new certificate and key in the web server config
5. Reload the web server: `nginx -t && systemctl reload nginx`
6. Verify the new cert: `openssl s_client -connect <host>:443 -servername <host>`
7. Update any pinned certificates in client applications
8. Set up monitoring for next expiry date
