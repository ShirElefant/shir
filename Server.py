import socket
import os
import sqlite3
import select
import random


class the_english_game:
    # פעולות האתחול בפעולה זו נאתחל את כל המשתנים הדרושים לנו בקובץ
    def __init__(self):

        self.WWWROOT = "..\\wwwroot\\"#מיקום הקבצים
        self.answers = []#התשובות שנענו 
        #תהליך ההוצאה מתוך בסיס הנתונים
        conn = sqlite3.connect('GAME200.db')
        self.num = random.randrange(0, 2)
        cursor = conn.execute("SELECT * from GAME")
        rows = cursor.fetchall()
        theRow = rows[self.num]
        self.q = theRow[0]
        ans = theRow[1]
        self.ans = ans.split(":")
        self.stri = ""
        
        self.open_client_sockets = []#רשימת הלקוחות המחוברים אל השרת 
        self.got_in = []#רשימת הלקוחות שהצטרפו אל הפרויקט 
        self.numArror = 0



    def Redirect(self):
        msg = "HTTP/1.1 302 Redirect\r\n"
        data = "<h1>what you are looking for is not here</h1>"
        data = data + "<h1><marquee>302</marquee></h1>"
        msg = msg + "Content-Length:" + str(len(data)) + "\r\n"
        msg = msg + "location: 127.0.0.1/page2.html\r\n"
        print(msg)
        msg = msg + "\r\n" + data
        return msg
    #פעולה התשנה את ההודעה אשר תתקבל ותחזיר מידע כאשר לא נמצא הקובץ שהתבקש
    def notFound(self):
        msg = "HTTP/1.1 404 Not Found\r\n"
        data = "<h1>We did not found what you are looking for</h1>"
        data = data + "<h1><marquee>404</marquee></h1>"
        msg = msg + "Content-Length:" + str(len(data)) + "\r\n"
        msg = msg + "\r\n" + data
        return msg
    #פעולה התשנה את ההודעה שתשלח ללקוח אם הקובץ שהוא ביקש הוא אסור 
    def Forbidden(self):
        msg = "HTTP/1.1 403 Forbidden\r\n"
        data = "<h1>You cant enter to this</h1>"
        data = data + "<h1><marquee>403</marquee></h1>"
        msg = msg + "Content-Length:" + str(len(data)) + "\r\n"
        msg = msg + "\r\n" + data
        return msg
    #פעולה החזירה את ההודעה שתשלח ללקוח אם התשובה שהוא הכניס הינה נכונה 
    def answer_is_correct(self, ansy):
        msg = "HTTP/1.1 200 OK\r\n"
        #בודק האם כבר ענו את התשובה הזאת 
        if (ansy not in self.answers):
            data = "<br><h1>Your answer " + ansy + " is correct</h1></br>"
            self.stri = self.stri + ", " + ansy
            data = data + "<h2> The answers that have already been answered are: " + self.stri + "</h2>"
            with open(self.WWWROOT + "gamePage.html", mode='rb') as file:
                fileContent = file.read()
                fileContent = fileContent.decode()
                msg = "HTTP/1.1 200 OK\r\n"
                msg = msg + "Content-Length:" + str(len(fileContent) + len(data)) + "\r\n"
                msg = msg + "\r\n" + fileContent + data

        #אם לא ענו את התשובה הזאת
        else:
            data = "<br><h1>Your answer " + ansy + " is correct but has already been answered</h1></br>"
            data = data + "<h2> The answers that have already been answered are:  " + self.stri + "</h2>"
            with open(self.WWWROOT + "gamePage.html", mode='rb') as file:
                fileContent = file.read()
                fileContent = fileContent.decode()
                msg = "HTTP/1.1 200 OK\r\n"
                msg = msg + "Content-Length:" + str(len(fileContent) + len(data)) + "\r\n"
                msg = msg + "\r\n" + fileContent + data

        self.answers.append(ansy)
        return msg
    #פעולה המחזירה את ההודעה אל השחקן אם התשובה שלו לא נכונה 
    def answer_is_incorrect(self, ansy):

        msg = "HTTP/1.1 200 OK\r\n"
        #בודק האם השחקנים נפסלים לפי מספר הטעויות שלהם או שלא 
        if (self.numArror < 2):
            self.numArror = self.numArror + 1
            data = "<br><h1>Your answer " + ansy + " is incorrect</h1><br>"
            data = data + "<br><h2> Your question is: " + self.q + "</h2></br>"
            data = data + "<h2> The answers that have already been answered are: " + self.stri + "</h2>"
            data = data + "<h2> You have " + str(3 - self.numArror) + " tries left</h2>"
            
            with open(self.WWWROOT + "gamePage.html", mode='rb') as file:
                fileContent = file.read()
                fileContent = fileContent.decode()
                msg = "HTTP/1.1 200 OK\r\n"
                msg = msg + "Content-Length:" + str(len(fileContent) + len(data)) + "\r\n"
                msg = msg + "\r\n" + fileContent + data

        else:
            #יוצר את ההודעה אשר תוחזר אם נגמרו לשחקן הניסיונות
            data = "<br><h1>You're all ot of tries</h1><br>"
            with open(self.WWWROOT + "losingPage.html", mode='rb') as file:
                fileContent = file.read()
                fileContent = fileContent.decode()
                msg = "HTTP/1.1 200 OK\r\n"
                msg = msg + "Content-Length:" + str(len(fileContent) + len(data)) + "\r\n"
                msg = msg + "\r\n" + fileContent + data

        return msg

        return msg
    #הודעה התשלח אל השרת אם הוא ינצח א
    def winning_msg(self):

        msg = "HTTP/1.1 200 OK\r\n"
        data = "<br><h1>All the correct answers are: " + self.stri + "</h1><br>"
        with open(self.WWWROOT + "endPageTye.html", mode='rb') as file:
            fileContent = file.read()
            fileContent = fileContent.decode()
            msg = "HTTP/1.1 200 OK\r\n"
            msg = msg + "Content-Length:" + str(len(fileContent) + len(data)) + "\r\n"
            msg = msg + "\r\n" + fileContent + data
        return msg



    def main(self):
        print("start server")
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        server_socket.bind(("0.0.0.0", 80))
        server_socket.listen(5)
        print("client connect")
        client_info = "".encode()
        while (1):
            rlist, wlist, xlist = select.select([server_socket] + self.open_client_sockets, self.open_client_sockets,[])
            #עובר על כל הסוקטים המחוברים
            for client_socket in rlist:
                #מחבר את השחקן החדש אל השרת ומוסיף אותו לרשימת הסוקטים החדשים
                if client_socket is server_socket:
                    (new_socket, adress) = server_socket.accept()
                    self.open_client_sockets.append(new_socket)
                else:

                    client_info = client_socket.recv(1024)
                    #מחלק את המידע אל השורות המציינות את המידע הספציפי
                    headers = client_info.decode().split('\r\n')
                    firstLine = headers[0]
                    parts = firstLine.split(' ')#אורך ההודעה

                    if len(parts) < 2:

                        continue
                    else:
                        filename = parts[1]
                        print("filename", filename)
                        #מחזיר ללקוח את האתר שאותו הוא חיפש 
                        if parts[0] == 'GET' or parts[0] == 'G':  # G is for AJAX...
                            #מחזיר ללקוח את דף הכניסה של המשחק
                            if filename == "/":
                                print("get index.html file")
                                with open(r"..\wwwroot\homepage.html", mode='rb') as file:
                                    # with open(r"c:\wwwroot\index.html", mode='rb') as file:
                                    fileContent = file.read()
                                    fileContent = fileContent.decode()
                                msg = "HTTP/1.1 200 OK\r\n"
                                msg = msg + "Content-Length:" + str(len(fileContent)) + "\r\n"
                                msg = msg + "Content-Type: text/html; charset=utf-8" + "\r\n"
                                msg = msg + "\r\n" + fileContent
                            elif os.path.isfile(self.WWWROOT + filename[1:]):  # without the /

                                print("msg get file", self.WWWROOT + filename[1:])
                                with open(self.WWWROOT + filename[1:], mode='rb') as file:
                                    fileContent = file.read()
                                    fileContent = fileContent.decode()
                                msg = "HTTP/1.1 200 OK\r\n"
                                #מחזיר את דף המשחק הראשון אל השחקן 
                                if filename[1:] == "gamePage.html":
                                    #מחזיר לשני השחקנים הראשונים שמתחברים את דף המשחק
                                    if len(self.got_in) < 2:
                                        print(len(self.got_in))
                                        self.got_in.append(client_socket)
                                        data = "<br>" + "<h2> Your question is: " + self.q + "<h2>"
                                        msg = msg + "Content-Length:" + str(len(fileContent) + len(data)) + "\r\n"
                                        msg = msg + "\r\n" + fileContent + data
                                    else:# אם כמות השחקנים גדולה מ2 לא יתן להם להכנס
                                        data = "<h1> Sorry we are full</h1>"
                                        msg = msg + "Content-Length:" + str(len(data)) + "\r\n"
                                        msg = msg + "\r\n" + data
                                else:
                                    msg = msg + "Content-Length:" + str(len(fileContent)) + "\r\n"
                                    msg = msg + "\r\n" + fileContent

                                # ***************************************************************************************
                            elif parts[1] == "/Foridden.html":
                                msg = self.Forbidden()
                            elif parts[1] == "/Redirect.html":

                                msg = self.Redirect()
                            #אם קיימת הפעולה בתוך שם הקובץ שהתבקש אז מוציא מהקובץ את המידע הנדרש כלומר התשובה שלו ובודק אם התשובה נכונה 
                            elif "calculate-next" in filename:

                                print("innnnnnnnnnnnnnnnnnnnnnnnn")
                                ansy = filename.split("=")[1]
                                if (len(self.ans) != len(self.answers)):
                                    if ansy in self.ans:
                                        msg = self.answer_is_correct(ansy)
                                    else:
                                        msg = self.answer_is_incorrect(ansy)
                                else:
                                    msg = self.winning_msg()

                                if parts[1] == "/Foridden.html":
                                    msg = self.Forbidden()

                    if parts[0] == 'POST' and client_info.decode() != "":
                        print("we got POST and do not know what to do.please help")
                        print("the data are of the post message holds nmb1=1&nmb2=2&nmb3=3")
                        msg = self.notFound()


                    elif client_info.decode() == "":
                        print("msg not found123")
                        msg = self.notFound()
                    client_socket.send(msg.encode())


game = the_english_game()
game.main()
