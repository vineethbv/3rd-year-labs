import socket


def xor(a, b):
    result = []

    for i in range(1, len(b)):
        if a[i] == b[i]:
            result.append('0')
        else:
            result.append('1')

    return ''.join(result)


# Performs Modulo-2 division
def mod2div(divident, divisor):
    pick = len(divisor)

    tmp = divident[0: pick]

    while pick < len(divident):

        if tmp[0] == '1':
            tmp = xor(divisor, tmp) + divident[pick]
        else:  
            tmp = xor('0'*pick, tmp) + divident[pick]

        pick += 1

    if tmp[0] == '1':
        tmp = xor(divisor, tmp)
    else:
        tmp = xor('0'*pick, tmp)

    checkword = tmp
    return checkword

# Function used at the receiver side to decode
# data received by sender
def decodeData(data, key):

    l_key = len(key)

    # Appends n-1 zeroes at end of data
    appended_data = data.decode() + '0'*(l_key-1)
    remainder = mod2div(appended_data, key)

    return remainder


# Creating Socket
s = socket.socket()
print("Socket successfully created")

# reserve a port on your computer in our
# case it is 12345 but it can be anything
port = 12345

s.bind(('', port))
print("socket binded to %s" % (port))
# put the socket into listening mode
s.listen(5)
print("socket is listening")


while True:
    # Establish connection with client.
    c, addr = s.accept()
    print('Got connection from', addr)

    # Get data from client
    data = c.recv(1024)

    print("Received encoded data in binary format :", data.decode())

    if not data:
        break

    key = "1001"

    ans = decodeData(data, key)
    print("Remainder after decoding is->"+ans)

    # If remainder is all zeros then no error occured
    temp = "0" * (len(key) - 1)
    if ans == temp:
        c.sendto(("THANK you Data ->"+data.decode() +
                  " Received No error FOUND").encode(), ('127.0.0.1', 12345))
    else:
        c.sendto(("Error in data").encode(), ('127.0.0.1', 12345))

    c.close()
