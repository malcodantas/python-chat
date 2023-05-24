"""Main Class."""
import socket
import threading

import rsa

PORT = 9995
public_key, private_key = rsa.newkeys(1024)

try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", PORT))
    public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
    client.send(public_key.save_pkcs1("PEM"))
    client_name = input("Qual seu Nome? ")
except ConnectionError:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", PORT))
    server_name = input("Qual seu Nome? ")
    server.listen()
    client, _ = server.accept()
    client.send(public_key.save_pkcs1("PEM"))
    public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))


def send_message_handler(c):
    while True:
        message = input("")
        c.send(rsa.encrypt(message.encode(), public_partner))
        print("You: " + message)


def receive_message_handler(c):
    while True:
        print("Other: ", rsa.decrypt(c.recv(1024), private_key).decode())


threading.Thread(target=send_message_handler, args=(client,)).start()
threading.Thread(target=receive_message_handler, args=(client,)).start()
