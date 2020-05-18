import socket
import os
import urllib
import subprocess
import json
import time
import sqlite3
import random
# WWWROOT="c:\\wwwroot\\"
WWWROOT = "..\\wwwroot\\"
answers=[]
conn = sqlite3.connect('GAME200.db')
num = random.randrange(0, 2)
cursor = conn.execute("SELECT * from GAME")
rows = cursor.fetchall()
theRow = rows[num]
q = theRow[0]
ans = theRow[1]
ans=ans.split(":")
 
def InternalServerError():
    msg = "HTTP/1.1 500 InternalServerError\r\n"
    data = "<h1>we dont understant what you want from us! </h1>"
    data = data + "<h1><marquee>500</marquee></h1>"
    msg = msg + "Content-Length:" + str(len(data)) + "\r\n"
    msg = msg + "\r\n" + data
    return msg


def Redirect():
    msg = "HTTP/1.1 302 Redirect\r\n"
    data = "<h1>what you are looking for is not here, sorry hunny </h1>"
    data = data + "<h1><marquee>302</marquee></h1>"
    msg = msg + "Content-Length:" + str(len(data)) + "\r\n"
    msg = msg+"location: 127.0.0.1/page2.html\r\n"
    print (msg)
    msg = msg + "\r\n" + data
    return msg


def notFound():
    msg = "HTTP/1.1 404 Not Found\r\n"
    data = "<h1>We did not found what you are looking for</h1>"
    data = data + "<h1><marquee>404</marquee></h1>"
    msg = msg + "Content-Length:" + str(len(data)) + "\r\n"
    msg = msg + "\r\n" + data
    return msg


def Forbidden():
    msg = "HTTP/1.1 403 Forbidden\r\n"
    data = "<h1>You cant enter to this</h1>"
    data = data + "<h1><marquee>403</marquee></h1>"
    msg = msg + "Content-Length:" + str(len(data)) + "\r\n"
    msg = msg + "\r\n" + data
    return msg
def answer_is_correct(ansy):
    msg = "HTTP/1.1 200 OK\r\n"
    data = "<h1>Your answer "+ansy+" is correct</h1>"
    with open(WWWROOT + "gamePage.html", mode='rb') as file:
        fileContent = file.read()
        fileContent=fileContent.decode()
        msg = "HTTP/1.1 200 OK\r\n"
        msg = msg + "Content-Length:" + str(len(fileContent)+len(data)) + "\r\n"
        msg = msg + "\r\n" + fileContent+data
		
    global answers
    answers.append(ansy)
    return msg
def answer_is_incorrect(ansy):
    global q
    msg = "HTTP/1.1 200 OK\r\n"
    data = "<br><h1>Your answer"+ansy+" is incorrect</h1><br>"
    data=data+"<h2> your qustion is: "+q+"<h2>"
    with open(WWWROOT + "gamePage.html", mode='rb') as file:
        fileContent = file.read()
        fileContent=fileContent.decode()
        msg = "HTTP/1.1 200 OK\r\n"
        msg = msg + "Content-Length:" + str(len(fileContent)+len(data)) + "\r\n"
        msg = msg + "\r\n" + fileContent+data
		
    global answers
    answers.append(ansy)
    return msg

def its_a_tye():
    msg = "HTTP/1.1 200 OK\r\n"
    data = "<br><h1> no more correct answers</h1><br>"
    with open(WWWROOT + "endPageTye.html", mode='rb') as file:
        fileContent = file.read()
        fileContent=fileContent.decode()
        msg = "HTTP/1.1 200 OK\r\n"
        msg = msg + "Content-Length:" + str(len(fileContent)+len(data)) + "\r\n"
        msg = msg + "\r\n" + fileContent+data
    return msg


def main():
    print ("start server")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    server_socket.bind(("127.0.0.1", 80))
    server_socket.listen(5)
    (client_socket, client_address) = server_socket.accept()
    print ("client connect")

    while (1):
        client_info = client_socket.recv(1024)
        if client_info.decode() == "":
            print (">>>>close connection and wait for new connection")
            client_socket.close()
            (client_socket, client_address) = server_socket.accept()  # wait for a new connection
        print ("\n\n++++++++++++++++++++++")
        print ("client_info", client_info)
        client_info=client_info.decode()
        headers = client_info.split('\r\n')
        firstLine = headers[0]
        parts = firstLine.split(' ')
        print ("\n\n*****************")
        print ("parts", parts)
        if len(parts) < 2:
            print (">>>>>parts len is lower than 2")  # this is kind of error
            continue
        filename = parts[1]
        print ("filename", filename)
        if parts[0] == 'GET' or parts[0] == 'G':  # G is for AJAX...
            if filename == "/":
                print ("get index.html file")
                with open(r"..\wwwroot\homepage.html", mode='rb') as file:
                    # with open(r"c:\wwwroot\index.html", mode='rb') as file:
                    fileContent = file.read()
                    fileContent=fileContent.decode()
                msg = "HTTP/1.1 200 OK\r\n"
                msg = msg + "Content-Length:" + str(len(fileContent)) + "\r\n"
                msg = msg + "Content-Type: text/html; charset=utf-8" + "\r\n"
                msg = msg + "\r\n" + fileContent
            elif os.path.isfile(WWWROOT + filename[1:]):  # without the /
                
                print ("msg get file", WWWROOT + filename[1:])
                with open(WWWROOT + filename[1:], mode='rb') as file:
                    fileContent = file.read()
                    fileContent=fileContent.decode()
                msg = "HTTP/1.1 200 OK\r\n"
                if filename[1:]=="gamePage.html":
                    data="<br>"+"<h2> your qustion is :"+q+"<h2>"
                    msg = msg + "Content-Length:" + str(len(fileContent)+len(data)) + "\r\n"
                    msg= msg + "\r\n" + fileContent+data
                else:
                    msg = msg + "Content-Length:" + str(len(fileContent)) + "\r\n"
                    msg = msg + "\r\n" + fileContent
                
                #***************************************************************************************
            elif parts[1] == "/Foridden.html":
                msg = Forbidden()
            elif parts[1] == "/Redirect.html":
            
                msg = Redirect()
                
            elif "calculate-next" in filename:
                ansy=filename.split("=")[1]
                global answers
                global ans
                if (len(ans)!= len(answers)):
                    if ansy not in answers and ansy in ans  :
                        msg=answer_is_correct(ansy)
                    else:
                        msg=answer_is_incorrect(ansy)
                else:
                    msg=its_a_tye()
                
            elif parts[1] == "/InternalServerError.html":
                msg = InternalServerError()
            elif ".py" in filename[1:]:  # dynamic page - http://127.0.0.1/add3.py?nmb1=1&nmb2=2&nmb3=3
                print ("msg calcaulate something", filename[1:])
                parts = urllib.urlparse(filename[1:])
                print (parts)
                if parts.path == "add3.py":
                    print (11111111111111111111111111111111111111111111)
                    r = parts.query.split("&")
                    c = [i.split("=") for i in r]  # list comprhension
                    a = [int(i[1]) for i in c]  # list comprhension - take the second item from each list
                    x = a[0] + a[1] + a[2]
                    data = "<h1>result is: " + str(x) + "</h1>"
                    msg = "HTTP/1.1 200 OK\r\n"
                    msg = msg + "Content-Length:" + str(len(data)) + "\r\n"
                    msg = msg + "\r\n" + data
                elif parts.path == "add4.py":
                    print(2222222222222222222222222222222222222222222222222222222222)
                    r = parts.query.split("&")
                    c = [i.split("=") for i in r]  # list comprhension
                    a = [i[1] for i in c]  # list comprhension - take the second item from each list
                    params_str = " ".join(a)
                    aa = "python.exe " + parts.path + " " + params_str
                    print ("run python script", aa,)
                    data = subprocess.check_output(aa)  # let add4.py script do the job !
                    msg = "HTTP/1.1 200 OK\r\n"
                    msg = msg + "Content-Length:" + str(len(data)) + "\r\n"
                    msg = msg + "\r\n" + data
                elif parts.path == "readPeriodallyFromServer.py":
                    print ("2222222222222222222222222222222222222222222222")
                    print ("client_info1111111", client_info)
                    r = client_info.split("\r\n\r\n")
                    print ("rrrrrrr", r[1])
                    e = r[1].split('&')
                    c = [i.split("=") for i in e]  # list comprhension
                    a = [int(i[1]) + 1 for i in c]  # list comprhension - take the second item from each list
                    data = {"amount": a[0], "firstName": a[1], "lastName": a[2], "email": a[3]}
                    data = json.dumps(data)
                    # data = "<h1>result is: "+str(x)+"</h1>"
                    msg = "HTTP/1.1 200 OK\r\n"
                    msg = msg + "Content-Length:" + str(len(data)) + "\r\n"
                    msg = msg + "\r\n" + data
                elif parts[1] == "/Foridden.html":
                    msg = Forbidden()


                else:
                    print ("msg not found444")
                    msg = notFound()
            else:
                print ("msg not found222")
                msg = notFound()

        elif parts[0] == 'POST':
            print ("we got POST and do not know what to do.please help")
            print ("the data are of the post message holds nmb1=1&nmb2=2&nmb3=3")
            msg = notFound()


        else:
            print ("msg not found123")
            msg = notFound()
        client_socket.send(msg.encode())
    # print msg


if __name__ == '__main__':
    main()