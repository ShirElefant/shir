import socket
import os
import urllib
import subprocess
import json
import time
import sqlite3
import select
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
stri=""
open_client_sockets=[]
got_in=[]

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
    global answers
    global stri
    msg = "HTTP/1.1 200 OK\r\n"
    data = "<br><h1>Your answer "+ansy+" is correct</h1></br>"
    stri=stri+", "+ansy
    data= data+ "<h2> the answers that alredy have answered: "+stri+"</h2>"
    with open(WWWROOT + "gamePage.html", mode='rb') as file:
        fileContent = file.read()
        fileContent=fileContent.decode()
        msg = "HTTP/1.1 200 OK\r\n"
        msg = msg + "Content-Length:" + str(len(fileContent)+len(data)) + "\r\n"
        msg = msg + "\r\n" + fileContent+data
		
    answers.append(ansy)
    return msg
def answer_is_incorrect(ansy):
    global q
    global answers
    global stri
    msg = "HTTP/1.1 200 OK\r\n"
    data = "<br><h1>Your answer"+ansy+" is incorrect</h1><br>"
    data=data+"<br><h2> your qustion is: "+q+"</h2></br>"
    data= data+ "<h2> the answers that alredy have answered: "+stri+"</h2>"
    with open(WWWROOT + "gamePage.html", mode='rb') as file:
        fileContent = file.read()
        fileContent=fileContent.decode()
        msg = "HTTP/1.1 200 OK\r\n"
        msg = msg + "Content-Length:" + str(len(fileContent)+len(data)) + "\r\n"
        msg = msg + "\r\n" + fileContent+data
		
    
    return msg
def not_your_turn():
    global q
    global answers
    global stri
    msg = "HTTP/1.1 200 OK\r\n"
    data = "<br><h1>its not your turn</h1><br>"
    data=data+"<br><h2> your qustion is: "+q+"</h2></br>"
    data= data+ "<h2> the answers that alredy have answered: "+stri+"</h2>"
    with open(WWWROOT + "gamePage.html", mode='rb') as file:
        fileContent = file.read()
        fileContent=fileContent.decode()
        msg = "HTTP/1.1 200 OK\r\n"
        msg = msg + "Content-Length:" + str(len(fileContent)+len(data)) + "\r\n"
        msg = msg + "\r\n" + fileContent+data
		
    
    return msg
def its_a_tye():
    global answers
    global stri
    msg = "HTTP/1.1 200 OK\r\n"
    data = "<br><h1> no more correct answers. all the correct answers are: "+stri+"</h1><br>"
    with open(WWWROOT + "endPageTye.html", mode='rb') as file:
        fileContent = file.read()
        fileContent=fileContent.decode()
        msg = "HTTP/1.1 200 OK\r\n"
        msg = msg + "Content-Length:" + str(len(fileContent)+len(data)) + "\r\n"
        msg = msg + "\r\n" + fileContent+data
    return msg
    

i=0

def main():
    print ("start server")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    server_socket.bind(("127.0.0.1", 80))
    server_socket.listen(5)
   # client_socket, client_address) = server_socket.accept()
    print ("client connect")
    client_info="".encode()
    while (1):
        rlist, wlist, xlist = select.select([server_socket] + open_client_sockets, open_client_sockets, [])
        for client_socket in rlist:
            if client_socket is server_socket :
                (new_socket, adress) = server_socket.accept()
                open_client_sockets.append(new_socket)
            else:
                
                client_info = client_socket.recv(1024)
                 
                    
                # if client_info.decode() == "":
                    # print (">>>>close connection and wait for new connection")
                    # #client_socket.close()
                    # (client_socket, client_address) = server_socket.accept()  # wait for a new connection
                #print ("\n\n++++++++++++++++++++++")
                #print ("client_info", client_info)
                
                headers = client_info.decode().split('\r\n')
                firstLine = headers[0]
                parts = firstLine.split(' ')
                #print ("\n\n*****************")
                #print ("parts", parts)
                if len(parts) < 2:
                    #print (">>>>>parts len is lower than 2")  # this is kind of error
                    continue
                else :
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
                                global got_in
                                if len(got_in)<2:
                                    print (len(got_in))
                                    got_in.append(client_socket)
                                    data="<br>"+"<h2> your qustion is :"+q+"<h2>"
                                    msg = msg + "Content-Length:" + str(len(fileContent)+len(data)) + "\r\n"
                                    msg= msg + "\r\n" + fileContent+data
                                else:
                                    data="<h1> sorry we are full</h1>"
                                    msg = msg + "Content-Length:" +str(len(data)) + "\r\n"
                                    msg= msg + "\r\n" +data
                            else:
                                msg = msg + "Content-Length:" + str(len(fileContent)) + "\r\n"
                                msg = msg + "\r\n" + fileContent
                            
                            #***************************************************************************************
                        elif parts[1] == "/Foridden.html":
                            msg = Forbidden()
                        elif parts[1] == "/Redirect.html":
                        
                            msg = Redirect()
                            
                        elif "calculate-next" in filename:
                            
                        
                            print ("innnnnnnnnnnnnnnnnnnnnnnnn")
                            ansy=filename.split("=")[1]
                            global answers
                            global ans
                            if (len(ans)!= len(answers)):
                                if ansy not in answers and ansy in ans:
                                    msg=answer_is_correct(ansy)
                                else:
                                    msg=answer_is_incorrect(ansy)
                            else:
                                msg=its_a_tye()
                            
                        else:
                            msg =not_your_turn()
                        
                            if parts[1] == "/Foridden.html":
                                msg = Forbidden()


                            # elif client_info.decode()!='':
                                # print ("msg not found444")
                                # msg = notFound()
                        # elif client_info.decode()!='':
                            # print ("msg not found222")
                            # msg = notFound()

                if parts[0] == 'POST' and client_info.decode()!="":
                    print ("we got POST and do not know what to do.please help")
                    print ("the data are of the post message holds nmb1=1&nmb2=2&nmb3=3")
                    msg = notFound()


                elif client_info.decode()=="":
                    print ("msg not found123")
                    msg = notFound()
                client_socket.send(msg.encode())
    # print msg


if __name__ == '__main__':
    main()