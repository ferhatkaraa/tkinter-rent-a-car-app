import smtplib


def send_mail(_to,_title,_mesage):
    try:
        mymail = "python.ferhat@gmail.com"
        mailpassword = "xzft gpnu uvqz thst"

        _title = f"subject: {_title} \n"
        _content = _title + "\n" + _mesage
        #sunucu host name ve port numarası
        server = smtplib.SMTP("smtp.gmail.com",587)

        #bağlantıyı başlat
        server.ehlo()

        #bilgileri şifrele
        server.starttls()

        server.login(mymail,mailpassword)
        
        server.sendmail(mymail,_to,_content.encode("utf-8"))
        print("mail gönderildi")
    except Exception as e:
        print("MailExceptionEror",e)
    finally:
        server.close()
        
