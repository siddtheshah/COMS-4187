

from scapy.all import *

def removeEthernet(packet):
    inputString = packet.command()
    index = inputString.find(")/")
    newCmd = inputString[index + 2:]
    #print(newCmd)
    return eval(newCmd)

conf.L3socket=L3RawSocket
stream = rdpcap("sendLogin.pcapng")

#send(stream[0])

stream = [removeEthernet(drib) for drib in stream]


#print(stream[0].show())

#sr(stream[0])
sr(stream[0])