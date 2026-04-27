import pandas as pd
from methods import caniiade,canirent,today,nowtime

cars = "./database/cars.csv"
logs = "./database/logs.csv"
history = "./database/history.csv"
class car:
    
    def __init__(self,carid,marka,model,plaka,payment,owner):
        self.carid = carid
        self.marka = marka
        self.model = model
        self.plaka = plaka
        self.payment = payment
        self.owner = owner
    
    @classmethod
    def show_cars(cls,param):
        """sayfada görüntülenecek araçların listesini döndürür"""
        df = pd.read_csv(param)
        return df.values.tolist()
    
#           ARABA EKLEME VE SİLME
#---------------------------------------------------------------------
    def add_car(self):
        df = pd.read_csv(cars)
        if self.carid not in df["carid"].tolist():
            df.loc[len(df)] = [self.carid,self.marka,self.model,self.plaka,self.payment,self.owner]
            df.to_csv(cars,index=False)
            df2 = pd.read_csv(history)
            df2.loc[len(df2)] = [self.owner,"araç eklendi",f"{self.payment} TL",self.carid,today(),nowtime()]
            df2.to_csv(history,index=False)
            return "EKLEME BAŞARILI"
        else:
            return "ZATEN VAR"
        
    
    def rm_car(self):
        df = pd.read_csv(cars)
        if self.carid in df["carid"].tolist():
            df = df[df["carid"] != self.carid] 
            df.to_csv(cars,index=False)
            df2 = pd.read_csv(history)
            df2.loc[len(df2)] = [self.owner,"araç silindi",None,self.carid,today(),nowtime()]
            df2.to_csv(history,index=False)
            return "SİLME BAŞARILI"
        else:
            return "ARABA bulunamadı"
        
    
#--------------------------------------------------------------------


#           ARAÇ KİRALAMA VE İADE ETME
#--------------------------------------------------------------------
 
    def _rent(self,id,stdate,fndate):
        df = pd.read_csv(cars)
        if self.carid in df["carid"].tolist():
            df = pd.read_csv(logs)
            datelist = df.loc[df["carid"] == self.carid,("datestart","dateend","iade")].values.tolist()
            if canirent(datelist,stdate,fndate):
                df.loc[len(df)] = [self.carid,stdate,fndate,"-",id]
                df.to_csv(logs,index=False)
                df2 = pd.read_csv(history)
                df2.loc[len(df2)] = [id,"kiralama tamamlandı",f"{stdate}-{fndate}",self.carid,today(),nowtime()]
                df2.to_csv(history,index=False)
                return "KİRALAMA BAŞARILI"
            else:
                return "ZATEN KİRALANDI"
        else:
            return "ARABA BULUNUMADI"
        
    
    def _iade(self,id,iadedate):
        df = pd.read_csv(logs)
        datelist = df.loc[(df["rentedby"] == id) & (df["carid"] == self.carid),("datestart","dateend","iade")].values.tolist()
        b,s,f = caniiade(datelist,iadedate)
        if b:
            df.loc[(df["carid"] == self.carid) & (df["rentedby"] == id) & (df["datestart"] == s),"iade"] = iadedate 
            df.to_csv(logs,index=False)
            df2 = pd.read_csv(history)
            df2.loc[len(df2)] = [id,"iade tarihi güncellendi",iadedate,self.carid,today(),nowtime()]
            df2.to_csv(history,index=False)
            return "İADE BAŞARILI"
        else:
            return "TARİH HATALI"
        
   
#--------------------------------------------------------------------


    
    
    
    




