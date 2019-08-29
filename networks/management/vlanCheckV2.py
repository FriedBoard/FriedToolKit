'''

    A script to check if VLANs are present on a switch

'''

# Variables used in the script
requiredVlans = []
configuredVlans = []
missingVlans = []

# A function to get multi line input from a user
def multi_input(requestText):
	try:
		print(requestText)
		while True:
			data=input()
			if not data: break
			yield data
	except KeyboardInterrupt:
		return

# Get the required VLANs
requiredVlans = list(multi_input('Please insert your required VLANs: '))

def checkVlans():
	# Get configured VLANs
	configuredVlans = list(multi_input('Please insert the result of \"show vlan\"'))

	# Check if the requiredVlan is configured
	for requiredVlan in requiredVlans:
		if requiredVlan in configuredVlans:
			print(str(requiredVlan) + ' is configured')
		else:
			missingVlans.append(requiredVlan)

	if len(missingVlans) > 0:
		print('The following VLANs are missing:')
		for missingVlan in missingVlans:
			print(missingVlan)

while True:
    checkVlans()