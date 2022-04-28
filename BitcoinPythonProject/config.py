#setting turn = 0 
turn = 0

def hex2Dec(n):
  table = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15}

  decimal = 0
  power = len(n) - 1
  for digit in n:
    decimal += table[digit] * 16 ** power
    power -= 1
  decimal = int(decimal)
  return decimal

def dec2Hex(n):
  if n > 0:
    x = ''
    while n != 0:
      r = n%16
      n = int(n/16)
      if(r == 10):
        r = 'A'
      elif(r == 11):
        r = 'B'
      elif(r == 12):
        r = 'C'
      elif(r == 13):
        r = 'D'
      elif(r == 14):
        r = 'E'
      elif(r == 15):
        r = 'F'
      x = str(r) + x
    while len(x) < 8:
      x = '0' + x
    return x

  elif n == 0:
    return '00000000'

  else:
    print("**Error**")

