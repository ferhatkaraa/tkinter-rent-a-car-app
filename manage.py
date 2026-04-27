import pandas as pd
from views import AuthGUI, CarsGUI

auth_file = "./database/auth.csv"

def check_auto_login():
    """
    auth.csv'de islogin=1 olan kullanıcı var mı kontrol et.
    Varsa kullanıcı bilgilerini döndür, yoksa None döndür.
    """
    try:
        df = pd.read_csv(auth_file)
        logged_in = df[df["islogin"] == 1]
        
        if not logged_in.empty:
            # İlk giriş yapmış kullanıcıyı al
            user_row = logged_in.iloc[0]
            # [[id, email, name, password, islogin]] formatında döndür
            user_data = [[
                user_row["id"],
                user_row["email"],
                user_row["name"],
                user_row["password"],
                user_row["islogin"]
            ]]
            return user_data
        return None
    except Exception as e:
        print(f"Otomatik giriş kontrolü hatası: {e}")
        return None

if __name__ == "__main__":
    # Otomatik giriş kontrolü
    logged_user = check_auto_login()
    
    if logged_user:
        # islogin=1 olan kullanıcı var, otomatik giriş yap
        print(f"Otomatik giriş: {logged_user[0][2]}")
        CarsGUI(logged_user)
    else:
        # Giriş yapılmamış, AuthGUI göster
        AuthGUI()
