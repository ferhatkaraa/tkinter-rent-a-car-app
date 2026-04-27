import random
import pandas as pd


auth = "./database/auth.csv"
sepet = "./database/sepet.csv"
cars = "./database/cars.csv"

class user:

    def __init__(self, name, password, email, id=0):
        self.name = name
        self.password = password
        self.email = email
        self.id = id

        
    def signin(self):
        df = pd.read_csv(auth)
        if not df[df["email"] == self.email].empty:
            return "Email adresi zaten kayıtlı"
        if not df[df["name"] == self.name].empty:
            return "kullanıcı adı zaten kayıtlı"
        while True:
            new_id = random.randint(100000, 999999)
            if df[df["id"] == new_id].empty:
                self.id = new_id
                break
        df.loc[len(df)] = [self.id, self.email, self.name, self.password, 0]
        df.to_csv(auth, index=False)
        return True
        

    def login(self):
        """ kullanıcı girişi"""
        df = pd.read_csv(auth)
        df.loc[
            ((df["name"] == self.name) | (df["email"] == self.email)) &
            (df["password"] == self.password),
            "islogin"
        ] = 1
        df.to_csv(auth, index=False)
        opened = df.loc[
            ((df["name"] == self.name) | (df["email"] == self.email)) &
            (df["password"] == self.password)
            ].values.tolist()
        if len(opened) != 0:
            return opened
        return False 
    def logout(self):
        df = pd.read_csv(auth)
        df.loc[df["id"] == self.id, "islogin"] = 0
        df.to_csv(auth, index=False)
        return True
    
    def signout(self):
        df = pd.read_csv(auth)
        df = df[df["id"] != self.id]
        df.to_csv(auth, index=False)
        return True
    
    def changepass(self, oldpass, newpass):
        """Şifre değiştirme - eski şifreyi kontrol eder"""
        df = pd.read_csv(auth)
        
        # Kullanıcıyı bul ve eski şifreyi kontrol et
        user_row = df[(df["id"] == self.id) & (df["password"] == oldpass)]
        
        if user_row.empty:
            return "Eski şifre yanlış!"
        
        # Şifreyi güncelle
        df.loc[df["id"] == self.id, "password"] = newpass
        df.to_csv(auth, index=False)
        return True

    def add_sepet(self,carid):
        df = pd.read_csv(cars)
        if df[df["carid"] == carid].empty:  # empty bir property, method değil
            return "araç bulunamadı"
        df = pd.read_csv(sepet)
        df.loc[len(df)] = [self.id,carid]
        df.to_csv(sepet,index=False)
        return df.values.tolist()
        
    
    def rm_sepet(self, carid=None, dellall=False):
        """
        Sepetten araç çıkarma:
        - carid verilirse: Sadece o aracı sepetten çıkar
        - dellall=True ise: Kullanıcının tüm sepetini boşalt
        """
        df = pd.read_csv(sepet)
        
        if dellall:
            # Kullanıcının tüm sepetini boşalt
            df = df[df["id"] != self.id]
        elif carid is not None:
            # Sadece belirtilen aracı kullanıcının sepetinden çıkar
            df = df[~((df["id"] == self.id) & (df["carid"] == carid))]
        
        df.to_csv(sepet, index=False)
        return df.values.tolist()
        
    



