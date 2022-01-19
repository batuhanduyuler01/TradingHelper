############################################
# eMailSender, kullanıcı isteğine göre     #
# belirlenen stock index tahmin & detay    #
# bilgilerini mail olarak gönderir.        #
############################################

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class eMailSender():
    def __init__(self):
        print("eMail Sender is ready to send!")
        #We need to set parameters
        self.__mailBuffer = "bos bir mail abi."
        self.__senderAddress = "batuhantradinghelper@gmail.com"
        self.__senderPassword = "batucan01"
        self.__receiverAddress = " "

        #Initialize smtp login.
        self.__server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        self.__server.ehlo()
        self.__server.login(self.__senderAddress, self.__senderPassword)



    def set_mail_buffer(self, mailToSend):

        if (0 == len(mailToSend)):
            print("We can not send an empty mail!")
            return False
        else:
            self.__mailBuffer = mailToSend
            return True
    
    def get_mail_buffer(self):
        return self.__mailBuffer

    def set_receiver_address(self, receiverAddress):
        if (len(receiverAddress) == 0):
            print("Falsely constructed mail address!")
            return False

        self.__receiverAddress = receiverAddress
        return True

    def get_receiver_address(self):
        return self.__receiverAddress

    def get_server(self):
        return self.__server

    def send_mail(self, receiverMail, mailContext):
        if (False == self.set_mail_buffer(mailContext)):
            return False

        if (False == self.set_receiver_address(receiverMail)):
            return False

        
        self.get_server().sendmail(self.__senderAddress, self.get_receiver_address(), self.get_mail_buffer())
        print("Mail is sent successfully!")
        return True



    def send_mail_with_html_buffer(self, receiverMail, htmlMsg):
        self.msg = MIMEMultipart('alternative')
        self.msg['Subject']  = "Trading Helper"
        self.msg['From'] = self.__senderAddress
        self.msg['To'] = receiverMail
        self.msgToAttached = MIMEText(htmlMsg, 'plain').as_string()
        self.msgAlreadyExist  = """\
        <html>
        <head></head>
        <body>
            <p>SELAMUN ALEYKUM!<br>
            Adresimiz: <a href="https://fulyatradinghelper.herokuapp.com">fulya trading helper</a> 
            </p>
        </body>
        </html>
        """

        part1 = MIMEText(self.msgToAttached, 'plain')
        part2 = MIMEText(self.msgAlreadyExist, 'html')
        self.msg.attach(part1)
        self.msg.attach(part2)

        self.get_server().sendmail(self.__senderAddress, receiverMail, self.msg.as_string())
        print("Html Mail is sent successfully!")
        

    def __del__(self):
        self.get_server().close()
