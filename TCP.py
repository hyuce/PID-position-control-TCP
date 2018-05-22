#!/usr/bin/python           # This is client.py file
import socket               # Import socket module
import time



s = socket.socket()         # Create a socket object
host = "192.168.43.169"      # Get local machine name
port = 12345              # port

s.connect((host, port))

while True:
    file = open("/home/pi/data.txt","r+")
    mesaj = file.read()
    s.send(mesaj.encode('utf-8'))
    time.sleep(0.01)
    
s.close()
time.sleep(1)


