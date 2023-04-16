from socket import * 
import config
serverPort = 20001
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))

TxFee = 2


def BothBalanceUpdated(transAmount, PayerAccount):
  f = open('BalanceB.txt', 'r')
  if(PayerAccount == '1'):
    B1Name = f.read(9)
    B1_Unconfirmed = config.hex2Dec(f.read(8))
    f.read(1)
    B1_Confirmed = config.hex2Dec(f.read(8))
    B2 = f.read()
    f.close()

    B1_Unconfirmed = str(config.dec2Hex(B1_Unconfirmed + transAmount))
    B1_Confirmed = str(config.dec2Hex(B1_Confirmed + transAmount))

    f = open('BalanceB.txt', 'w')
    f.write(B1Name + B1_Unconfirmed + ':' + B1_Confirmed + B2)
    f.close()
  else:
    f = open('BalanceB.txt', 'r')
    B1 = f.readline()
    B2Name = f.read(9)
    B2_Unconfirmed = config.hex2Dec(f.read(8))
    f.read(1)
    B2_Confirmed = config.hex2Dec(f.read(8))
    
    B2_Unconfirmed = str(config.dec2Hex(B2_Unconfirmed + transAmount))
    B2_Confirmed = str(config.dec2Hex(B2_Confirmed + transAmount))

    f = open('BalanceB.txt', 'w')
    f.write(B1 + B2Name + B2_Unconfirmed + ':' + B2_Confirmed)
    f.close()
    

def updateUncalculated(transAmount,PayerAccount):
  f = open('BalanceB.txt','r')
  if(PayerAccount == '1'):
    B1 = f.read(18)
    B1_Confirmed = config.hex2Dec(f.read(8))
    B2 = f.read()
    f.close()

    tmp = str(config.dec2Hex(B1_Confirmed - transAmount))

    f = open('BalanceB.txt', 'w')
    f.write(B1 + tmp + B2)
    f.close()
    
  else:
    B1 = f.readline()
    B2 = f.read(18)
    B2_Confirmed = config.hex2Dec(f.read(8))
    f.close()

    tmp = str(config.dec2Hex(B2_Confirmed - transAmount))

    f = open('BalanceB.txt', 'w')
    f.write(B1 + B2 + tmp)
    f.close()

print("The server is ready to receive")

while 1:
  message, requesterAddress = serverSocket.recvfrom(2048)
  print("F2 has connected")
  message = message.decode()
  payer = message[0:8]
  payee = message[8:16]
  TxAmount = message[16:24]

  if payer[0] == 'B':
    f = open('Unconfirmed_TB.txt', 'r')
    validTx = False
    for x in range(4):
      tmp = f.read(24)
      if(tmp == message):
        validTx = True
        break
      elif(tmp == '\n'):
        break
      else:
        f.read(1)
    f.close()

    if payer == 'B0000001':
      updateUncalculated(config.hex2Dec(TxAmount) + TxFee, '1')
    else:
      updateUncalculated(config.hex2Dec(TxAmount) + TxFee, '2')
    
    if(validTx == True):
      f = open('Unconfirmed_TB.txt', 'r')
      content = f.readlines()
      f.close()
      f = open('Unconfirmed_TB.txt', 'w')
      flag = False
      for line in content:
        if(line.strip('\n') == message and flag == False):
          flag = True
        else:
          f.write(line)
      f.close()
    else:
      print("Error: invalid Tx occurred")
    f = open('Confirmed_TB.txt', 'a')
    f.write(message + '\n')
    f.close()
  else:
    if payee == 'B0000001':
      BothBalanceUpdated(config.hex2Dec(TxAmount), '1')
    elif payee == 'B0000002':
      BothBalanceUpdated(config.hex2Dec(TxAmount), '2')
    else:
      print("this is the problem")
    f = open('Confirmed_TB.txt', 'a')
    f.write(message + '\n')
    f.close()