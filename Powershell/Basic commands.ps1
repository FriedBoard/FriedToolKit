#Fetches local computers name, domain and domainrole
Get-ComputerInfo | select CsName,CsDomain,CsDomainRole

#Get IPv4 configuration of the local machine, you know because ipconfig isn't powershell
Get-NetIPAddress | where{$_.AddressFamily -eq "IPv4"} | select InterfaceAlias,IPAddress,PrefixLength

Get-DnsClientServerAddress -AddressFamily IPv4 | where{$_.ServerAddresses -ne "{}"} | select InterfaceAlias,ServerAddresses