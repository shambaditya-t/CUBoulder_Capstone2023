import socket 

class BL_Server:
    def __init__(self,port):
        self.localIP = "127.0.0.1"                      #IP Address set to local host 
        self.localPort = port                           #Port, much match with client 
        self.bufferSize = 1024                          #Maximum size of received data 

        self.UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)     #Define and bind UDP socket 
        self.UDPServerSocket.bind((self.localIP,self.localPort))

    def recv_height(self,valid):
        #Validity indicates whether we want to open the server 
        #Used due to blocking behavior 
        if(not valid):
            return 0
        
        receiver = self.UDPServerSocket.recvfrom(self.bufferSize)       #Block until data received in (message, IPAddress) format
        height = receiver[0]                                            #Only selecting for the actual message 
        clientMsg = "{}".format(height)                                 #Format the message 
        print("Received Height: ", clientMsg)
        return int(clientMsg)                                           #Return an integer signifying the height
