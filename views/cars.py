import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from controls import (
    show_cars_controller,
    add_car_controller,
    rent_car_controller,
    iade_car_controller,
    add_cart_controller,
    remove_cart_controller,
    clear_cart_controller,
    remove_car_controller,
    daily_rent,
    log_out,
    change_password,
    delete_account,
    get_car_rental_details,
)
from models.auth import user as UserClass

cars = "./database/cars.csv"
logs = "./database/logs.csv"
sepet = "./database/sepet.csv"
history = "./database/history.csv"

class CarsGUI:
    def __init__(self, user):
        self.user = user
        self.tab = 1
        self.window = tk.Tk()
        self.window.title("Araç Kiralama Sistemi")
        self.window.geometry("900x600")
        self.window.minsize(700, 500)

        # responsive grid
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        style.configure("TNotebook.Tab", padding=[10, 6], font=("Arial", 11))

        # Notebook (sekme)
        notebook = ttk.Notebook(self.window)
        notebook.grid(sticky="nsew", padx=8, pady=8, row=0, column=0)

        # Tabs
        self.tab_cars = ttk.Frame(notebook)
        self.tab_cart = ttk.Frame(notebook)
        self.tab_mycars = ttk.Frame(notebook)
        self.tab_daily = ttk.Frame(notebook)
        self.tab_settings = ttk.Frame(notebook)

        notebook.add(self.tab_cars, text="Arabalar")
        notebook.add(self.tab_cart, text="Sepetim")
        notebook.add(self.tab_mycars, text="Benim Arabalarım")
        notebook.add(self.tab_daily, text="Günlük Kiralama Özeti")
        notebook.add(self.tab_settings, text="Ayarlar")

        # Build each tab
        self.build_cars_tab()
        self.build_cart_tab()
        self.build_my_cars_tab()
        self.build_daily_tab()
        self.build_settings_tab()

        # center window on screen
        self.center(self.window)

        self.window.mainloop()

    # -------------------- helper window positioning --------------------
    def center(self, win):
        win.update_idletasks()
        w = win.winfo_width()
        h = win.winfo_height()
        if w == 1 and h == 1:  # first geometry might be 1x1; use requested size
            try:
                geo = win.geometry().split("+")[0]
                w, h = map(int, geo.split("x"))
            except Exception:
                w, h = 900, 600
        x = (win.winfo_screenwidth() // 2) - (w // 2)
        y = (win.winfo_screenheight() // 2) - (h // 2)
        win.geometry(f"{w}x{h}+{x}+{y}")

    def popup_center(self, popup, parent):
        popup.update_idletasks()
        pw = popup.winfo_width()
        ph = popup.winfo_height()
        px = parent.winfo_x() + (parent.winfo_width() // 2) - (pw // 2)
        py = parent.winfo_y() + (parent.winfo_height() // 4)
        popup.geometry(f"+{px}+{py}")

    # -------------------- utility: build a left/right layout --------------------
    def _build_lr_frames(self, parent):
        """Return (left_frame, right_frame) configured for responsive layout."""
        parent.columnconfigure(0, weight=3)  # left bigger
        parent.columnconfigure(1, weight=1)
        parent.rowconfigure(0, weight=1)

        left = ttk.Frame(parent, padding=(6, 6))
        right = ttk.Frame(parent, padding=(6, 6))

        left.grid(row=0, column=0, sticky="nsew")
        right.grid(row=0, column=1, sticky="nsew")

        return left, right

    # -------------------- helper: make a treeview --------------------
    def _make_tree(self, parent, columns=("id", "brand", "model", "plate", "payment", "owner")):
        tv = ttk.Treeview(parent, columns=columns, show="headings", selectmode="browse")
        for col in columns:
            tv.heading(col, text=col.capitalize())
            tv.column(col, anchor="center", width=100, stretch=True)
        tv.pack(expand=True, fill="both")
        # vertical scrollbar
        vsb = ttk.Scrollbar(parent, orient="vertical", command=tv.yview)
        tv.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        return tv

    # -------------------- populate helpers --------------------
    def _populate_tree_from_df(self, tree, df):
        tree.delete(*tree.get_children())
        if df is None or df.empty:
            return
        # ensure columns exist
        cols = list(df.columns)
        for _, row in df.iterrows():
            values = [str(row[col]) if col in df.columns else "" for col in df.columns]
            tree.insert("", "end", values=values)

    # ========================= ARABALAR TAB =========================
    def build_cars_tab(self):
        left, right = self._build_lr_frames(self.tab_cars)

        # right paneli yeniden tanımlayıp mavi yap
        right.destroy()
        right = tk.Frame(self.tab_cars, bg="#e3f2fd", padx=6, pady=6)
        right.grid(row=0, column=1, sticky="nsew")

        # left: treeview of all cars
        lbl = ttk.Label(left, text="Arabalar", font=("Arial", 12, "bold"))
        lbl.pack(anchor="w", pady=(0, 6))
        self.tree_cars = self._make_tree(left, columns=("carid", "marka", "model", "plaka", "payment", "owner"))

        # Araçlara tıklandığında detayları göster
        self.tree_cars.bind("<Double-1>", self.show_car_details)

        # initial load - cars.csv'den tüm araçları çek
        self.refresh_cars_tree()

        # right: filter entry + buttons stacked
        tk.Label(right, text="Araç Filtrele:", bg="#e3f2fd", font=("Arial", 11)).pack(anchor="w", pady=(0, 6))
        self.filter_cars_var = tk.StringVar()
        ttk.Entry(right, textvariable=self.filter_cars_var).pack(fill="x", pady=(0, 10))

        # Güzel butonlar
        btn_filter = tk.Button(right, text="Filtrele", font=("Arial", 10), bg="#2196F3", fg="white", 
                               command=self.filter_cars, cursor="hand2")
        btn_filter.pack(fill="x", pady=6, ipady=4)
        btn_filter.bind("<Enter>", lambda e: btn_filter.config(bg="#64B5F6"))
        btn_filter.bind("<Leave>", lambda e: btn_filter.config(bg="#2196F3"))

        btn_add = tk.Button(right, text="Araba Ekle", font=("Arial", 10), bg="#4CAF50", fg="white",
                            command=self.open_add_car, cursor="hand2")
        btn_add.pack(fill="x", pady=6, ipady=4)
        btn_add.bind("<Enter>", lambda e: btn_add.config(bg="#66BB6A"))
        btn_add.bind("<Leave>", lambda e: btn_add.config(bg="#4CAF50"))

        btn_rent = tk.Button(right, text="Araç Kirala", font=("Arial", 10), bg="#FF9800", fg="white",
                             command=self.open_rent_car_from_cars, cursor="hand2")
        btn_rent.pack(fill="x", pady=6, ipady=4)
        btn_rent.bind("<Enter>", lambda e: btn_rent.config(bg="#FFB74D"))
        btn_rent.bind("<Leave>", lambda e: btn_rent.config(bg="#FF9800"))

        btn_cart = tk.Button(right, text="Sepete Ekle", font=("Arial", 10), bg="#9C27B0", fg="white",
                             command=self.add_selected_to_cart_from_cars, cursor="hand2")
        btn_cart.pack(fill="x", pady=6, ipady=4)
        btn_cart.bind("<Enter>", lambda e: btn_cart.config(bg="#BA68C8"))
        btn_cart.bind("<Leave>", lambda e: btn_cart.config(bg="#9C27B0"))

    def refresh_cars_tree(self):
        """cars.csv dosyasından tüm araçları yükle"""
        try:
            df = pd.read_csv(cars)
            self._populate_tree_from_df(self.tree_cars, df)
        except Exception as e:
            print(f"Arabalar yüklenirken hata: {e}")

    def filter_cars(self):
        keyword = self.filter_cars_var.get().strip()

        try:
            df = pd.read_csv(cars)  # cars.csv dosyasından oku

            if keyword:
                df = df[df.apply(
                    lambda row: row.astype(str).str.contains(keyword, case=False, na=False)
                ).any(axis=1)]

            self._populate_tree_from_df(self.tree_cars, df)
        except Exception as e:
            print(f"Filtreleme hatası: {e}")

    def open_add_car(self):
        popup = tk.Toplevel(self.window)
        popup.title("Araba Ekle")
        popup.geometry("450x350")
        popup.configure(bg="white")
        self.popup_center(popup, self.window)
        popup.columnconfigure(1, weight=1)

        # Başlık
        tk.Label(popup, text="Yeni Araç Ekle", font=("Arial", 14, "bold"), bg="white").grid(
            row=0, column=0, columnspan=2, pady=15)

        tk.Label(popup, text="Araç ID:", font=("Arial", 10), bg="white").grid(
            row=1, column=0, sticky="e", padx=10, pady=6)
        ent_id = ttk.Entry(popup, width=25)
        ent_id.grid(row=1, column=1, sticky="w", padx=10, pady=6)

        tk.Label(popup, text="Marka:", font=("Arial", 10), bg="white").grid(
            row=2, column=0, sticky="e", padx=10, pady=6)
        ent_brand = ttk.Entry(popup, width=25)
        ent_brand.grid(row=2, column=1, sticky="w", padx=10, pady=6)

        tk.Label(popup, text="Model:", font=("Arial", 10), bg="white").grid(
            row=3, column=0, sticky="e", padx=10, pady=6)
        ent_model = ttk.Entry(popup, width=25)
        ent_model.grid(row=3, column=1, sticky="w", padx=10, pady=6)

        tk.Label(popup, text="Plaka:", font=("Arial", 10), bg="white").grid(
            row=4, column=0, sticky="e", padx=10, pady=6)
        ent_plate = ttk.Entry(popup, width=25)
        ent_plate.grid(row=4, column=1, sticky="w", padx=10, pady=6)

        tk.Label(popup, text="Ödeme:", font=("Arial", 10), bg="white").grid(
            row=5, column=0, sticky="e", padx=10, pady=6)
        ent_payment = ttk.Entry(popup, width=25)
        ent_payment.grid(row=5, column=1, sticky="w", padx=10, pady=6)

        def do_add():
            cid = ent_id.get().strip()
            marka = ent_brand.get().strip()
            model = ent_model.get().strip()
            plaka = ent_plate.get().strip()
            payment = ent_payment.get().strip()

            # Validasyon
            if not cid or not marka or not model or not plaka or not payment:
                messagebox.showerror("Hata", "Tüm alanları doldurunuz!".center(100))
                return

            try:
                user_id = self.get_user_id()
                result = add_car_controller(cid, marka, model, plaka, payment, user_id)

                if result == "EKLEME BAŞARILI":
                    messagebox.showinfo("Başarılı", "Araç başarıyla eklendi.".center(100))
                    popup.destroy()
                    self.refresh_cars_tree()
                    self.refresh_my_cars()
                else:
                    messagebox.showerror("Hata", result.center(100))
            except Exception as e:
                messagebox.showerror("Hata", f"Ekleme başarısız: {e}".center(100))

        btn_add = tk.Button(popup, text="Ekle", font=("Arial", 11), bg="#4CAF50", fg="white",
                            command=do_add, cursor="hand2", width=15)
        btn_add.grid(row=7, column=0, columnspan=2, pady=15, ipady=4)
        btn_add.bind("<Enter>", lambda e: btn_add.config(bg="#66BB6A"))
        btn_add.bind("<Leave>", lambda e: btn_add.config(bg="#4CAF50"))

    def open_rent_car_from_cars(self):
        sel = self.tree_cars.selection()
        if not sel:
            messagebox.showwarning("Uyarı", "Lütfen soldaki listeden bir araç seçin.".center(100))
            return
        values = self.tree_cars.item(sel[0], "values")
        try:
            cid = int(values[0])
        except Exception:
            messagebox.showerror("Hata", "Geçersiz araç ID.".center(100))
            return

        popup = tk.Toplevel(self.window)
        popup.title("Araç Kirala")
        popup.geometry("380x200")
        popup.configure(bg="white")
        self.popup_center(popup, self.window)
        popup.columnconfigure(1, weight=1)

        tk.Label(popup, text=f"Araç ID: {cid}", font=("Arial", 12, "bold"), bg="white").grid(
            row=0, column=0, columnspan=2, pady=10)
        tk.Label(popup, text="Başlangıç tarih:", font=("Arial", 10), bg="white").grid(
            row=1, column=0, sticky="e", padx=10, pady=8)
        ent_st = ttk.Entry(popup, width=20)
        ent_st.grid(row=1, column=1, sticky="w", padx=10, pady=8)

        tk.Label(popup, text="Bitiş tarih:", font=("Arial", 10), bg="white").grid(
            row=2, column=0, sticky="e", padx=10, pady=8)
        ent_fn = ttk.Entry(popup, width=20)
        ent_fn.grid(row=2, column=1, sticky="w", padx=10, pady=8)

        def do_rent():
            st = ent_st.get().strip()
            fn = ent_fn.get().strip()

            # Validasyon
            if not st or not fn:
                messagebox.showerror("Hata", "Tarih alanlarını doldurunuz!".center(100))
                return

            try:
                user_id = self.get_user_id()
                result = rent_car_controller(cid, user_id, st, fn)
                if result == "KİRALAMA BAŞARILI":
                    messagebox.showinfo("Başarılı", "Araç başarıyla kiralandı.".center(100))
                    popup.destroy()
                    self.refresh_my_cars()
                else:
                    messagebox.showerror("Hata", result.center(100))
            except Exception as e:
                messagebox.showerror("Hata", f"Kiralama başarısız: {e}".center(100))

        btn_rent = tk.Button(popup, text="Kirala", font=("Arial", 11), bg="#FF9800", fg="white",
                             command=do_rent, cursor="hand2", width=15)
        btn_rent.grid(row=3, column=0, columnspan=2, pady=15, ipady=4)
        btn_rent.bind("<Enter>", lambda e: btn_rent.config(bg="#FFB74D"))
        btn_rent.bind("<Leave>", lambda e: btn_rent.config(bg="#FF9800"))

    def add_selected_to_cart_from_cars(self):
        sel = self.tree_cars.selection()
        if not sel:
            messagebox.showwarning("Uyarı", "Lütfen listeden bir araç seçin.".center(100))
            return
        values = self.tree_cars.item(sel[0], "values")
        try:
            cid = int(values[0])
        except Exception:
            messagebox.showerror("Hata", "Geçersiz araç ID.".center(100))
            return

        user_obj = self.get_user_object()
        ekle = add_cart_controller(user_obj, cid)
        if type(ekle) != str:
            messagebox.showinfo("Sepet", f"Araç ({cid}) sepete eklendi.".center(100))
            self.refresh_cart_tree()
        else:
            messagebox.showerror("Hata", ekle.center(100))

    # ========================= SEPET TAB =========================
    def build_cart_tab(self):
        left, right = self._build_lr_frames(self.tab_cart)

        # ---- RIGHT PANELİ tk.Frame olarak yeniden oluştur ----
        right.destroy()
        right = tk.Frame(self.tab_cart, bg="#e3f2fd", padx=6, pady=6)
        right.grid(row=0, column=1, sticky="nsew")
        ttk.Label(left, text="Sepetim", font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 6))
        self.tree_cart = self._make_tree(left, columns=("carid", "marka", "model", "plaka", "payment", "owner"))

        # right side: filter + buttons
        tk.Label(right, text="Araç Filtrele:", bg="#e3f2fd", font=("Arial", 11)).pack(anchor="w", pady=(0, 6))
        self.filter_cart_var = tk.StringVar()
        ttk.Entry(right, textvariable=self.filter_cart_var).pack(fill="x", pady=(0, 10))

        btn_filter = tk.Button(right, text="Filtrele", font=("Arial", 10), bg="#2196F3", fg="white",
                               command=self.filter_cart, cursor="hand2")
        btn_filter.pack(fill="x", pady=6, ipady=4)
        btn_filter.bind("<Enter>", lambda e: btn_filter.config(bg="#64B5F6"))
        btn_filter.bind("<Leave>", lambda e: btn_filter.config(bg="#2196F3"))

        btn_clear = tk.Button(right, text="Sepeti Boşalt", font=("Arial", 10), bg="#f44336", fg="white",
                              command=self.clear_cart, cursor="hand2")
        btn_clear.pack(fill="x", pady=6, ipady=4)
        btn_clear.bind("<Enter>", lambda e: btn_clear.config(bg="#EF5350"))
        btn_clear.bind("<Leave>", lambda e: btn_clear.config(bg="#f44336"))

        btn_remove = tk.Button(right, text="Sepetten Çıkar", font=("Arial", 10), bg="#FF5722", fg="white",
                               command=self.remove_from_cart, cursor="hand2")
        btn_remove.pack(fill="x", pady=6, ipady=4)
        btn_remove.bind("<Enter>", lambda e: btn_remove.config(bg="#FF8A65"))
        btn_remove.bind("<Leave>", lambda e: btn_remove.config(bg="#FF5722"))

        btn_rent = tk.Button(right, text="Araç Kirala", font=("Arial", 10), bg="#FF9800", fg="white",
                             command=self.rent_cart_items, cursor="hand2")
        btn_rent.pack(fill="x", pady=6, ipady=4)
        btn_rent.bind("<Enter>", lambda e: btn_rent.config(bg="#FFB74D"))
        btn_rent.bind("<Leave>", lambda e: btn_rent.config(bg="#FF9800"))

        # initial populate
        self.refresh_cart_tree()

    def get_user_id(self):
        """Kullanıcı ID'sini döndür"""
        if isinstance(self.user, list) and len(self.user) > 0:
            if isinstance(self.user[0], list) and len(self.user[0]) > 0:
                return self.user[0][0]
            return self.user[0]
        return self.user

    def get_user_object(self):
        """Controller fonksiyonları için user objesi oluştur"""
        if isinstance(self.user, list) and len(self.user) > 0:
            data = self.user[0] if isinstance(self.user[0], list) else self.user
            # data = [id, email, name, password, islogin]
            return UserClass(data[2], data[3], data[1], data[0])  # name, password, email, id
        return self.user

    def refresh_cart_tree(self):
        """sepet.csv'den kullanıcının sepetindeki araçları cars.csv ile birleştirerek göster"""
        try:
            user_id = self.get_user_id()
            
            # sepet.csv'den kullanıcının sepetindeki araç id'lerini al
            df_sepet = pd.read_csv(sepet)
            user_sepet = df_sepet[df_sepet["id"] == user_id]
            
            if user_sepet.empty:
                # Sepet boş
                df_cars = pd.read_csv(cars)
                empty_df = pd.DataFrame(columns=df_cars.columns)
                self._populate_tree_from_df(self.tree_cart, empty_df)
                return
            
            # Sepetteki araç id'leri
            cart_car_ids = user_sepet["carid"].tolist()
            
            # cars.csv'den bu araçların detaylarını getir
            df_cars = pd.read_csv(cars)
            df_filtered = df_cars[df_cars["carid"].isin(cart_car_ids)]
            
            self._populate_tree_from_df(self.tree_cart, df_filtered)
        except Exception as e:
            print(f"Sepet yenilenirken hata: {e}")

    def filter_cart(self):
        kw = self.filter_cart_var.get().strip()
        if not kw:
            self.refresh_cart_tree()
            return
        try:
            user_id = self.get_user_id()
            
            # sepet.csv'den kullanıcının sepetini al
            df_sepet = pd.read_csv(sepet)
            user_sepet = df_sepet[df_sepet["id"] == user_id]
            
            if user_sepet.empty:
                return
            
            cart_car_ids = user_sepet["carid"].tolist()
            
            # cars.csv'den araçları getir ve filtrele
            df_cars = pd.read_csv(cars)
            df_filtered = df_cars[df_cars["carid"].isin(cart_car_ids)]
            df_filtered = df_filtered[df_filtered.apply(
                lambda row: row.astype(str).str.contains(kw, case=False, na=False)
            ).any(axis=1)]
            
            self._populate_tree_from_df(self.tree_cart, df_filtered)
        except Exception as e:
            print("Filter cart error:", e)

    def clear_cart(self):
        if messagebox.askyesno("Onay", "Sepeti boşaltmak istediğinize emin misiniz?".center(100)):
            user_obj = self.get_user_object()
            clear_cart_controller(user_obj)
            self.refresh_cart_tree()
            messagebox.showinfo("Sepet", "Sepet başarıyla boşaltıldı.".center(100))

    def remove_from_cart(self):
        sel = self.tree_cart.selection()
        if not sel:
            messagebox.showwarning("Uyarı", "Lütfen sepetten çıkarmak için bir araç seçin.".center(100))
            return
        values = self.tree_cart.item(sel[0], "values")
        try:
            cid = int(values[0])
        except Exception:
            messagebox.showerror("Hata", "Geçersiz araç ID.".center(100))
            return
        user_obj = self.get_user_object()
        remove_cart_controller(user_obj, cid)
        self.refresh_cart_tree()
        messagebox.showinfo("Sepet", f"Araç ({cid}) sepetten çıkarıldı.".center(100))

    def rent_cart_items(self):
        """Sepetten seçili aracı kirala"""
        sel = self.tree_cart.selection()
        if not sel:
            messagebox.showwarning("Uyarı", "Lütfen listeden bir araç seçin.".center(100))
            return
        values = self.tree_cart.item(sel[0], "values")
        try:
            cid = int(values[0])
        except Exception:
            messagebox.showerror("Hata", "Geçersiz araç ID.".center(100))
            return

        popup = tk.Toplevel(self.window)
        popup.title("Araç Kirala")
        popup.geometry("380x200")
        popup.configure(bg="white")
        self.popup_center(popup, self.window)
        popup.columnconfigure(1, weight=1)

        tk.Label(popup, text=f"Araç ID: {cid}", font=("Arial", 12, "bold"), bg="white").grid(
            row=0, column=0, columnspan=2, pady=10)
        tk.Label(popup, text="Başlangıç tarih:", font=("Arial", 10), bg="white").grid(
            row=1, column=0, sticky="e", padx=10, pady=8)
        ent_st = ttk.Entry(popup, width=20)
        ent_st.grid(row=1, column=1, sticky="w", padx=10, pady=8)

        tk.Label(popup, text="Bitiş tarih:", font=("Arial", 10), bg="white").grid(
            row=2, column=0, sticky="e", padx=10, pady=8)
        ent_fn = ttk.Entry(popup, width=20)
        ent_fn.grid(row=2, column=1, sticky="w", padx=10, pady=8)

        def do_rent():
            st = ent_st.get().strip()
            fn = ent_fn.get().strip()

            # Validasyon
            if not st or not fn:
                messagebox.showerror("Hata", "Tarih alanlarını doldurunuz!".center(100))
                return

            try:
                user_id = self.get_user_id()
                user_obj = self.get_user_object()
                result = rent_car_controller(cid, user_id, st, fn)
                if result == "KİRALAMA BAŞARILI":
                    remove_cart_controller(user_obj, cid)
                    messagebox.showinfo("Başarılı", "Araç başarıyla kiralandı.".center(100))
                    popup.destroy()
                    self.refresh_cart_tree()
                    self.refresh_my_cars()
                else:
                    messagebox.showerror("Hata", result.center(100))
            except Exception as e:
                messagebox.showerror("Hata", f"Kiralama başarısız: {e}".center(100))

        btn_rent = tk.Button(popup, text="Kirala", font=("Arial", 11), bg="#FF9800", fg="white",
                             command=do_rent, cursor="hand2", width=15)
        btn_rent.grid(row=3, column=0, columnspan=2, pady=15, ipady=4)
        btn_rent.bind("<Enter>", lambda e: btn_rent.config(bg="#FFB74D"))
        btn_rent.bind("<Leave>", lambda e: btn_rent.config(bg="#FF9800"))

   # ========================= BENİM ARABALARIM TAB =========================
    def build_my_cars_tab(self):
        left, right = self._build_lr_frames(self.tab_mycars)

        # ---------- RIGHT PANELİ tk.Frame OLARAK YENİDEN OLUŞTUR ----------
        right.destroy()
        right = tk.Frame(self.tab_mycars, bg="#e3f2fd", padx=6, pady=6)
        right.grid(row=0, column=1, sticky="nsew")
        # ------------------------------------------------------------------

        ttk.Label(left, text="Benim Arabalarım & Kiraladıklarım", font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 6))
        self.tree_my = self._make_tree(left, columns=("carid", "marka", "model", "plaka", "payment", "durum"))
        self.refresh_my_cars()

        # right: filter + actions
        tk.Label(right, text="Araç Filtrele:", bg="#e3f2fd", font=("Arial", 11)).pack(anchor="w", pady=(0, 6))

        self.filter_my_var = tk.StringVar()
        ttk.Entry(right, textvariable=self.filter_my_var).pack(fill="x", pady=(0, 10))

        btn_filter = tk.Button(right, text="Filtrele", font=("Arial", 10), bg="#2196F3", fg="white",
                               command=self.filter_my_cars, cursor="hand2")
        btn_filter.pack(fill="x", pady=6, ipady=4)
        btn_filter.bind("<Enter>", lambda e: btn_filter.config(bg="#64B5F6"))
        btn_filter.bind("<Leave>", lambda e: btn_filter.config(bg="#2196F3"))

        btn_add = tk.Button(right, text="Araba Ekle", font=("Arial", 10), bg="#4CAF50", fg="white",
                            command=self.open_add_car_for_me, cursor="hand2")
        btn_add.pack(fill="x", pady=6, ipady=4)
        btn_add.bind("<Enter>", lambda e: btn_add.config(bg="#66BB6A"))
        btn_add.bind("<Leave>", lambda e: btn_add.config(bg="#4CAF50"))

        btn_delete = tk.Button(right, text="Araba Sil", font=("Arial", 10), bg="#f44336", fg="white",
                               command=self.remove_my_car_selected, cursor="hand2")
        btn_delete.pack(fill="x", pady=6, ipady=4)
        btn_delete.bind("<Enter>", lambda e: btn_delete.config(bg="#EF5350"))
        btn_delete.bind("<Leave>", lambda e: btn_delete.config(bg="#f44336"))

        btn_iade = tk.Button(right, text="Araç İade", font=("Arial", 10), bg="#FF9800", fg="white",
                             command=self.open_iade_for_mycar, cursor="hand2")
        btn_iade.pack(fill="x", pady=6, ipady=4)
        btn_iade.bind("<Enter>", lambda e: btn_iade.config(bg="#FFB74D"))
        btn_iade.bind("<Leave>", lambda e: btn_iade.config(bg="#FF9800"))

    def refresh_my_cars(self):
        """
        Benim Arabalarım sekmesi:
        1. cars.csv'den owner'ı benim olan araçlar (Sahibi)
        2. logs.csv'den kiraladığım araçlar (Kiralandı)
        """
        try:
            user_id = self.get_user_id()
            df_cars = pd.read_csv(cars)
            df_logs = pd.read_csv(logs)
            
            result_list = []
            added_car_ids = set()  # Tekrar eklemeyi önlemek için
            
            # 1. Owner'ı benim olan araçlar
            my_owned = df_cars[df_cars["owner"].astype(str) == str(user_id)]
            for _, row in my_owned.iterrows():
                result_list.append({
                    "carid": row["carid"],
                    "marka": row["marka"],
                    "model": row["model"],
                    "plaka": row["plaka"],
                    "payment": row["payment"],
                    "durum": "Sahibi"
                })
                added_car_ids.add(row["carid"])
            
            # 2. Kiraladığım araçlar (logs.csv'den rentedby = user_id olanlar)
            my_rented = df_logs[df_logs["rentedby"].astype(str) == str(user_id)]
            
            for _, rental in my_rented.iterrows():
                car_id = rental["carid"]
                
                # Zaten eklenmişse atla
                if car_id in added_car_ids:
                    continue
                
                # Araç detayını cars.csv'den al
                car_detail = df_cars[df_cars["carid"] == car_id]
                if not car_detail.empty:
                    row = car_detail.iloc[0]
                    result_list.append({
                        "carid": row["carid"],
                        "marka": row["marka"],
                        "model": row["model"],
                        "plaka": row["plaka"],
                        "payment": row["payment"],
                        "durum": "Kiralandı"
                    })
                    added_car_ids.add(car_id)
            
            # DataFrame oluştur ve göster
            if result_list:
                result_df = pd.DataFrame(result_list)
                self._populate_tree_from_df(self.tree_my, result_df)
            else:
                empty_df = pd.DataFrame(columns=["carid", "marka", "model", "plaka", "payment", "durum"])
                self._populate_tree_from_df(self.tree_my, empty_df)
                
        except Exception as e:
            print(f"Benim arabalarım yüklenirken hata: {e}")

    def filter_my_cars(self):
        kw = self.filter_my_var.get().strip()
        if not kw:
            self.refresh_my_cars()
            return
        try:
            user_id = self.get_user_id()
            df_cars = pd.read_csv(cars)
            df_logs = pd.read_csv(logs)
            
            result_list = []
            added_car_ids = set()
            
            # Owner'ı benim olan araçlar
            my_owned = df_cars[df_cars["owner"].astype(str) == str(user_id)]
            for _, row in my_owned.iterrows():
                result_list.append({
                    "carid": row["carid"],
                    "marka": row["marka"],
                    "model": row["model"],
                    "plaka": row["plaka"],
                    "payment": row["payment"],
                    "durum": "Sahibi"
                })
                added_car_ids.add(row["carid"])
            
            # Kiraladığım araçlar (logs.csv'den)
            my_rented = df_logs[df_logs["rentedby"].astype(str) == str(user_id)]
            
            for _, rental in my_rented.iterrows():
                car_id = rental["carid"]
                if car_id in added_car_ids:
                    continue
                    
                car_detail = df_cars[df_cars["carid"] == car_id]
                if not car_detail.empty:
                    row = car_detail.iloc[0]
                    result_list.append({
                        "carid": row["carid"],
                        "marka": row["marka"],
                        "model": row["model"],
                        "plaka": row["plaka"],
                        "payment": row["payment"],
                        "durum": "Kiralandı"
                    })
                    added_car_ids.add(car_id)
            
            if result_list:
                result_df = pd.DataFrame(result_list)
                # Anahtar kelime filtresi uygula
                result_df = result_df[result_df.apply(
                    lambda row: row.astype(str).str.contains(kw, case=False, na=False)
                ).any(axis=1)]
                self._populate_tree_from_df(self.tree_my, result_df)
        except Exception as e:
            print(f"Filtreleme hatası: {e}")

    def open_add_car_for_me(self):
        popup = tk.Toplevel(self.window)
        popup.title("Araba Ekle")
        popup.geometry("450x350")
        popup.configure(bg="white")
        self.popup_center(popup, self.window)
        popup.columnconfigure(1, weight=1)

        tk.Label(popup, text="Yeni Araç Ekle", font=("Arial", 13, "bold"), bg="white").grid(
            row=0, column=0, columnspan=2, pady=15)

        tk.Label(popup, text="Araç ID:", font=("Arial", 10), bg="white").grid(
            row=1, column=0, sticky="e", padx=10, pady=6)
        ent_id = ttk.Entry(popup, width=22)
        ent_id.grid(row=1, column=1, sticky="w", padx=10, pady=6)

        tk.Label(popup, text="Marka:", font=("Arial", 10), bg="white").grid(
            row=2, column=0, sticky="e", padx=10, pady=6)
        ent_brand = ttk.Entry(popup, width=22)
        ent_brand.grid(row=2, column=1, sticky="w", padx=10, pady=6)

        tk.Label(popup, text="Model:", font=("Arial", 10), bg="white").grid(
            row=3, column=0, sticky="e", padx=10, pady=6)
        ent_model = ttk.Entry(popup, width=22)
        ent_model.grid(row=3, column=1, sticky="w", padx=10, pady=6)

        tk.Label(popup, text="Plaka:", font=("Arial", 10), bg="white").grid(
            row=4, column=0, sticky="e", padx=10, pady=6)
        ent_plate = ttk.Entry(popup, width=22)
        ent_plate.grid(row=4, column=1, sticky="w", padx=10, pady=6)

        tk.Label(popup, text="Ödeme:", font=("Arial", 10), bg="white").grid(
            row=5, column=0, sticky="e", padx=10, pady=6)
        ent_payment = ttk.Entry(popup, width=22)
        ent_payment.grid(row=5, column=1, sticky="w", padx=10, pady=6)

        def do_add():
            cid = ent_id.get().strip()
            marka = ent_brand.get().strip()
            model = ent_model.get()
            plaka = ent_plate.get().strip()
            payment = ent_payment.get().strip()

            # Validasyon
            if not cid or not marka or not model or not plaka or not payment:
                messagebox.showerror("Hata", "Tüm alanları doldurunuz!".center(100))
                return

            try:
                user_id = self.get_user_id()
                result = add_car_controller(cid, marka, model, plaka, payment, user_id)

                if result == "EKLEME BAŞARILI":
                    messagebox.showinfo("Başarılı", "Araç başarıyla eklendi.".center(100))
                    popup.destroy()
                    self.refresh_my_cars()
                    self.refresh_cars_tree()
                else:
                    messagebox.showerror("Hata", result.center(100))
            except Exception as e:
                messagebox.showerror("Hata", f"Ekleme başarısız: {e}".center(100))

        btn_add = tk.Button(popup, text="Ekle", font=("Arial", 11), bg="#4CAF50", fg="white",
                            command=do_add, cursor="hand2", width=15)
        btn_add.grid(row=6, column=0, columnspan=2, pady=15, ipady=4)
        btn_add.bind("<Enter>", lambda e: btn_add.config(bg="#66BB6A"))
        btn_add.bind("<Leave>", lambda e: btn_add.config(bg="#4CAF50"))

    def remove_my_car_selected(self):
        sel = self.tree_my.selection()
        if not sel:
            messagebox.showwarning("Uyarı", "Lütfen silmek için bir araç seçin.".center(100))
            return
        values = self.tree_my.item(sel[0], "values")
        try:
            cid = int(values[0])
        except Exception:
            messagebox.showerror("Hata", "Geçersiz araç ID.".center(100))
            return
        
        if messagebox.askyesno("Onay", f"Araç ({cid}) silmek istediğinize emin misiniz?".center(100)):
            try:
                remove_car_controller(cid)
                messagebox.showinfo("Başarılı", "Araç başarıyla silindi.".center(100))
                self.refresh_my_cars()
                self.refresh_cars_tree()
            except Exception as e:
                messagebox.showerror("Hata", f"Silme sırasında hata: {e}".center(100))

    def open_iade_for_mycar(self):
        sel = self.tree_my.selection()
        if not sel:
            messagebox.showwarning("Uyarı", "Lütfen iade için bir araç seçin.".center(100))
            return
        values = self.tree_my.item(sel[0], "values")
        try:
            cid = int(values[0])
        except Exception:
            messagebox.showerror("Hata", "Geçersiz araç ID.".center(100))
            return
        
        popup = tk.Toplevel(self.window)
        popup.title("Araç İade")
        popup.geometry("380x180")
        popup.configure(bg="white")
        self.popup_center(popup, self.window)
        popup.columnconfigure(1, weight=1)

        tk.Label(popup, text=f"Araç ID: {cid}", font=("Arial", 12, "bold"), bg="white").grid(
            row=0, column=0, columnspan=2, pady=15)
        tk.Label(popup, text="İade tarih:", font=("Arial", 10), bg="white").grid(
            row=1, column=0, sticky="e", padx=10, pady=10)
        ent_fn = ttk.Entry(popup, width=20)
        ent_fn.grid(row=1, column=1, sticky="w", padx=10, pady=10)

        def do_iade():
            fn = ent_fn.get().strip()

            # Validasyon
            if not fn:
                messagebox.showerror("Hata", "İade tarihini giriniz!".center(100))
                return

            try:
                user_id = self.get_user_id()
                result = iade_car_controller(cid, user_id, fn)
                messagebox.showinfo("Bilgi", result.center(100))
                popup.destroy()
                self.refresh_my_cars()
            except Exception as e:
                messagebox.showerror("Hata", f"İade yapılamadı: {e}".center(100))

        btn_iade = tk.Button(popup, text="İade Et", font=("Arial", 11), bg="#FF9800", fg="white",
                             command=do_iade, cursor="hand2", width=15)
        btn_iade.grid(row=2, column=0, columnspan=2, pady=15, ipady=4)
        btn_iade.bind("<Enter>", lambda e: btn_iade.config(bg="#FFB74D"))
        btn_iade.bind("<Leave>", lambda e: btn_iade.config(bg="#FF9800"))

    # ========================= GÜNLÜK ÖZET TAB =========================
    def build_daily_tab(self):
        frame = self.tab_daily
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(2, weight=1)

        # Butonlar
        btn_frame = tk.Frame(frame, bg="#e3f2fd")
        btn_frame.grid(row=0, column=0, pady=12, sticky="ew", padx=8)
        
        btn_all = tk.Button(btn_frame, text="Tüm Geçmişimi Göster", font=("Arial", 10), 
                            bg="#2196F3", fg="white", command=self.show_all_history, cursor="hand2")
        btn_all.pack(side="left", padx=5, ipady=4, ipadx=8)
        btn_all.bind("<Enter>", lambda e: btn_all.config(bg="#64B5F6"))
        btn_all.bind("<Leave>", lambda e: btn_all.config(bg="#2196F3"))

        btn_today = tk.Button(btn_frame, text="Bugünkü İşlemlerim", font=("Arial", 10),
                              bg="#4CAF50", fg="white", command=self.daily_report, cursor="hand2")
        btn_today.pack(side="left", padx=5, ipady=4, ipadx=8)
        btn_today.bind("<Enter>", lambda e: btn_today.config(bg="#66BB6A"))
        btn_today.bind("<Leave>", lambda e: btn_today.config(bg="#4CAF50"))

        btn_clear = tk.Button(btn_frame, text="Temizle", font=("Arial", 10),
                              bg="#9E9E9E", fg="white", command=self.clear_history_text, cursor="hand2")
        btn_clear.pack(side="left", padx=5, ipady=4, ipadx=8)
        btn_clear.bind("<Enter>", lambda e: btn_clear.config(bg="#BDBDBD"))
        btn_clear.bind("<Leave>", lambda e: btn_clear.config(bg="#9E9E9E"))

        # Treeview for history
        ttk.Label(frame, text="Kiralama Geçmişi (history.csv)", font=("Arial", 11, "bold")).grid(row=1, column=0, sticky="w", padx=8)
        
        tree_frame = ttk.Frame(frame)
        tree_frame.grid(row=2, column=0, sticky="nsew", padx=8, pady=6)
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
        
        self.tree_history = ttk.Treeview(tree_frame, 
            columns=("id", "islem", "deger", "carid", "tarih", "saat"), 
            show="headings", selectmode="browse")
        
        # Kolon başlıkları
        self.tree_history.heading("id", text="Kullanıcı ID")
        self.tree_history.heading("islem", text="İşlem")
        self.tree_history.heading("deger", text="Değer")
        self.tree_history.heading("carid", text="Araç ID")
        self.tree_history.heading("tarih", text="Tarih")
        self.tree_history.heading("saat", text="Saat")
        
        for col in ("id", "islem", "deger", "carid", "tarih", "saat"):
            self.tree_history.column(col, anchor="center", width=100, stretch=True)
        
        self.tree_history.grid(row=0, column=0, sticky="nsew")
        
        # scrollbar
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree_history.yview)
        self.tree_history.configure(yscrollcommand=vsb.set)
        vsb.grid(row=0, column=1, sticky="ns")

    def show_all_history(self):
        """history.csv'den kullanıcının tüm işlem geçmişini göster"""
        try:
            user_id = self.get_user_id()
            df = pd.read_csv(history)
            
            user_history = df[df["id"].astype(str) == str(user_id)]
            
            self.tree_history.delete(*self.tree_history.get_children())
            
            if user_history.empty:
                messagebox.showinfo("Bilgi", "Henüz işlem geçmişiniz bulunmuyor.".center(100))
                return
            
            for _, row in user_history.iterrows():
                self.tree_history.insert("", "end", values=(
                    row.get("id", ""),
                    row.get("did", ""),
                    row.get("value", ""),
                    row.get("carid", ""),
                    row.get("date", ""),
                    row.get("time", "")
                ))
                
        except Exception as e:
            messagebox.showerror("Hata", f"Geçmiş yüklenemedi: {e}".center(100))

    def daily_report(self):
        """history.csv'den bugünkü işlemleri göster"""
        try:
            user_id = self.get_user_id()
            result = daily_rent(user_id)
            
            self.tree_history.delete(*self.tree_history.get_children())
            
            if not result or len(result) == 0:
                messagebox.showinfo("Bilgi", "Bugün hiç işlem yapılmamış.".center(100))
                return
            
            for row in result:
                if len(row) >= 6:
                    self.tree_history.insert("", "end", values=(
                        row[0],
                        row[1],
                        row[2],
                        row[3],
                        row[4],
                        row[5]
                    ))
                    
        except Exception as e:
            messagebox.showerror("Hata", f"Özet alınamadı: {e}".center(100))

    def clear_history_text(self):
        """Geçmiş treeview'ini temizle"""
        self.tree_history.delete(*self.tree_history.get_children())

    def show_car_details(self, event):
        """Araçlara çift tıklandığında kiralama detaylarını göster"""
        sel = self.tree_cars.selection()
        if not sel:
            return

        values = self.tree_cars.item(sel[0], "values")
        try:
            carid = int(values[0])
        except:
            return

        # Araç bilgilerini al
        rental_details = get_car_rental_details(carid)

        # Popup oluştur
        popup = tk.Toplevel(self.window)
        popup.title(f"Araç {carid} - Kiralama Detayları")
        popup.geometry("500x400")
        popup.configure(bg="white")
        self.popup_center(popup, self.window)

        # Başlık
        tk.Label(popup, text=f"Araç ID: {carid}", font=("Arial", 14, "bold"), bg="white").pack(pady=10)

        # Detaylar için frame
        frame = tk.Frame(popup, bg="white")
        frame.pack(fill="both", expand=True, padx=20, pady=10)

        if not rental_details:
            tk.Label(frame, text="Bu araç henüz hiç kiralanmamış.", font=("Arial", 11),
                    bg="white", fg="#666").pack(pady=20)
        else:
            # Başlık
            tk.Label(frame, text="Kiralama Geçmişi:", font=("Arial", 12, "bold"),
                    bg="white").pack(anchor="w", pady=(0, 10))

            # Scrollable text area
            text_frame = tk.Frame(frame, bg="white", bd=1, relief="solid")
            text_frame.pack(fill="both", expand=True)

            scrollbar = tk.Scrollbar(text_frame)
            scrollbar.pack(side="right", fill="y")

            text_area = tk.Text(text_frame, height=15, wrap="word", yscrollcommand=scrollbar.set,
                              font=("Arial", 10), bg="#f8f9fa", padx=10, pady=10)
            text_area.pack(fill="both", expand=True)
            scrollbar.config(command=text_area.yview)

            text_area.insert("1.0", "Dolu Zaman Aralıkları:\n")
            text_area.insert("end", "=" * 40 + "\n\n")

            for detail in rental_details:
                status = "İade Edildi" if detail["iade"] != "-" else "Henüz İade Edilmedi"
                text = f"• {detail['baslangic']} - {detail['bitis']} ({status})\n"
                if detail["iade"] != "-":
                    text += f"  İade Tarihi: {detail['iade']}\n"
                text += "\n"
                text_area.insert("end", text)

            text_area.config(state="disabled")

        # Kapat butonu
        btn_close = tk.Button(popup, text="Kapat", font=("Arial", 11), bg="#666", fg="white",
                             command=popup.destroy, cursor="hand2", width=15)
        btn_close.pack(pady=15)
        btn_close.bind("<Enter>", lambda e: btn_close.config(bg="#888"))
        btn_close.bind("<Leave>", lambda e: btn_close.config(bg="#666"))

    # ========================= AYARLAR TAB =========================
    def build_settings_tab(self):
        frame = self.tab_settings
        frame.columnconfigure(0, weight=1)
        
        # Ana container - ortada
        container = tk.Frame(frame, bg="white", padx=30, pady=30)
        container.place(relx=0.5, rely=0.5, anchor="center")

        # ===== ŞİFRE DEĞİŞTİRME BÖLÜMÜ =====
        ttk.Label(container, text="Şifre Değiştir", font=("Arial", 14, "bold")).grid(
            row=0, column=0, columnspan=2, pady=(0, 20), sticky="w")

        ttk.Label(container, text="Eski Şifre:", font=("Arial", 11)).grid(
            row=1, column=0, sticky="e", padx=(0, 10), pady=8)
        self.ent_old_pass = ttk.Entry(container, show="*", width=25)
        self.ent_old_pass.grid(row=1, column=1, pady=8)

        ttk.Label(container, text="Yeni Şifre:", font=("Arial", 11)).grid(
            row=2, column=0, sticky="e", padx=(0, 10), pady=8)
        self.ent_new_pass = ttk.Entry(container, show="*", width=25)
        self.ent_new_pass.grid(row=2, column=1, pady=8)

        ttk.Label(container, text="Şifre Onayla:", font=("Arial", 11)).grid(
            row=3, column=0, sticky="e", padx=(0, 10), pady=8)
        self.ent_confirm_pass = ttk.Entry(container, show="*", width=25)
        self.ent_confirm_pass.grid(row=3, column=1, pady=8)

        btn_change = tk.Button(container, text="Şifreyi Değiştir",
                               font=("Arial", 11), bg="#4CAF50", fg="white",
                               command=self.do_change_password, width=20)
        btn_change.grid(row=5, column=0, columnspan=2, pady=20)
        btn_change.bind("<Enter>", lambda e: btn_change.config(bg="#66BB6A"))
        btn_change.bind("<Leave>", lambda e: btn_change.config(bg="#4CAF50"))

        # Ayırıcı çizgi
        ttk.Separator(container, orient="horizontal").grid(
            row=6, column=0, columnspan=2, sticky="ew", pady=20)

        # ===== ÇIKIŞ BÖLÜMÜ =====
        ttk.Label(container, text="Oturum", font=("Arial", 14, "bold")).grid(
            row=7, column=0, columnspan=2, pady=(0, 15), sticky="w")

        btn_logout = tk.Button(container, text="Çıkış Yap",
                               font=("Arial", 11), bg="#f44336", fg="white",
                               command=self.do_logout, width=20)
        btn_logout.grid(row=8, column=0, columnspan=2, pady=8)
        btn_logout.bind("<Enter>", lambda e: btn_logout.config(bg="#EF5350"))
        btn_logout.bind("<Leave>", lambda e: btn_logout.config(bg="#f44336"))

        # ===== HESAP SİLME BÖLÜMÜ =====
        ttk.Separator(container, orient="horizontal").grid(
            row=9, column=0, columnspan=2, sticky="ew", pady=20)

        ttk.Label(container, text="Hesap Yönetimi", font=("Arial", 14, "bold")).grid(
            row=10, column=0, columnspan=2, pady=(0, 15), sticky="w")

        # Uyarı mesajı
        warning_label = tk.Label(container, text="⚠️ Bu işlem geri alınamaz!",
                                fg="red", bg="white", font=("Arial", 10, "bold"))
        warning_label.grid(row=11, column=0, columnspan=2, pady=(0, 10))

        btn_delete = tk.Button(container, text="Hesabımı Sil",
                               font=("Arial", 11), bg="#d32f2f", fg="white",
                               command=self.do_delete_account, width=20)
        btn_delete.grid(row=12, column=0, columnspan=2, pady=10)
        btn_delete.bind("<Enter>", lambda e: btn_delete.config(bg="#b71c1c"))
        btn_delete.bind("<Leave>", lambda e: btn_delete.config(bg="#d32f2f"))

    def do_change_password(self):
        """Şifre değiştirme işlemi"""
        old_pass = self.ent_old_pass.get().strip()
        new_pass = self.ent_new_pass.get().strip()
        confirm_pass = self.ent_confirm_pass.get().strip()

        if not old_pass or not new_pass or not confirm_pass:
            messagebox.showerror("Hata", "Tüm alanları doldurunuz!".center(100))
            return

        if new_pass != confirm_pass:
            messagebox.showerror("Hata", "Yeni şifreler eşleşmiyor!".center(100))
            return

        if len(new_pass) < 3:
            messagebox.showerror("Hata", "Yeni şifre en az 3 karakter olmalı!".center(100))
            return

        user_obj = self.get_user_object()
        result = change_password(user_obj, old_pass, new_pass)

        if result == True:
            messagebox.showinfo("Başarılı", "Şifreniz başarıyla değiştirildi.".center(100))
            self.ent_old_pass.delete(0, tk.END)
            self.ent_new_pass.delete(0, tk.END)
            self.ent_confirm_pass.delete(0, tk.END)
        else:
            messagebox.showerror("Hata", result.center(100))

    def do_logout(self):
        """Çıkış yapma işlemi"""
        if messagebox.askyesno("Çıkış", "Çıkış yapmak istediğinize emin misiniz?".center(100)):
            user_obj = self.get_user_object()
            result = log_out(user_obj)

            if result:
                self.window.destroy()
                from views.auth import AuthGUI
                AuthGUI()

    def do_delete_account(self):
        """Hesap silme işlemi"""
        if messagebox.askyesno("Hesap Silme", "Hesabınızı silmek istediğinize emin misiniz?\n\nBu işlem geri alınamaz!".center(100)):
            # İkinci onay
            if messagebox.askyesno("Son Uyarı", "Hesabınız kalıcı olarak silinecektir.\nDevam etmek istiyor musunuz?".center(100)):
                user_obj = self.get_user_object()
                result = delete_account(user_obj)

                if result:
                    messagebox.showinfo("Bilgi", "Hesabınız başarıyla silindi.".center(100))
                    self.window.destroy()
                    from views.auth import AuthGUI
                    AuthGUI()
                else:
                    messagebox.showerror("Hata", "Hesap silme işlemi başarısız oldu.".center(100))



