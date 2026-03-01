# Troubleshooting VPN Connectivity

When users report VPN connection issues:

1. Verify VPN server is reachable: `ping <vpn-gateway-ip>`
2. Check VPN service status on the server: `systemctl status openvpn` or check cloud VPN console
3. Verify user credentials and certificate expiration: `openssl x509 -enddate -noout -in client.crt`
4. Check for split-tunnel vs full-tunnel configuration conflicts
5. Test from client side: try reconnecting, check client logs
6. Verify firewall rules allow VPN traffic (UDP 1194 or TCP 443)
7. Check if the user's IP is blocked by fail2ban or rate limiting
8. Ensure DNS resolution works inside the tunnel
