import blockchain
import config
from socket import *



serverName = 'localhost'
serverPort = 10000
clientSocket = socket(AF_INET, SOCK_DGRAM)


def updateBalance(transAmount,payerAccount):
  f = open('BalanceA.txt','r')
  if(payerAccount == '1'):
    A1 = f.read(9)
    A1_unconfirmed = config.hex2Dec(f.read(8))
    A1_confirmed = f.read(9)
    A2 = f.read()
    f.close()

    tmp = str(config.dec2Hex(A1_unconfirmed - transAmount))

    f = open('BalanceA.txt', 'w')
    f.write(A1 + tmp + A1_confirmed + A2)
    f.close()
    
  else:
    A1 = f.readline()
    A2 = f.read(9)
    A2_unconfirmed = config.hex2Dec(f.read(8))
    A2_confirmed = f.read(9)
    f.close()


    tmp = str(config.dec2Hex(A2_unconfirmed - transAmount))

    f = open('BalanceA.txt', 'w')
    f.write(A1 + A2 + tmp + A2_confirmed)
    f.close()


def DisplayUnconfirmed():
  f = open('Unconfirmed_TA.txt', 'r')
  for line in f:
    if line != '\n':
      payer = line[0:8]
      payee = line[8:16]
      tAmount = line[16:24]
      print('Tx: ' + payer + ' paying ' + payee + ' the amount of ' + tAmount + ' BTC.')
  f.close()

def DisplayConfirmed():
  f = open('Confirmed_TA.txt', 'r')
  for line in f:
    if line != '\n':
      payer = line[0:8]
      payee = line[8:16]
      tAmount = line[16:24]
      print('Tx: ' + payer + ' paying ' + payee + ' the amount of ' + tAmount + ' BTC.')
  f.close()



def DisplayBalance():
  indent =  '\t\t\t'
  
  f = open('BalanceA.txt','r')
  f.read(9)
  A1_unconfirmed = config.hex2Dec(f.read(8))
  f.read(1)
  A1_confirmed = config.hex2Dec(f.read(8))
  f.read(10)
  A2_unconfirmed = config.hex2Dec(f.read(8))
  f.read(1)
  A2_confirmed = config.hex2Dec(f.read(8))
  f.close()
  print('\tUnconfirmed\tConfirmed')
  print('A1:\t' + str(A1_unconfirmed) + indent + str(A1_confirmed))
  print('A2:\t' + str(A2_unconfirmed) + indent + str(A2_confirmed))



global Tx_Fee
Tx_N = 0
Tx_Fee = 2

def NewTransaction(): 
  global Tx_N
  Tx_N = Tx_N + 1

  print("Select a Payer")
  print("Payer 1: A0000001")
  print("Payer 2: A0000002")
  payer = input(">")
  while(payer != "1" and payer != "2"):
    print('**Error** inputs selection --> 1 & 2')
    print("Choose a Payer")
    print("Payer 1: A0000001")
    print("Payer 2: A0000002")
    payer = input('>')

  print("Select a Payee:")
  print("Payer 1: B0000001")
  print("Payer 2: B0000002")
  payee = input(">")
  while(payee != "1" and payee != "2"):
    print("**Error** input selection --> 1 & 2")
    print("Choose a Payee:")
    print("Payer 1: B0000001")
    print("Payer 2: B0000002")
    payee = input('>')
  payee = 'B000000' + payee

  transaction_Amount = int(input("Enter Transaction Amount:"))

  with open('BalanceA.txt') as f:
     if (payer == '2'):
      f.readline()
     payerHex = f.read(8)
     f.read(1)
     balance = f.read(8)
     f.close()
  balance = config.hex2Dec(balance)

  if balance < transaction_Amount + Tx_Fee:
    print("Insufficient Funds!")
  else:
    tFile = open('Unconfirmed_TA.txt','a')
    tFile.write(payerHex + payee + config.dec2Hex(transaction_Amount) + '\n')
    updateBalance(transaction_Amount + Tx_Fee, payer)
    
    Transaction = (payerHex + payee + config.dec2Hex(transaction_Amount))
    clientSocket.sendto(Transaction.encode(),(serverName,serverPort))   


def userInput():
  print("Please select a choice:")
  print("1. Enter a new Tx.")
  print("2. Print current balance for each Accounts.")
  print("3. Print unconfirmed transactions.")
  print("4. Print confirmed transactions.")
  print("5. EXIT.")


while 1:
  userInput()
  cin = input(">")
  if(cin == '1'):
    NewTransaction()
  elif(cin == '2'):
    DisplayBalance()
  elif(cin == '3'):
    DisplayUnconfirmed()
  elif(cin == '4'):
    DisplayConfirmed()
  elif(cin == '5'):
    break
  else:
    print("**ERROR INVALID INPUT**")

clientSocket.close()