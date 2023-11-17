import socket
import threading

host = "127.0.0.1"
port = 6969
server = socket.socket()
connected = False
conn= "\n   ____                            _           _   _                                       \n  / ___|___  _ __  _ __   ___  ___| |_ ___  __| | | |_ ___    ___  ___ _ ____   _____ _ __ \n | |   / _ \| '_ \| '_ \ / _ \/ __| __/ _ \/ _` | | __/ _ \  / __|/ _ \ '__\ \ / / _ \ '__|\n | |__| (_) | | | | | | |  __/ (__| ||  __/ (_| | | || (_) | \__ \  __/ |   \ V /  __/ |   \n  \____\___/|_| |_|_| |_|\___|\___|\__\___|\__,_|  \__\___/  |___/\___|_|    \_/ \___|_|   "
text_server_stop= "\n                                 _           _                    _             \n  ___  ___ _ ____   _____ _ __  (_)___   ___| |_ ___  _ __  _ __ (_)_ __   __ _ \n / __|/ _ \ '__\ \ / / _ \ '__| | / __| / __| __/ _ \| '_ \| '_ \| | '_ \ / _` |\n \__ \  __/ |   \ V /  __/ |    | \__ \ \__ \ || (_) | |_) | |_) | | | | | (_| |\n |___/\___|_|    \_/ \___|_|    |_|___/ |___/\__\___/| .__/| .__/|_|_| |_|\__, |\n                                                     |_|   |_|            |___/\n"
bye =  "  _                \n | |__  _   _  ___ \n | '_ \| | | |/ _ \ \n | |_) | |_| |  __/\n |_.__/ \__, |\___|\n        |___/     \n"





def send(server):
    global connected
    first_connection = True
    while connected:
        if first_connection:
            message = input("enter you Pseudo: ")
            message = "/\/P$eudo/\/"+message
            try:
                server.send(message.encode())

            except ConnectionAbortedError:
                print("No server connected")
                connected = False

            except ConnectionResetError:
                print("Server has stopped")
                connected = False

            else:
                if message == "bye":
                    print("You can't disconnect you havent give the server a pseudo")
                    
                elif message == "arret":
                    print("you have no write to disconnet the server")
                    
                else:
                    first_connection = False
        else:
            message = input("")
            try:
                server.send(message.encode())

            except ConnectionAbortedError:
                print("No server connected")
                connected = False

            except ConnectionResetError:
                print("Server has stopped")
                connected = False

            else:
                if message == "bye":
                    print(bye)
                    server.send(message.encode())
                    connected = False
                if message == "arret":
                    print("you've requested to stop the server")
                    server.send(message.encode())
                    message = server.recv(1024).decode() #attente de confirmation
                    connected = False

    server.close()


    



try:
    server.connect((host, port))
except ConnectionRefusedError:
    print("404 Server not online")
else:
    envoi = threading.Thread(target=send, args=[server])
    print(conn)
    connected = True
    envoi.start()
    while connected:
        try:
            message = server.recv(1024).decode()
        except ConnectionResetError:
            print("server forcibly disconnected")
            connected = False
        except ConnectionAbortedError:
            print("server forcibly disconnected")
            connected = False
        else:
            if message == text_server_stop:
                connected = False
            """if message == "server is shutting down, you all will be disconnected":
                print(message)
                server.close()
                connected = False
            else:"""
            print(message)

    envoi.join()
    server.close()
        
