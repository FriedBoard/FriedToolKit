import re
import sys

from mininet.cli import CLI
from mininet.net import Mininet
from mininet.topolib import TreeTopo
from mininet.topo import Topo
from mininet.node import Controller, RemoteController, OVSController
from mininet.log import setLogLevel, info, error
from mininet.link import Intf
from mininet.util import quietRun

net = Mininet()

#Define controller
c0 = net.addController('c0', controller=RemoteController, ip='10.100.0.3', port=6633)
host1 = net.addHost('host1')
host2 = net.addHost('host2')

#Give switch real interface
s3 = net.addSwitch('s3')
s2 = net.addSwitch('s2')
_intf = Intf( 'ens192', node=s3 )

#Create links between nodes
net.addLink(host1, s3)
net.addLink(host2, s3)
net.addLink(s3, s2)

#Configure IP addresses
host1.setIP(self,'10.100.0.100',8,None)
host2.setIP(self,'10.100.0.101',8,None)

#h0.cmd("route del -net 0.0.0.0")
#h0.cmd("route add -net 10.100.0.0 netmask 255.255.255.0 " + h0int)

#Start the network
net.start()
