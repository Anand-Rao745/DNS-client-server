#Anand Rao
#asr73
#CS356-008

import sys
import socket
import struct
import random

serverIP = sys.argv[1]
serverPort = int(sys.argv[2])
hostname=sys.argv[3]
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientsocket.settimeout(1)

temp=str(hostname)+" A IN"
message_ID=random.randint(1,100)
numbers=struct.pack("iiiii", 1,0,message_ID,len(temp),0)
question=temp.encode()

i=0
while i<3:
    try:
        print("Sending Request to "+str(serverIP)+", "+str(serverPort)+":")
        clientsocket.sendto(numbers+question, (serverIP,serverPort))
        if i==0:        
            print("Message ID: "+str(message_ID))
            print("Question Length: "+ str(len(temp))+ " bytes")
            print("Answer Length: 0 bytes")
            print("Question: "+temp)
            print("\n") 

        message, address=clientsocket.recvfrom(1024)
        server_data_numbers=struct.unpack("iiiii", message[0:20])
        server_data_string=message[20:].decode()
        server_return_code=server_data_numbers[1]

        print("Received Response from "+str(serverIP)+", "+str(serverPort)+":")
        if server_return_code==0:
            print("Return Code: 0 (No errors)")
        else:
            print("Return Code: 1 (Name does not exist)")
        print("Message ID: "+str(server_data_numbers[2]))
        print("Question Length: "+ str(server_data_numbers[3])+ " bytes")
        print("Answer Length: "+ str(server_data_numbers[4])+ " bytes")
        print("Question: "+server_data_string[server_data_numbers[4]:])
        if server_return_code==0:
            print("Answer: "+server_data_string[0:server_data_numbers[4]])
        break

    except socket.timeout:
        if i<2:
            print("Request timed out...")
        else:  
            print("Request timed out ... Exiting Program.")
            sys.exit(1)
        i+=1

clientsocket.close()
