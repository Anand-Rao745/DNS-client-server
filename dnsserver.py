#Anand Rao
#asr73
#CS356-008

import sys
import socket
import random
import struct

serverIP = sys.argv[1]
serverPort = int(sys.argv[2])

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.bind((serverIP, serverPort))
inputfile=open("dns-master.txt")
temp=inputfile.readlines()
resource_records=[]
for line in temp:
    if line[0:4]=="host":
        resource_records.append(line.rstrip())

while True:
    message, address=serverSocket.recvfrom(1024)
    client_data_numbers=struct.unpack("iiiii", message[0:20])
    client_data_string=message[20:].decode()
    answer=''
    for record in resource_records:
        if client_data_string in record:
            answer+=record
    response_string=answer.encode()+client_data_string.encode()
    return_code=0
    if not answer:
        return_code=1
    response_numbers=struct.pack("iiiii",2,return_code,client_data_numbers[2],client_data_numbers[3], len(answer))
    serverSocket.sendto(response_numbers+response_string, address)

    
