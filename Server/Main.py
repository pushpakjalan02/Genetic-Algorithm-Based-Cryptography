import socket
import Decrypt

def createSocket():

    print()
    ip = input('Enter IP Address: ')
    port = int(input('Enter Port: '))
    print()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Created Socket Successfully\n')

    s.bind((ip, port))
    print('Binding done to port ' + str(port) + '\n')

    s.listen(5)
    print('Started listening\n')

    return s

def main():
    s = createSocket()
    while(True):
        c, addr = s.accept()
        print('Connection established with ' + str(addr) + '\n')

        cipherText = c.recv(1024).decode('utf-8')
        print('Received data: ' + cipherText + '\n')

        key = input('Enter Decryption Key: ')
        print()

        decryptedData = Decrypt.decrypt(cipherText, key)
        print('Done decrypting\n')
        
        print('Decrypted data: ' + decryptedData + '\n')

        c.close()
        print('Connection closed\n')

    return

if __name__ == "__main__":
    main()
