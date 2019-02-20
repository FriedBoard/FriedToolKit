import re
import sys
import time
import mininet

from mininet.cli import CLI
from mininet.net import Mininet
from mininet.topolib import TreeTopo
from mininet.topo import Topo
from mininet.node import Controller, RemoteController, OVSController
from mininet.log import setLogLevel, info, error
from mininet.link import Intf
from mininet.util import quietRun

#Ask how many hosts are required.
number = int(input('How many hosts would you like? '))

net = Mininet()
allhosts = []

#Fill the allhosts array with hostnames
while ( number > 0):
    hostnumber = str(number)
    hostname = str('h' + hostnumber)
    allhosts.append(hostname)
    number = number -1

#Add the opendaylight controller
c0 = net.addController('c0', controller=RemoteController, ip='10.100.0.3', port=6633)

#Give switch real interface
s2 = net.addSwitch('s2')
s3 = net.addSwitch('s3')

net.addLink(s2, s3)

#Generate all hosts and set ip to 0.0.0.0 to allow dhclient to set the IP later on
for host in allhosts:
    print('Creating host ' + host)
    exec(host + ' = ' + 'net.addHost(\'' + host + '\', ip=\'0.0.0.0\')')
    exec('net.addLink(' + host + ', s2)')

#Add real interface to switch x
_intf = Intf('ens192', node=s3)

#Wait 3 seconds to be sure the interface is added correctly before the network is started.
time.sleep(3)

#Start the network
net.start()

#Set hosts to use DHCP
print 'Configuring DHCP for clients now.'
for host in allhosts:
    exec(host + '.cmd(\'dhclient ' + host + '-eth0\')')
    print('DHCP configured successfully for: ' + host)
    #Make the host ping the gateway so that it appears on the OpenDayLight Controller.
    print('Host: ' + host + ' will now ping the  gateway 4 times')
    exec(host + '.cmd(\'ping -c 4 10.101.0.254\')')
    print('Ping excuted successfully')

#Enter mininet commandline
CLI(net)

#Stop mininet on exit
net.stop()
