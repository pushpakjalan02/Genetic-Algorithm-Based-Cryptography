import socket
import Encrypt

def sendData(cipherText, key):

    ip = input('Enter Server IP Address: ')
    port = int(input('Enter Server Port: '))
    print()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Created socket successfully\n')

    s.connect((ip, port))
    print('Connection to server established\n' + 
        'Server IP Address: ' + ip + '\n' + 
        'Server Port: ' + str(port) + '\n')

    s.sendall(cipherText.encode('utf-8'))
    print('Sent Data: ' + cipherText)
    print('Decryption key: ' + key + '\n')

    s.close()
    print('Connection closed\n')

    return

def main():

    print()
    plainText = input('Enter data to send: ')
    print()

    cipherText, key = Encrypt.encrypt(plainText)
    print('Done encrypting\n')

    sendData(cipherText, key)

    return

if __name__ == "__main__":
    main()
