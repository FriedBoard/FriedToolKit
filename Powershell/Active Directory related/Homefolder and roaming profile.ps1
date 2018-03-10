Get-ADUser -Filter * | Foreach-Object{

    $sam = $_.SamAccountName

    #Home folder requires the SAM to be inserted whereas %USERNAME% does work for profilepath 
    Set-ADuser -Identity $_ -HomeDrive "H:" -HomeDirectory "\\server\folder\$sam" -ProfilePath '\\server\foldder\%USERNAME%'
    
    #The home folder has to be made manually unlike the profile
    md "\\server\folder\$sam"
}