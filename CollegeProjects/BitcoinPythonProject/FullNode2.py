from socket import *
import blockchain
import config


serverPort = 20000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))

FullNode2balance = 0
Miningfee = 30
Transaction_fee = 8


print ('FullNode2.py is ready to receive')

while 1:
  message, requesterAddress = serverSocket.recvfrom(2048)
  message = message.decode()

  if requesterAddress[1] == 10000:
    print("F1 server has connected")
    if(len(message) == 24):
      pass
    else:
      serverSocket.sendto(message[136:160].encode(), ('localhost',20001))
      serverSocket.sendto(message[160:184].encode(), ('localhost',20001))
      serverSocket.sendto(message[184:208].encode(), ('localhost',20001))
      serverSocket.sendto(message[208:232].encode(), ('localhost',20001))  
  else:
    print("a client has connected")
    serverSocket.sendto(message.encode(), ('localhost', 10000))
    f = open('Temp_T.txt', 'a')
    f.write(message + '\n')
    f.close()

  numTrans = 0
  f = open('Temp_T.txt', 'r')
  for line in f:
    if(line != '\n'):
      numTrans += 1
  f.close()
  if(numTrans == 4):
    config.turn = config.turn +  1
    if(config.turn%2 == 0):
      Block = blockchain.UpdatingBlockchain()
      FullNode2balance = Miningfee + Transaction_fee
      f = open('Blockchain.txt', 'a')
      f.write(Block + '\n')
      f.close()
      serverSocket.sendto(Block[136:160].encode(), ('localhost',20001))
      serverSocket.sendto(Block[160:184].encode(), ('localhost',20001))
      serverSocket.sendto(Block[184:208].encode(), ('localhost',20001))
      serverSocket.sendto(Block[208:232].encode(), ('localhost',20001))
      serverSocket.sendto(Block.encode(), ('localhost', 10000))
      print(Block)