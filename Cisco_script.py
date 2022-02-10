#import libraries
import sys
from csv import DictReader

# open file in read mode
with open('C:\\Users\\user_name\\cisco_script\\my_ip.csv', 'r') as read_obj:
    # pass the file object to DictReader() to get the DictReader object
    csv_dict_reader = DictReader(read_obj)

    # iterate over each line as a ordered dictionary
    for row in csv_dict_reader:

        # row variable is a dictionary that represents a row in csv
        Fa = str(row['Fa'])         #fast port number
        Id = str(row['Id#'])        #Id Number
        IpOct = str(row['ip'])      #1st 3 octets
        IpEnd = int(row['ip2'])     #last octect
        Sub = str(row['sub'])       #subnet-mask
        Gate = str(row['gate'])     #gateway
        Central = str(row['central'])       #Central of IR829
        BCentral = str(row['bcentral'])     #bCentral of IR829
        Room = str(row['room'])       #room number from Master spreedsheet
        Central1 = int(Central[11:])        #Central segment
        BCentral1 = int(BCentral[11:])      #bCentral segment
        Deviceu =str(row['deviceu'])      #deviceunit number

        #Read general script from pathIn
        pathIn = 'C:\\Users\\user_name\\cisco_script\\general.txt'
        general_file = open(pathIn,'r')
        general = general_file.read()
        
        #Write console out with all code to path
        path = ('C:\\Users\\user_name\\cisco_script\\Batch_1\\') + (str(Fa) + '_' + 'Id' +str(Id) + '.txt')
        sys.stdout = open(path, 'w')
        
        #General config
        print(general)
        general_file.close()

        #Unique config
        print('conf t')

        #hostname + Ip address
        print(f'''!
hostname Id{Id}-IR829
interface Vlan73
 description device-Vlan
 ip address {IpOct + str(IpEnd+6)} {Sub} secondary
 ip address {IpOct + str(IpEnd+2)} {Sub}
 no ip redirects
 ip pim sparse-mode
snmp-server trap-source Vlan73
no ip igmp snooping vlan 73
exit
!''')

        #Default route
        print(f'''!
conf t
ip Idoute 10.111.8.22 255.255.255.255 {Central[0:11]+str(Central1-1)}
ip Idoute 10.111.9.22 255.255.255.255 {BCentral[0:11]+str(BCentral1-1)}
ip route 10.111.8.0 255.255.255.248 {Gate} name Central-deviceP2P track 3
ip route 10.111.8.0 255.255.255.192 {Gate} name Central-deviceP2P track 3
ip route 10.111.8.64 255.255.255.192 {Gate} name Central-deviceSERVERVLAN track 3
ip route 10.111.8.128 255.255.255.224 {Gate} name Central-deviceMGMTVLAN track 3
ip route 10.111.8.160 255.255.255.224 {Gate} name Central-deviceWSAVLAN track 3
ip route 10.111.8.192 255.255.255.224 {Gate} name Central-deviceWSBVLAN track 3
ip route 10.111.9.0 255.255.255.248 {Gate} name BCentral-deviceP2P track 3
ip route 10.111.9.0 255.255.255.192 {Gate} name BCentral-deviceP2P track 3
ip route 10.111.9.64 255.255.255.192 {Gate} name BCentral-deviceSERVERVLAN track 3
ip route 10.111.9.128 255.255.255.224 {Gate} name BCentral-deviceMGMTVLAN track 3
ip route 10.111.9.160 255.255.255.224 {Gate} name BCentral-deviceWSAVLAN track 3
ip route 0.0.0.0 0.0.0.0 {Gate} name DEFAULT-ROUTE
ip route 10.0.75.0 255.255.255.0 {Gate} name TEMP-CONNECTION-TO-device-LAB
ip route 10.111.8.32 255.255.255.252 {Gate} name Central-deviceCOREIPSLA
ip route 10.111.8.224 255.255.255.248 {Gate} name CentraldeviceDISTRIBUTION-IPSLA
ip route 10.111.9.32 255.255.255.252 {Gate} name BCentral-deviceCOREIPSLA
ip route 10.111.9.224 255.255.255.248 {Gate} name BCentraldeviceDISTRIBUTION-IPSLA
!''')
        
        #Tunnel eigrp 1
        print(f'''!
router eigrp 1
 network {IpOct + str(IpEnd)} 0.0.0.15
 network {Central} 0.0.0.0
 network {BCentral} 0.0.0.0
exit 
!''')

        #Tunnel 1
        print(f'''!
interface Tunnel1
 description to Central-cellular CPE via cellular MPLS
 ip address {Central} 255.255.255.252
 tunnel source Cellular0/0
 tunnel destination 111.222.333.444
end
!''')

        #Tunnel 2
        print(f'''!
config t
interface Tunnel2
 description to BCentral-cellular CPE via cellular MPLS
 ip address {BCentral} 255.255.255.252
 tunnel source Cellular0/0
 tunnel destination 111.222.333.444
end
!''')
        
        #event manager m_cast_Primary
        print(f'''!
conf t
event manager applet mcast_Primary authorization bypass
 event track 3 state up
 action 005 syslog msg "IP SLA 3 up"
 action 010 cli command "conf t"
 action 015 cli command "no ip Idoute 10.111.8.222 255.255.255.255 {Central}"
 action 025 cli command "no ip Idoute 10.111.9.222 255.255.255.255 {BCentral}"
 action 035 cli command "exit"
 action 040 cli command "clear ip Idoute *"
 action 045 cli command "clear ip igmp group vlan 73"
 action 100 syslog msg "Multicast is L2-IGMP"
end
''')

        #event manager m_cast_cellular
        print(f'''!
conf t
event manager applet mcast_cellular authorization bypass
 event track 3 state down
 action 005 syslog msg "IP SLA 3 down"
 action 010 cli command "conf t"
 action 015 cli command "ip Idoute 10.111.8.222 255.255.255.255 {Central}"
 action 025 cli command "ip Idoute 10.111.9.222 255.255.255.255 {BCentral}"
 action 035 cli command "exit"
 action 040 cli command "clear ip Idoute *"
 action 045 cli command "clear ip igmp group vlan 73"
 action 100 syslog msg "Multicast is L3-PIM"
end      
''')

        #sla 1
        print(f'''!
conf t
ip sla 1
 icmp-echo 10.111.8.225 source-ip {IpOct + str(IpEnd + 6)}
 tag Central-DISTRIBUTION-IPSLA-VLAN
 timeout 10000
 frequency 30
ip sla schedule 1 life forever start-time now
!''')
        
        #sla 2
        print(f'''!
ip sla 2
 icmp-echo 10.111.9.225 source-ip {IpOct + str(IpEnd + 6)}
 tag BCentral-DISTRIBUTION-IPSLA-VLAN
 timeout 10000
 frequency 30
ip sla schedule 2 life forever start-time now
!''')
        
        print(f'''!
exit
wr
!''')
        print(f'''!
ping {Gate}
!''')