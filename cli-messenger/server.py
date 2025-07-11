import socket
import threading

HOST = '127.0.0.1'
PORT = 5000

clients = []
nicknames = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

def broadcast(message, sender=None):
    for client in clients:
        if client != sender:
            try:
                client.send(message.encode())
            except:
                pass

def handle(client):
    index = clients.index(client)
    nickname = nicknames[index]

    while True:
        try:
            message = client.recv(1024).decode()
            if message.strip() == "/quit":
                client.send("you have left the chat.".encode())
                client.close()
                clients.remove(client)
                nicknames.remove(nickname)
                broadcast(f"{nickname} has left the chat.")
                break
            else:
                broadcast(f"{nickname}: {message}", sender=client)
        except:
            break

def accept_connections():
    print(f"server listening on {HOST}:{PORT}")
    while True:
        client, _ = server.accept()
        client.send("NICK".encode())
        nickname = client.recv(1024).decode()
        nicknames.append(nickname)
        clients.append(client)
        print(f"{nickname} joined.")
        broadcast(f"{nickname} has joined the chat.")

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

def server_input():
    while True:
        msg = input()
        broadcast(f"[SERVER]: {msg}")

threading.Thread(target=accept_connections).start()
threading.Thread(target=server_input).start()
