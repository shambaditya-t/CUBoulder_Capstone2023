import socket 

localIP = "127.0.0.1"
localPort = 20002
bufferSize = 1024

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP,localPort))


receiver = UDPServerSocket.recvfrom(bufferSize)
message = receiver[0]
address = receiver[1]

clientMsg = "Message From Client: {}".format(message)
clientIP = "Client IP Address: {}".format(address)

print(clientMsg)
print(clientIP)