from socket import *
import base64
def createServer():
    serversocket = socket(AF_INET, SOCK_STREAM)
    try :
        serversocket.bind(('localhost',9000))
        serversocket.listen(5)
        while(1):
            (clientsocket, address) = serversocket.accept()

            rd = clientsocket.recv(5000).decode()
            pieces = rd.split("\n")
            if ( len(pieces) > 0) : print(pieces)

            ###################################################

            if ( len(pieces) >17 ) :
                
                info = pieces[18]   #string chứa thông tin username and pass
                pieces = info.split("&")

                usernameStr = pieces[0]
                usernameStr=usernameStr.split("=")
                usernameStr=usernameStr[1]  #username

                passwordStr = pieces[1]
                passwordStr=passwordStr.split("=")
                passwordStr=passwordStr[1]  #password

                if (usernameStr == "admin" and passwordStr == "admin") :
                    print("OK")
                    while (pieces[0] != "GET /info.html HTTP/1.1\r") :
                        
                        (clientsocket, address) = serversocket.accept()  
                        rd = clientsocket.recv(5000).decode()
                        pieces = rd.split("\n")

                        #redirect to info.html
                        
                        data = "HTTP/1.1 301 Moved Permanently\r\n"
                        data += "Location: http://localhost:9000/info.html\r\n"

                        clientsocket.sendall(data.encode())
                        clientsocket.shutdown(SHUT_WR)


                    while (1):
                        (clientsocket, address) = serversocket.accept()  
                        rd = clientsocket.recv(5000).decode()
                        pieces=rd.split('\n')
                        data = "HTTP/1.1 200 OK\r\n"
                        data += "Content-Type: text/html; charset=utf-8\r\n"
                        data += "\r\n"

                        filename = 'info.html'
                        f = open(filename, 'r', encoding="utf8")
                        content = "" + f.read() + ""

                        #đọc file ảnh
                        with open("NL.jpeg", "rb") as imgFile:
                            image = base64.b64encode(imgFile.read())
                            image = image.decode('utf-8')

                        content = content.replace("NL.jpeg", "data:image/jpeg;base64," + image)

                        with open("TL.jpeg", "rb") as imgFile:
                            image = base64.b64encode(imgFile.read())
                            image = image.decode('utf-8')

                        content = content.replace("TL.jpeg", "data:image/jpeg;base64," + image)
                        
                        data += content

                        clientsocket.sendall(data.encode())
                        clientsocket.shutdown(SHUT_WR)

                else:
                    while (pieces[0] != "GET /404.html HTTP/1.1\r") :
                        
                        (clientsocket, address) = serversocket.accept()  
                        rd = clientsocket.recv(5000).decode()
                        pieces = rd.split("\n")

                        #redirect to 404.html
                        
                        data = "HTTP/1.1 301 Moved Permanently\r\n"
                        data += "Location: http://localhost:9000/404.html\r\n"

                        clientsocket.sendall(data.encode())
                        clientsocket.shutdown(SHUT_WR)


                    while (1):
                        (clientsocket, address) = serversocket.accept()  
                        rd = clientsocket.recv(5000)
                        
                        data = "HTTP/1.1 404 Not Found\r\n"
                        data += "Content-Type: text/html; charset=utf-8\r\n"
                        data += "\r\n"

                        filename = '404.html'
                        f = open(filename, 'r')
                        content = "" + f.read() + ""

                        data += content

                        
                        clientsocket.sendall(data.encode())
                        clientsocket.shutdown(SHUT_WR)


#form login
            data = "HTTP/1.1 200 OK\r\n"
            data += "Content-Type: text/html; charset=utf-8\r\n"
            data += "\r\n"

            filename = 'index.html'
            f = open(filename, 'r') #iso-8859-1
            content = "" + f.read() + ""

            data += content
            clientsocket.sendall(data.encode())
            clientsocket.shutdown(SHUT_WR)
   

    except KeyboardInterrupt :
        print("\nShutting down...\n");
    except Exception as exc :
        print("Error:\n");
        print(exc)

    serversocket.close()

print('Access http://localhost:9000/index.html')
createServer()