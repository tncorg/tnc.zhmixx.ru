import socket
import threading
import sys

HOST = '127.0.0.1'
PORT = 5000

nickname = input("enter your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def receive():
    while True:
        try:
            message = client.recv(1024).decode()
            if not message:
                break
            print(f"\r{message}\n> ", end='', flush=True)
        except:
            print("\n disconnected from server.")
            client.close()
            break

def write():
    while True:
        msg = input("> ")
        if msg.strip() == "/quit":
            client.send("/quit".encode())
            print("exiting chat.")
            client.close()
            sys.exit()
        client.send(msg.encode())

def main():
    try:
        if client.recv(1024).decode() == "NICK":
            client.send(nickname.encode())

        threading.Thread(target=receive, daemon=True).start()
        write()
    except KeyboardInterrupt:
        print("\nexiting...")
        client.send("/quit".encode())
        client.close()

main()
