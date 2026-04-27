import pandas as pd
from models import user
from methods import send_mail

auth = "./database/auth.csv"

#views/auth.py
def sendmail(email):
    df = pd.read_csv(auth)
    password = df.loc[df["email"] == email, "password"]
    if not password.empty:
        konu = "ŞİFRE"
        content = f"şifreniz: {password.values[0]}"
        send_mail(email, konu, content)
        return True
    else:
        return False

#views/auth.py
def log_in(username,password):
    email = ""
    if "@" in username:
        email = username
        username =""
    
    u = user(username,password,email)
    opened = u.login()
    if opened != False:
        return opened
    return False
def sign_in(n,e,p):
    u = user(n,p,e)
    if u.signin():
        return True
    return False

#views/cars.py - Çıkış yap
def log_out(u:user):
    if u.logout():
        return True
    return False

#views/cars.py - Şifre değiştir
def change_password(u:user, oldpass, newpass):
    """Şifre değiştirme controller'ı"""
    return u.changepass(oldpass, newpass)

#views/cars.py - Hesap silme
def delete_account(u:user):
    """Hesap silme controller'ı - logout + signout"""
    if u.logout():  # Önce logout yap
        return u.signout()  # Sonra hesabı sil
    return False

