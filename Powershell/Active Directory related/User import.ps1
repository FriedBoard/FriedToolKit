#Import CSV
$csv = Import-Csv -Delimiter ";"  "users.csv"
$groupList = New-Object System.Collections.ArrayList
$OUList = New-Object System.Collections.ArrayList

foreach($user in $csv){
    #Add every group in the groupList variable
    $OUList.Add($user.OrganisationalUnit)
}
#Get all unique groups and create those
$OUList = $OUList | select -Unique
foreach($OU in $OUList){
    New-ADOrganizationalUnit -Name $OU -ProtectedFromAccidentalDeletion $FALSE
}

foreach($user in $csv){
    #Add every group in the groupList variable
    $groupList.Add($user.Group)
}
#Get all unique groups and create those
$groupList = $groupList | select -Unique
foreach($group in $groupList){
    $groupPath = "OU=HU," + (get-addomain | select -ExpandProperty DistinguishedName) 
    New-ADGroup -Name $group -GroupScope global -Path $groupPath
}

foreach($user in $csv){
    $userPassword = ConvertTo-SecureString $user.Password -AsPlainText -Force
    $userPath = "OU=" + $user.OrganisationalUnit + ","  + (get-addomain | select -ExpandProperty DistinguishedName) 
    New-ADUser -Name $user.Name -GivenName $user.Name -AccountPassword $userPassword -ChangePasswordAtLogon $FALSE -PasswordNeverExpires $TRUE -UserPrincipalName $user.Name -Enabled $TRUE -Path $userPath
    Add-ADGroupMember -Identity $user.Group -Members $user.Name
}