"""
Pre-requisites:

-	Monitor permissions on the IBM switch
-	Configuration permissions on the ASA firewall

Capabilities:
Check if the Inside, Outside or all VLANs that exist on the ASA are configured on a IBM switchport.

"""
#Parameters for script
insidePort = ""
outsidePort = ""

#Variables used in script, warning: does not include all!
inside = []
outside = []
insideVlans = []
outsideVlans = []
allVlans = []
totalPorts = 0


#function to get multi line input from a user
def multi_input(requestText):
	try:
		print(requestText)
		while True:
			data=input()
			if not data: break
			yield data
	except KeyboardInterrupt:
		return

#Get port-channel interfaces, input will contain \n so it loops till there are no more lines
asaRaw = list(multi_input("Please input the result of \" show run | i Port-channel \" , do not include allocate-interface, on the active ASA: "))

#Sanitize the asaRaw input


#Set totalPorts for portCheck later
totalPorts = len(asaRaw)

#Sort inside and outside ports, also sanitize them
for portChannel in asaRaw:
	

	#replace "interface" in input with nothing
	portChannel = portChannel.replace("interface ", "")
	portChannel = portChannel.replace("interface ", "")

	#Put insidePorts in the inside list
	if insidePort in portChannel:
		inside.append(portChannel)
		if portChannel == insidePort:
			inside.remove(portChannel)
			totalPorts = totalPorts - 1
	
	#Put outside ports in the outside list
	if outsidePort in portChannel:
		outside.append(portChannel)
		if portChannel == outsidePort:
			outside.remove(portChannel)
			totalPorts = totalPorts - 1
#End sorting

#Check for missing or double added ports
outputPorts = len(inside) + len(outside)

if totalPorts == outputPorts:
	portCheck = "All ports are included"
elif totalPorts < outputPorts:
	portCheck = "Ports are missing"
elif totalPorts > outputPorts: 
	portCheck = "More ports in original input than in output"  
	
else:
	portCheck = "Something went wrong in portCheck"

#End of check
	
#Start sanitizing both inside and outside to extract VLAN numbers
#Extract insideVlan from insidePorts and store them in insideVlans
for insidePorts in inside:
	#Remove the insidePort from the string
	insideVlan = insidePorts.replace(insidePort, "")
	
	#Remove the . in the Port-channel statement
	insideVlan = insideVlan.replace(".", "")
	
	#Put the insideVlan in the insideVlans list
	insideVlans.append(insideVlan)

#Extract outsideVlan from outsidePorts and store them in outsideVlans
for outsidePorts in outside:
	#Remove the outsidePort from the string
	outsideVlan = outsidePorts.replace(outsidePort, "")
	
	#Remove the . in the Port-channel statement
	outsideVlan = outsideVlan.replace(".", "")
	
	#Put the outsideVlan in the outsideVlans list
	outsideVlans.append(outsideVlan)
		
allVlans = insideVlans + outsideVlans

#Print portCheck status
print(portCheck)

#Start switch port processing
while True:
	#Get required input for switch port processing
	portRaw = list(multi_input("Insert result for \"VLANs:\" section with \" show interface port x\" on switch: "))
	isSpecial = input("Is this port inside, outside or all? ").lower()
	flexCheck = input("Is this a IBM Flex switch yes or no? ").lower()
	
	#Clear vlans list
	vlans = []
	
	#function to process VLANs on generic IBM switches
	def vlan_processing(lines):
		#List object for vlans
		vlans = []
		
		#Process raw input lines
		for line in lines:
			#Remove spaces
			lineVlans = line.replace(" ", "")
		
			#Put VLANS into list
			lineVlans = list(line.split(","))
			vlans = vlans + lineVlans
		
		#Expand VLANs hidden with -
		for vlan in vlans:
			
			#New str object for split check
			vlan = str(vlan)
			
			if "-" in vlan:
				#Split the vlans and create list with missing vlans
				splitVlanList = vlan.split("-")
				
				#Create list with all vlans including start and end
				hiddenVlansInt = list(range(int(splitVlanList[0]), (int(splitVlanList[1]) + 1)))
				
				#List to store string values from range returned ints
				hiddenVlansStr = []
				
				for vlanInt in hiddenVlansInt:
					hiddenVlansStr.append(str(vlanInt))
				
				#Add hiddenVlans to vlans list
				vlans = vlans + hiddenVlansStr
				
				#Remove the old entry
				vlans.remove(vlan)
			
		return(vlans)
	
	#Function to process VLANs on IBM Flex switches
	def vlan_processing_flex(lines):
		#List object for vlans
		vlans = []
		
		#Process raw input lines
		for line in lines:
			#Split based upon the a blank space
			lineVlans = list(line.split(" "))
		
			#Put VLANS into the vlans list
			vlans = vlans + lineVlans
		
		return(vlans)
	
	def vlan_compare(asa, switch):
		missingVlans = []
		for asaVlan in asa:
			if asaVlan not in switch:
				missingVlans.append(asaVlan)
		return missingVlans
	
	#Some logic to find out which VLANs to compare
	#Check if all inside VLANs on the ASA are configured on this port
	if isSpecial == "inside":
		#Check if it's Flex switch input if so use a different processing function
		if flexCheck == "yes":
			vlans = vlan_processing_flex(portRaw)
		elif flexCheck == "no":
			vlans = vlan_processing(portRaw)
		else:
			print("Wrong input given on flex question.")
		
		#Return which VLANs are on the ASA but not on the switchport
		print("The following inside VLANs are missing on this switchport: ")
		
		#check if vlans isn't empty
		if len(vlans) == 0:
			print("Please try again.")
		else:
			print(vlan_compare(insideVlans, vlans))
	
	#Check if all outside VLANs on the ASA are configured on this port
	elif isSpecial == "outside":
		#Check if it's Flex switch input if so use a different processing function
		if flexCheck == "yes":
			vlans = vlan_processing_flex(portRaw)
		elif flexCheck == "no":
			vlans = vlan_processing(portRaw)
		else:
			print("Wrong input given on flex question.")
		
		#Return which VLANs are on the ASA but not on the switchport
		print("The following outside VLANs are missing on this switchport: ")
		
		#check if vlans isn't empty
		if len(vlans) == 0:
			print("Please try again.")
		else:
			print(vlan_compare(outsideVlans, vlans))
	
	#Check if all VLANs that exist on the ASA are available on the port
	elif isSpecial == "all":
		#Check if it's Flex switch input if so use a different processing function
		if flexCheck == "yes":
			vlans = vlan_processing_flex(portRaw)
		elif flexCheck == "no":
			vlans = vlan_processing(portRaw)
		else:
			print("Wrong input given on flex question.")
		
		#Return which VLANs are on the ASA but not on the switchport
		print("The following VLANs are missing on this switchport: ")
		
		#check if vlans isn't empty
		if len(vlans) == 0:
			print("Please try again.")
		else:
			print(vlan_compare(allVlans, vlans))
	
	else:
		print("Wrong input given")
