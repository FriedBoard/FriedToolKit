#Install the AD-domain-services feature

#true or false
$managementTools = $true

#Check if ad-domain-services role is installed
$role = Get-WindowsFeature -Name ad-domain-services
$rolePresent = $role.Installed

#Start by installing the role
if($rolePresent -eq $true){
    #If ad-domain-services is already installed do nothing
    write-host('Active Directory role is already installed. Proceeding with domain controller installation.')
}

else{
    #Else install the service with or without management tools specified
    if($managementTools -eq $true){
        Install-WindowsFeature ad-domain-services -IncludeManagementTools 
    }
    else{
        Install-WindowsFeature ad-domain-services
    }
}

Restart-Computer