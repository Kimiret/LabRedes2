import socket
import os
import time

#Importante cambiar esta direccion base para acceder a los directorios correctos
archivo_src = '/home/juanjo/Escritorio/Projects/LabRedes2/'

host, port = 'localhost', 8888


#Creacion del socket de servidor con host y port ya definidos, se quedara escuchando a conexiones
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind((host, port))
serversocket.listen(1)

while True:
    client_connect, client_addr = serversocket.accept()
    request = client_connect.recv(1024).decode('utf-8')
    print(request) #ver todos los datos que se obtienen de la request
    string_list = request.split(' ')
    method = string_list[0]
    request = string_list[1]
    version = string_list[2]
    #print(version)

    #Este if maneja el escenario de una version HTTP distinta a 1.1
    if(version.find('1.1') == -1):
        header = 'HTTP/1.1 505 HTTP Version Not Supported'
        response = '<html><body>Error 505: HTTP Version not supported</body></html>'
        mimetype = 'text/html'
        header += 'Content-Type: ' + mimetype + '\r\n'

    #En caso de recibir una request de un metodo distinto a GET
    elif(method != 'GET'):
        header = 'HTTP/1.1 405 Method Not Allowed\n'
        response = '<html><body>Error 405: Method Not Allowed</body></html>'.encode('utf-8')
        mimetype = 'text/html'
        header += 'Content-Type: ' + mimetype + '\n\n'

    #Si la url recibida no empieza con /
    elif(request.find('/') != 0):
        header = 'HTTP/1.1 400 Bad Request\n'
        response = '<html><body>Error 400: Bad Request</body></html>'.encode('utf-8')
        mimetype = 'text/html'
        header += 'Content-Type: ' + mimetype + '\n\n'
    
    #Esta cosa por algun motivo solo sirve en Firefox, es la redireccion
    elif(request.endswith('Files') or request.endswith('Images')):
        print('redirigiendo...\n')
        header = 'HTTP/1.1 301 Moved Permanently\n'
        header += f'Location: http://localhost:{port}{request}/\n'
        response = '<html><body>Error 301: Moved Permanently</body></html>'.encode('utf-8')
        mimetype = 'text/html'
        header += 'Content-Type: ' + mimetype + '\n\n'
    else:
        archivo = request.split('?')[0]
        archivo_final = archivo_src
        archivo_final += archivo

        
        #Si la url termina en /, se asume que hay un index.html en esa direccion
        if(archivo.endswith('/')):
            archivo_final += 'index.html'

        header = 'HTTP/1.1 200 OK\n'
            
        try: 
            archivo_size = os.path.getsize(archivo_final)
            #Al encontrar un archivo, se lee y determina su mimetype
            with open(archivo_final, 'rb') as file:
                response = file.read()
            
            if archivo_final.endswith('.html'):
                mimetype = 'text/html'
            elif archivo_final.endswith('.css'):
                mimetype = 'text/css'
            elif archivo_final.endswith('.js'):
                mimetype = 'application/javascript'
            elif archivo_final.endswith('.png'):
                mimetype = 'image/png'
            elif archivo_final.endswith('.jpeg') or archivo_final.endswith('.jpg'):
                mimetype = 'image/jpeg'
            else:
                mimetype = 'application/octet-stream'

            #Luego se añade informacion extra del archivo al header
            header += 'Content-Type: '+str(mimetype)+'\n' + 'Content-Length: '+str(len(response))+'\n\n'
            #print(header)
            
        except FileNotFoundError:
            header = 'HTTP/1.1 404 Not Found\n'
            response = '<html><body>Error 404: File not found</body></html>'.encode('utf-8')
            mimetype = 'text/html'
            header += 'Content-Type: ' + mimetype + '\n\n'

    respuesta = header.encode('utf-8')
    respuesta += response
    client_connect.send(respuesta)
    client_connect.close()
