from socket import * 
import config
serverPort = 10001
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))

TxFee = 2

def BothBalanceUpdate(transAmount, PayerAccount):
  f = open('BalanceA.txt', 'r')
  if(PayerAccount == '1'):
    A1 = f.read(9)
    A1_unconfirmed = config.hex2Dec(f.read(8))
    f.read(1)
    A1_confirmed = config.hex2Dec(f.read(8))
    A2 = f.read()
    f.close()

    A1_unconfirmed = str(config.dec2Hex(A1_unconfirmed + transAmount))
    A1_confirmed = str(config.dec2Hex(A1_confirmed + transAmount))

    f = open('BalanceA.txt', 'w')
    f.write(A1 + A1_unconfirmed+ ':' + A1_confirmed + A2)
    f.close()
  else:
    f = open('BalanceA.txt', 'r')
    A1 = f.readline()
    A2Name = f.read(9)
    A2_unconfirmed= config.hex2Dec(f.read(8))
    f.read(1)
    A2_confirmed = config.hex2Dec(f.read(8))
    
    A2_unconfirmed = str(config.dec2Hex(A2_unconfirmed + transAmount))
    A2_confirmed = str(config.dec2Hex(A2_confirmed+ transAmount))

    f = open('BalanceA.txt', 'w')
    f.write(A1 + A2Name + A2_unconfirmed + ':' + A2_confirmed)
    f.close()


def updateUncalculated(transAmount,PayerAccount):
  f = open('BalanceA.txt','r')
  if(PayerAccount == '1'):
    A1 = f.read(18)
    A1_conf = config.hex2Dec(f.read(8))
    A2 = f.read()
    f.close()

    tmp = str(config.dec2Hex(A1_conf - transAmount))

    f = open('BalanceA.txt', 'w')
    f.write(A1 + tmp + A2)
    f.close()
    
  else:
    A1 = f.readline()
    A2 = f.read(18)
    A2_conf = config.hex2Dec(f.read(8))
    f.close()

    tmp = str(config.dec2Hex(A2_conf - transAmount))

    f = open('BalanceA.txt', 'w')
    f.write(A1 + A2 + tmp)
    f.close()

    

print("The server is ready to receive")

while 1:
  message, requesterAddress = serverSocket.recvfrom(2048)
  print("Full Node connected")
  message = message.decode()
  Payer = message[0:8]
  Payee = message[8:16]
  TAamount = message[16:24]

  if Payer[0] == 'A':
    f = open('Unconfirmed_TA.txt', 'r')
    validTx = False
    for x in range(4):
      tmp = f.read(24)
      if(tmp == message):
        print("*change valid transaction to true*")
        validTx = True
        break
      elif(tmp == '\n'):
        break
      else:
        f.read(1)
    f.close()

    if Payer == 'A0000001':
      updateUncalculated(config.hex2Dec(TAamount) + TxFee, '1')
    else:
      updateUncalculated(config.hex2Dec(TAamount) + TxFee, '2')
    
    if(validTx == True):
      f = open('Unconfirmed_TA.txt', 'r')
      content = f.readlines()
      f.close()
      f = open('Unconfirmed_TA.txt', 'w')
      flag = False
      for line in content:
        if(line.strip('\n') == message and flag == False):
          flag = True
        else:
          f.write(line)
      f.close()
    else:
      print("Error: invalid Tx occurred")
    f = open('Confirmed_TA.txt', 'a')
    f.write(message + '\n')
    f.close()
  else:
    if Payee == 'A0000001':
      BothBalanceUpdate(config.hex2Dec(TAamount), '1')
    else:
      BothBalanceUpdate(config.hex2Dec(TAamount), '2')
    f = open('Confirmed_TA.txt', 'a')
    f.write(message + '\n')
    f.close()


