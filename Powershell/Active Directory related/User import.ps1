#Import CSV
$csv = Import-Csv -Delimiter ";"  "users.csv"

#Create list objects to store groups and organisational units associated with users
$groupList = New-Object System.Collections.ArrayList
$OUList = New-Object System.Collections.ArrayList

#For every user add their organisational un