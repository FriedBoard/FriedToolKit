#Install the domain or forest
#Set to true if this is the first domain controller in the forest. 
#Else set it to false to add a domain controller to the forest

$installForest = $true

#Set installation parameters
$domainName = 'bmc.local' 
$installDns = $true
$domainNetbios = 'bmc'

if($installDns -eq $true){
    if($installForest -eq $true){
            write-host('Installing forest ' + $domainName + ' with dns now.' )
            Install-ADDSForest -DomainName $domainName -InstallDns -DomainNetbiosName $domainNetbios -Confirm:$false
        }
        else{
            write-host('Adding this computer as domain controller to ' + $domainName + ' with dns now.' )
            Install-ADDSDomainController -DomainName $domainName  -InstallDns -Confirm:$false
    }
}
else{
    if($installForest -eq $true){
            write-host('Installing forest ' + $domainName + ' without dns now.' )
            Install-ADDSForest -DomainName $domainName -DomainNetbiosName $domainNetbios -Confirm:$false
        }
        else{
            write-host('Adding this computer as domain controller to ' + $domainName + ' without dns now.' )
            Install-ADDSDomainController -DomainName $domainName -Confirm:$false
    }
}