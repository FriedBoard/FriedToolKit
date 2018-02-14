#Creates a base disk based VM
$vmname = read-host 'Naam virtuele machine'
$vhdpath = 'E:\VHD\' + $vmname + '.vhdx'
write-host "
1 Windows server 2012 R2
2 Windows 8.1
3 Windows 10
"
$vmos = read-host "Operating system"
#Create differential VHD according to OS
if ($vmos -eq '1') {
New-VHD -ParentPath E:\VHD\BASE\template2012r2.vhdx -path $vhdpath -differencing -SizeBytes 30GB
}
#create VM and bind vhd
New-VM -Name $vmname -Generation 2 -MemoryStartupBytes 1024MB -VHDPath $vhdpath

#Configure CPU
Set-VMProcessor -VMName $vmname -Count 4

#Configure dynamic memory
Set-VMMemory -VMName $vmname -Buffer 10 -DynamicMemoryEnabled $true -MinimumBytes 256MB -MaximumBytes 1512MB