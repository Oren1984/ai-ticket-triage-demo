# Granting Elevated Access Permissions

When a user needs temporary elevated access:

1. Verify the request is approved by the user's manager or through ticketing system
2. Determine minimum required permissions (principle of least privilege)
3. For AWS: create time-boxed IAM policy or use AWS SSO permission sets
4. For Kubernetes: create RoleBinding with specific verbs and resources
5. For Linux: add to sudo group or create specific sudoers entry
6. Set expiration: use temporary credentials or schedule permission removal
7. Log the access grant with ticket number, approver, and expiry
8. Follow up to remove access after the maintenance window closes
