import socket
#import time

def client(): 
    print("I am a client")
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        client.bind(("", 8080))       
        data = 0
        client.settimeout(5)
        #time.sleep(0.2)
        while True:
            data = client.recvfrom(1024).decode()
            client.close()
            print("received message: %s"%data)
            # break to peer to peer
            #else if timeout break to server
    except:
        print("cannot find port 8080 :( ") 
        client.shutdown(socket.SHUT_RDWR)
        client.close()
        return data

def server():
    print("I am now a server")
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    server.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST, 1)
    
    
    try:
        server.bind(("", 80))
        server.settimeout(5)
        message = b"44444"
        #while True:
        server.sendto(message, ('<broadcast>', 8080))
        print("message sent!")
    except: 
        print("cannot find port 44444")
        server.shutdown(socket.SHUT_RDWR)
        server.close()
        #time.sleep(1)


def p2p():
    print("we bacame peer to peer yaaay")
  
    
result = client()

if result == 0:
    server()
else:
    p2p()