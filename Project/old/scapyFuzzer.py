
from scapy.all import *
from tcpSession import TcpSession

request = "GET /bWAPP/login.php HTTP/1.1\r\n" \
        + "Host: localhost\r\n" \
        + "Accept: text/html,text/php,text/css,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n" \
        + "Connection: keep-alive\r\n" \
        + "Cookie: security_level=0; PHPSESSID=0\r\n\r\n"



conf.L3socket=L3RawSocket

sport = random.randint(1024,65535)


# SYN
# ip=IP(src='127.0.0.1',dst='127.0.0.1')
# SYN=TCP(sport=sport,dport=80,flags='S',seq=1000)
# SYNACK=sr1(ip/SYN)

# #print(SYNACK.show())

# # SYN-ACK
# ACK=TCP(sport=sport, dport=80, flags='A', seq=SYNACK.ack, ack=SYNACK.seq + 1)
# send(ip/ACK)

# #need to use the following command to prevent reset packets being sent

# #iptables -A OUTPUT -p tcp --tcp-flags RST RST -s 127.0.0.1 -j DROP

# PACK=TCP(sport=sport, dport=80, flags='PA', seq=SYNACK.ack, ack=SYNACK.seq + 1)

#message = sr(ip/PACK/request, timeout=3, multi=5)
#ACK=TCP(sport=sport, dport=80, flags='A', seq=SYNACK.ack, ack=SYNACK.seq + 1)
#send(ip/ACK)

#send(ip/ACK)
#print(len(message))
#print(len(message[0]))
#print(len(message[0][0]))
#print(len(message[0][0][0]))
#packets = sniff(count=1, filter="tcp and host 127.0.0.1")
#wrpcap('answer.pcap', packets, append=True)

# 0 1 1 has html payload

#print message[0][1][0].show()

# def removeEthernet(packet):
#     inputString = packet.command()
#     index = inputString.find(")/")
#     newCmd = inputString[index + 2:]
#     #print(newCmd)
#     return eval(newCmd)

# conf.L3socket=L3RawSocket
# stream = rdpcap("sendLogin.pcapng")

# #send(stream[0])

# stream = [removeEthernet(drib) for drib in stream]


# #print(stream[0].show())

# #sr(stream[0])
# ret = sr(stream[0])

sess = TcpSession(("127.0.0.1", 80))
sess.connect()
sess.sr(request)
sess.close()


