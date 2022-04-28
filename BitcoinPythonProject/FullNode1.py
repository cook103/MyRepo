from socket import *
import blockchain
import config
import hashlib

serverPort = 10000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))

print ('The server is ready to receive')


FullNode1balance = 0
Miningfee = 30
Transaction_fee = 8

while 1:
  message, requesterAddress = serverSocket.recvfrom(2048)
  message = message.decode()

  if requesterAddress[1] == 20000:
    print("FullNode1 server has connected")
    if(len(message) == 24):
      pass
    else:
      serverSocket.sendto(message[136:160].encode(), ('localhost',10001))
      serverSocket.sendto(message[160:184].encode(), ('localhost',10001))
      serverSocket.sendto(message[184:208].encode(), ('localhost',10001))
      serverSocket.sendto(message[208:232].encode(), ('localhost',10001))  
  else:
    print("Client connected")
    serverSocket.sendto(message.encode(), ('localhost', 20000))
    f = open('Temp_T.txt', 'a')
    f.write(message + '\n')
    f.close()

  numTrans = 0
  f = open('Temp_T.txt', 'r')
  for line in f:
    if(line != '\n'):
      numTrans = numTrans + 1
  f.close()
  if(numTrans == 4):
    config.turn = config.turn + 1
    if(config.turn%2 == 1):
      Block = blockchain.UpdatingBlockchain()
      FullNode1balance = Miningfee + Transaction_fee
      f = open('Blockchain.txt', 'a')
      f.write(Block + '\n')
      f.close()
      serverSocket.sendto(Block[136:160].encode(), ('localhost',10001))
      serverSocket.sendto(Block[160:184].encode(), ('localhost',10001))
      serverSocket.sendto(Block[184:208].encode(), ('localhost',10001))
      serverSocket.sendto(Block[208:232].encode(), ('localhost',10001))
      serverSocket.sendto(Block.encode(), ('localhost', 20000))
      print(Block)



