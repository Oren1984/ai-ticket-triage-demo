# Fixing DNS Resolution Failures

When DNS resolution fails for internal or external hostnames:

1. Test resolution: `nslookup <hostname>` or `dig <hostname>`
2. Check /etc/resolv.conf for correct nameserver entries
3. Test against specific DNS server: `dig @8.8.8.8 <hostname>`
4. Check if local DNS cache is stale: `systemd-resolve --flush-caches`
5. Verify DNS server is running: `systemctl status named` or check cloud DNS console
6. Check for DNSSEC validation failures: `dig +dnssec <hostname>`
7. Look for recent DNS zone changes that might have propagation delays
8. Check network connectivity to DNS servers: `ping <dns-server-ip>`
