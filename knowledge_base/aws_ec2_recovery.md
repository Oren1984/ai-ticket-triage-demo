# Recovering Stuck EC2 Instances

When an EC2 instance is stuck or unresponsive:

1. Check instance status: `aws ec2 describe-instance-status --instance-ids <id>`
2. Review system and instance status checks in AWS Console
3. Try stop and start (not reboot): `aws ec2 stop-instances --instance-ids <id>` then `aws ec2 start-instances --instance-ids <id>`
4. If stuck in stopping: force stop via `aws ec2 stop-instances --instance-ids <id> --force`
5. Check system log: `aws ec2 get-console-output --instance-id <id>`
6. If persistent: detach root volume, attach to recovery instance, fix issues, reattach
7. Verify security group and network ACL haven't changed
8. Check if the instance is on degraded hardware: migrate to new host if needed
