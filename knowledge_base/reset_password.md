# Reset User Password in Active Directory

To reset a user's password in Active Directory:

1. Open Active Directory Users and Computers (ADUC) or use PowerShell
2. Locate the user account: `Get-ADUser -Identity <username>`
3. Reset the password: `Set-ADAccountPassword -Identity <username> -Reset -NewPassword (ConvertTo-SecureString "TempP@ss123" -AsPlainText -Force)`
4. Force password change at next login: `Set-ADUser -Identity <username> -ChangePasswordAtLogon $true`
5. Unlock the account if locked: `Unlock-ADAccount -Identity <username>`
6. Notify the user of their temporary password via secure channel
