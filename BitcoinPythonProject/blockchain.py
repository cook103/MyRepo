import hashlib
import config

def merkleRoot(A,B,C,D):
  m = hashlib.sha256()
  m.update(A.encode("utf-8"))
  A = m.hexdigest()
  m.update(B.encode("utf-8"))
  B = m.hexdigest()
  m.update(C.encode("utf-8"))
  C = m.hexdigest()
  m.update(D.encode("utf-8"))
  D = m.hexdigest()
  m.update(A.encode("utf-8") + B.encode("utf-8"))
  Tx12 = m.hexdigest()
  m.update(C.encode("utf-8") + D.encode("utf-8"))
  Tx34 = m.hexdigest()
  m.update(Tx12.encode("utf-8") + Tx34.encode("utf-8"))
  return m.hexdigest()

block_count = 0 

def FindNonce(A,B,C,D):
  global block_count
  hashHandler = hashlib.sha256()
  nonce = 0
  hashValue = ''

  while True:
    if block_count == 0:
      prevHash = "0000000000000000000000000000000000000000000000000000000000000000" 
    else:
      prevHash = hashValue 
    tmp = config.dec2Hex(nonce)
    while(len(tmp) != 8):
      tmp = '0' + tmp
    block_header = tmp + prevHash.upper() + merkleRoot(A,B,C,D).upper()
    hashHandler.update(block_header.encode("utf-8"))
    hashValue = hashHandler.hexdigest()
    nonceFound = True
    for i in range(4):
      if hashValue[i]!='0':
        nonceFound = False
        break
    if nonceFound:
      break
    nonce += 1
  
  block_count = block_count + 1
  return block_header

def last_hash():
  nonce = 0
  last = FindNonce()
  block = str(nonce) + last + merkle_root()
  print(block.upper())
  return block.upper()

def UpdatingBlockchain():
  f = open('Temp_T.txt', 'r')
  A = f.readline(24)
  f.read(1)
  B = f.readline(24)
  f.read(1)
  C = f.readline(24)
  f.read(1)
  D = f.readline(24)
  f.close()

  f = open('Temp_T.txt', 'w')
  f.write('')
  f.close()

  header = FindNonce(A,B,C,D)
  block = header + A + B + C + D 
  return block.upper()


