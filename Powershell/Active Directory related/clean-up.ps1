#Clean up script
Remove-ADOrganizationalUnit -Identity ("OU=HU," + (get-addomain | select -ExpandProperty DistinguishedName)