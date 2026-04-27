import pandas as pd
import re
from methods import today
from models import car,user
history = "./database/history.csv"
cars = "./database/cars.csv"
logs = "./database/logs.csv"



    


def _filter(self,content,_where):
    df = pd.read_csv(_where)
    df = df[df.apply(lambda row: row.astype(str).str.contains(content, case=False)).any(axis=1)]
    return df.values.tolist()

# VALIDATION FUNCTIONS
#------------------------------------------------------------------
def validate_car_id(carid):
    """Araç ID'sinin sayı olup olmadığını kontrol eder"""
    try:
        int(carid)
        return True, ""
    except ValueError:
        return False, "Araç ID sadece rakamlardan oluşmalıdır!"

def validate_license_plate(plate):
    """Plaka formatını kontrol eder (örn: 34ABC123)"""
    # En az 2 rakam, sonra en az 2 harf, sonra rakamlar
    pattern = r'^\d{2,}[A-ZÇĞİÖŞÜ]{2,}\d+$'
    if re.match(pattern, plate.upper()):
        return True, ""
    else:
        return False, "Plaka formatı hatalı! Örnek: 34ABC123"

def validate_date(date_str):
    """Tarih formatını kontrol eder (dd-mm-yy)"""
    pattern = r'^\d{2}-\d{2}-\d{2}$'
    if re.match(pattern, date_str):
        try:
            day, month, year = map(int, date_str.split('-'))
            if 1 <= day <= 31 and 1 <= month <= 12 and 0 <= year <= 99:
                return True, ""
        except:
            pass
    return False, "Tarih formatı hatalı! Format: GG-AA-YY (örn: 25-12-24)"

def validate_payment(payment):
    """Ödeme bilgisinin sayı olup olmadığını kontrol eder"""
    try:
        float(payment)
        return True, ""
    except ValueError:
        return False, "Ödeme miktarı sadece rakamlardan oluşmalıdır!"

#------------------------------------------------------------------

# 1 - SHOW CARS
def show_cars_controller(param):
    return car.show_cars(param)


# 2 - ARABA EKLE
def add_car_controller(carid, marka, model, plaka, payment, owner):
    # Validasyon
    valid_id, id_msg = validate_car_id(carid)
    if not valid_id:
        return id_msg

    valid_plate, plate_msg = validate_license_plate(plaka)
    if not valid_plate:
        return plate_msg

    valid_payment, payment_msg = validate_payment(payment)
    if not valid_payment:
        return payment_msg

    c = car(carid, marka, model, plaka, payment, owner)
    return c.add_car()


# 3 - ARABA SİL
def remove_car_controller(carid):
    c = car(carid, None, None, None, None, None)
    return c.rm_car()


# 4 - ARABA KİRALA
def rent_car_controller(carid, userid, start_date, end_date):
    # Validasyon
    valid_start, start_msg = validate_date(start_date)
    if not valid_start:
        return start_msg

    valid_end, end_msg = validate_date(end_date)
    if not valid_end:
        return end_msg

    # Tarih karşılaştırmaları için bugünün tarihini al
    from datetime import datetime
    today = datetime.now().date()

    # Başlangıç tarihini parse et
    start_parts = start_date.split('-')
    start_date_obj = datetime(int('20' + start_parts[2]), int(start_parts[1]), int(start_parts[0])).date()

    # Bitiş tarihini parse et
    end_parts = end_date.split('-')
    end_date_obj = datetime(int('20' + end_parts[2]), int(end_parts[1]), int(end_parts[0])).date()

    # Başlangıç tarihi bugünden eski olmamalı
    if start_date_obj < today:
        return "Kiralama başlangıç tarihi bugünden eski olamaz!"

    # Bitiş tarihi başlangıç tarihinden sonra olmalı
    if end_date_obj <= start_date_obj:
        return "Kiralama bitiş tarihi başlangıç tarihinden sonra olmalı!"

    # Araç zaten kiralanmış durumda mı kontrol et
    try:
        df_logs = pd.read_csv(logs)
        car_rentals = df_logs[df_logs["carid"] == int(carid)]

        for _, rental in car_rentals.iterrows():
            # İade edilmiş kiralamaları atla
            if rental["iade"] != "-":
                continue

            # Aktif kiralama var mı kontrol et
            rental_end_parts = rental["dateend"].split('-')
            rental_end_date = datetime(int('20' + rental_end_parts[2]), int(rental_end_parts[1]), int(rental_end_parts[0])).date()

            # Eğer mevcut aktif kiralama varsa ve süresi bitmemişse izin verme
            if rental_end_date >= today:
                return f"Bu araç {rental['datestart']} - {rental['dateend']} tarihleri arasında kiralanmış durumda!"

    except Exception as e:
        print(f"Kiralama kontrolü hatası: {e}")
        # Hata durumunda devam et

    c = car(carid, None, None, None, None, None)
    return c._rent(userid, start_date, end_date)


# 5 - ARABA İADE
def iade_car_controller(carid, userid, iade_date):
    # Validasyon
    valid_date, date_msg = validate_date(iade_date)
    if not valid_date:
        return date_msg

    # İade tarihi bugünden eski olmamalı
    from datetime import datetime
    today = datetime.now().date()

    # İade tarihini parse et
    iade_parts = iade_date.split('-')
    iade_date_obj = datetime(int('20' + iade_parts[2]), int(iade_parts[1]), int(iade_parts[0])).date()

    if iade_date_obj < today:
        return "İade tarihi bugünden eski olamaz!"

    c = car(carid, None, None, None, None, None)
    return c._iade(userid, iade_date)


# 6 - SEPETE EKLE
def add_cart_controller(user:user,carid):
    return user.add_sepet(carid)


# 7 - SEPETTEN ÇIKAR (sadece seçili araç)
def remove_cart_controller(user:user, carid):
    return user.rm_sepet(carid=carid)


# 8 - SEPETİ BOŞALT
def clear_cart_controller(user:user):
    return user.rm_sepet(dellall=True)


# 9 - KİRALAMA GEÇMİŞİNİ GÖSTER
#günlük kiralama raporları
def daily_rent(id):
    df = pd.read_csv(history)
    rapor = df.loc[(df["id"] == id) & (df["date"] == today())]
    return rapor.values.tolist()


# 10 - ÇIKIŞ YAP
def logout_controller():
    print("Çıkış yapıldı.")
    return True

# 11 - ARAÇ KİRALAMA DETAYLARI
def get_car_rental_details(carid):
    """logs.csv'den aracın kiralama geçmişini döndürür"""
    try:
        df_logs = pd.read_csv(logs)
        df_cars = pd.read_csv(cars)

        # Aracın bilgilerini al
        car_info = df_logs[df_logs["carid"] == carid]

        if car_info.empty:
            return []

        result = []
        for _, rental in car_info.iterrows():
            result.append({
                "baslangic": rental["datestart"],
                "bitis": rental["dateend"],
                "iade": rental["iade"],
                "kiraci_id": rental["rentedby"]
            })

        return result
    except Exception as e:
        print(f"Araç detayları alınırken hata: {e}")
        return []

