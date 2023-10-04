import socket, sys
IP = socket.gethostbyname(socket.gethostname())
PORT = 4467
ADDR = (IP, PORT)
SIZE = 2048
FORMAT = "utf-8"

def main():
    print("[STARTING] Server is starting.")
    #Starting tcp socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Binds the IP and PORT to the server
    server.bind(ADDR)

    #Server is listening or waiting for a client to conenct
    server.listen()
    print("[LISTENING] Server is listening.")
    while True:
        #Server accepts connection from client
        conn, addr = server.accept()
        print(f"[NEW CONNECTION] {addr} connected.")
            
        #Receiving the filename
        filename = conn.recv(SIZE).decode(FORMAT)
        print(f"[RECV] Receiving the filename.")
        file = open("New_" + filename, "wb")
        conn.send("Filename received.".encode(FORMAT))

        #Receiving the file data
        data = conn.recv(SIZE)
        print(f"[RECV] Receiving the file data.")
        while data:
            file.write(data)
            data = conn.recv(SIZE)

        file.close()
        conn.close()
        print(f"[DISCONNECTED] {addr} disconnected.")

if __name__ == "__main__":
    main()
