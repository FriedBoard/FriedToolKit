#This script replaces interface names in router configurations made using GNS3

import csv
import fileinput

#End part of the configuration file name
configuration = "_startup-config.cfg"

with open('InterfaceMapping.csv', 'r') as mapping:
    #Read the CSV file and convert lines
    mappingLines = csv.reader(mapping, delimiter=';')
    
    #Skip the first row
    next(mappingLines)
    
    #Now start working through the configurations
    for map in mappingLines:
        configurationName = map[0] + configuration
        
        try:
            #Open the configuration file for this row and keep a backup
            with fileinput.FileInput(configurationName, inplace=True, backup='.bak') as configurationFile:
                
                #Search and replace the GNS3 value with the IRL value in the configuration
                for line in configurationFile:
                    print(line.replace(map[1], map[2]), end='')
        except:
            print(configurationName + " is ongeldig.")
