import blockchain
import config

from socket import *
serverName = 'localhost'
serverPort = 20000
clientSocket = socket(AF_INET, SOCK_DGRAM)


def updateBalance(transAmount,payerAccount):
  f = open('BalanceB.txt','r')
  if(payerAccount == '1'):
    B1 = f.read(9)
    B1_unconfirmed = config.hex2Dec(f.read(8))
    B1_confirmed = f.read(9)
    B2 = f.read()
    f.close()
    tmp = str(config.dec2Hex(B1_unconfirmed - transAmount))

    f = open('BalanceB.txt', 'w')
    f.write(B1 + tmp + B1_confirmed + B2)
    f.close()
  else:
    B1 = f.readline()
    B2 = f.read(9)
    B2_unconfirmed = config.hex2Dec(f.read(8))
    B2_confirmed = f.read(9)
    f.close()
    tmp = str(config.dec2Hex(B2_unconfirmed - transAmount))

    f = open('BalanceB.txt', 'w')
    f.write(B1 + B2 + tmp + B2_confirmed)
    f.close()

def DisplayUnconfirmed():
  f = open('Unconfirmed_TB.txt', 'r')
  for line in f:
    if line != '\n':
      Payer = line[0:8]
      Payee = line[8:16]
      tAmount = line[16:24]
      print('Tx: ' + Payer + ' paying ' + Payee + ' the amount of ' + tAmount + ' BTC.')
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
  f = open('BalanceB.txt','r')
  f.read(9)
  B1_unconfirmed = config.hex2Dec(f.read(8))
  f.read(1)
  B1_confirmed = config.hex2Dec(f.read(8))
  f.read(10)
  B2_unconfirmed = config.hex2Dec(f.read(8))
  f.read(1)
  B2_confirmed = config.hex2Dec(f.read(8))
  f.close()
  print('\tUnconfirmed\tConfirmed')
  print('B1:\t' + str(B1_unconfirmed) + indent + str(B1_confirmed))
  print('B2:\t' + str(B2_unconfirmed) + indent + str(B2_confirmed))

Tx_N = 0
global Tx_Fee
Tx_Fee = 2

def NewTransaction(): 
  global Tx_N
  Tx_N = Tx_N + 1

  print("Select a Payer")
  print("Payer 1: B0000001")
  print("Payer 2: B0000002")
  Payer = input(">")
  while(Payer != "1" and Payer != "2"):
    print('**Error** inputs selection --> 1 & 2')
    print("Select a Payer")
    print("Payer 1: B0000001")
    print("Payer 2: B0000002")
    Payer = input('>')

  print("Select a Payee:")
  print("Payer 1: A0000001")
  print("Payer 2: A0000002")
  Payee = input(">")
  while(Payee != "1" and Payee != "2"):
    print('**Error** inputs selection --> 1 & 2')
    print("Select a Payee:")
    print("Payer 1: A0000001")
    print("Payer 2: A0000002")
    Payee = input('>')
  Payee = 'A000000' + Payee

  tAmount = int(input("Enter Transaction Amount:"))

  with open('BalanceB.txt') as f:
     if (Payer == '2'):
      f.readline()

     PayerHex = f.read(8)
     f.read(1)
     balance = f.read(8)
    
     f.close()

  balance = config.hex2Dec(balance)

  if balance < tAmount:
    print("Insufficient Funds")
  else:
    tFile = open('Unconfirmed_TB.txt','a')
    tFile.write(PayerHex + Payee + config.dec2Hex(tAmount) + '\n')
    updateBalance(tAmount + Tx_Fee,Payer)
    
    Transaction = (PayerHex + Payee + config.dec2Hex(tAmount))
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