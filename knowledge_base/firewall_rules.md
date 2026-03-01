# Managing Firewall Rules

When traffic is blocked by firewall rules:

1. Identify the blocked traffic: source IP, destination IP, port, protocol
2. Check current rules: `iptables -L -n` or cloud security group console
3. Check firewall logs for denied packets: `grep DENY /var/log/firewall.log`
4. Add allow rule if justified: `iptables -A INPUT -s <source> -p tcp --dport <port> -j ACCEPT`
5. For cloud firewalls: update security group or network ACL via console/CLI
6. Save rules persistently: `iptables-save > /etc/iptables/rules.v4`
7. Test connectivity after change: `telnet <host> <port>` or `nc -zv <host> <port>`
8. Document the change in the change management system
