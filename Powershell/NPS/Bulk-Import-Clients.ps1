'
This script is made to bulk import RADIUS clients into NPS from a csv.

The nps_client.csv file should contain a column named name, address and secret. 
Name will be set as friendly name for the client while address will be used as the address.
Secret will be used as the secret for this client.
'

#Import CSV
$csv = Import-Csv -Delimiter ";"  "nps_clients.csv"

#Loop to add the clients
foreach($client in $csv){
    #Add the client
    New-NpsRadiusClient -Address $client.address -Name $client.address -SharedSecret $client.secret
}
