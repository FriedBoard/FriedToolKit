#Import CSV
$csv = Import-Csv -Delimiter ";"  "users.csv"

#Create list objects to store groups and organisational units associated with users
$groupList = New-Object System.Collections.ArrayList
$OUList = New-Object System.Collections.ArrayList

#For every user add their organisational unit to the OUList variable
foreach($user in $csv){
    #Add every group in the groupList variable
    $OUList.Add($user.OrganisationalUnit)
}


#Reassign the OUList to only have unique values in it
$OUList = $OUList | select -Unique

#For every OU in the OUList create it
foreach($OU in $OUList){
    New-ADOrganizationalUnit -Name $OU -ProtectedFromAccidentalDeletion $FALSE
}

#For every user in the CSV add their group to the groupList variable
foreach($user in $csv){
    $groupList.Add($user.Group)
}


#Reassign the groupList variable to only have unique values in it
$groupList = $groupList | select -Unique

#For every group in groupList create it in the domain root
foreach($group in $groupList){
    $groupPath = "OU=HU," + (get-addomain | select -ExpandProperty DistinguishedName) 
    New-ADGroup -Name $group -GroupScope global -Path $groupPath
}

#For every user in the CSV create it with it's associated properties
foreach($user in $csv){
    #Convert the plaintext password to a securestring new-aduser will accept
    $userPassword = ConvertTo-SecureString $user.Password -AsPlainText -Force

    #Set the location of the user to their OU
    $userPath = "OU=" + $user.OrganisationalUnit + ","  + (get-addomain | select -ExpandProperty DistinguishedName)

    #Create the user account in Active Directory as specified
    New-ADUser -Name $user.Name -GivenName $user.Name -AccountPassword $userPassword -ChangePasswordAtLogon $FALSE -PasswordNeverExpires $TRUE -UserPrincipalName $user.Name -Enabled $TRUE -Path $userPath

    #Add the user account to their associated group
    Add-ADGroupMember -Identity $user.Group -Members $user.Name
}