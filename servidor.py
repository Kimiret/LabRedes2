import socket


host, port = 'localhost', 8888

#Creacion del socket de servidor con host y port ya definidos, se quedara escuchando a conexiones
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind((host, port))
serversocket.listen(1)

while True:
    client_connect, client_addr = serversocket.accept()
    request = client_connect.recv(1024).decode('utf-8')
    #print(request) #ver todos los datos que se obtienen de la request
    string_list = request.split(' ')
    method = string_list[0]
    request = string_list[1]
    version = string_list[2]
    print(version)
    print(version.find('1.1'))

    if(version.find('1.1') == -1):
        header = 'HTTP/1.1 505 HTTP Version Not Supported'
        response = '<html><body>Error 505: HTTP Version not supported</body></html>'.encode('utf-8')
    else:
        if(method != 'GET'):
            header = 'HTTP/1.1 405 Method Not Allowed\n'
            response = '<html><body>Error 405: Method Not Allowed</body></html>'.encode('utf-8')
        else:
            #print('Se solicita ',request) 

            archivo = request.split('?')[0]
            if(archivo.endswith('/')):
                archivo = 'index.html'
            elif(archivo.endswith('index.html')):
                archivo = 'index.html'

            header = 'HTTP/1.1 200 OK\n'
            
            try: 
                with open(archivo, 'rb') as file:
                    response = file.read()
                

                if archivo.endswith('.html'):
                    mimetype = 'text/html'
                elif archivo.endswith('.css'):
                    mimetype = 'text/css'
                elif archivo.endswith('.js'):
                    mimetype = 'application/javascript'
                elif archivo.endswith('.png'):
                    mimetype = 'image/png'
                elif archivo.endswith('.jpeg') or archivo.endswith('.jpg'):
                    mimetype = 'image/jpeg'
                else:
                    mimetype = 'application/octet-stream'
                header += 'Content-Type: '+str(mimetype)+'\n\n'
            
            except FileNotFoundError:
                header = 'HTTP/1.1 404 Not Found\n'
                response = '<html><body>Error 404: File not found</body></html>'.encode('utf-8')

    respuesta = header.encode('utf-8')
    respuesta += response
    client_connect.send(respuesta)
    client_connect.close()
