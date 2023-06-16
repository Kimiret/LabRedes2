import socket


host, port = 'localhost', 8888

#Creacion delsocket de servidor con host y port ya definidos, se quedara escuchando a conexiones
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind((host, port))
serversocket.listen(1)

while True:
    client_connect, client_addr = serversocket.accept()
    request = client_connect.recv(1024).decode('utf-8')
    string_list = request.split(' ')
    method = string_list[0]
    request = string_list[1]


    print('Se solicita ',request) 

    archivo = request.split('?')[0]
    if(archivo == '/'):
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
