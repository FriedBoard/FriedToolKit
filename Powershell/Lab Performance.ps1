#Disable Windows Defender, don't use this on things connected to the internet
Set-MpPreference -DisableRealtimeMonitoring $true
