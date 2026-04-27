import tkinter as tk
from tkinter import ttk, messagebox
from .cars import CarsGUI
from controls import *


class AuthGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Araç Kiralama - Giriş / Kayıt")

        self.WIDTH = 500
        self.HEIGHT = 500
        self.center_window(self.window, self.WIDTH, self.HEIGHT)
        self.window.configure(bg="#e8e8e8")

        style = ttk.Style()
        style.configure("TNotebook.Tab", padding=[20, 8], font=("Arial", 12))

        # =====================================================
        #  ANA MERKEZ KUTU (Card)
        # =====================================================
        container = tk.Frame(self.window, bg="white", bd=2, relief="groove")
        container.place(relx=0.5, rely=0.5, anchor="center", width=380, height=460)

        notebook = ttk.Notebook(container)
        notebook.pack(expand=True, fill="both", padx=20, pady=20)

        # =====================================================
        #  LOGIN TAB
        # =====================================================
        login_frame = tk.Frame(notebook, bg="white")
        notebook.add(login_frame, text="Giriş Yap")

        tk.Label(login_frame, text="Kullanıcı Adı / Email:", bg="white",
                 font=("Arial", 12)).pack(pady=(30, 8))
        self.login_name = self.rounded_entry(login_frame, "Kullanıcı Adı veya Email")


        tk.Label(login_frame, text="Şifre:", bg="white",
                 font=("Arial", 12)).pack(pady=(20, 8))
        self.login_password = self.rounded_password_entry(login_frame, "Şifre")


        btn_login = tk.Button(login_frame, text="Giriş Yap",
                  bg="#2196F3", fg="white", font=("Arial", 12), width=15,
                  command=self.login)
        btn_login.pack(pady=20, ipady=6)
        btn_login.bind("<Enter>", lambda e: btn_login.config(bg="#64B5F6"))
        btn_login.bind("<Leave>", lambda e: btn_login.config(bg="#2196F3"))

        btn_forgot = tk.Button(login_frame, text="Şifremi Unuttum",
                  bg="#FF9800", fg="white", font=("Arial", 11), width=15,
                  command=self.open_forgot_window)
        btn_forgot.pack(ipady=8)
        btn_forgot.bind("<Enter>", lambda e: btn_forgot.config(bg="#FFB74D"))
        btn_forgot.bind("<Leave>", lambda e: btn_forgot.config(bg="#FF9800"))

        # =====================================================
        #  REGISTER TAB
        # =====================================================
        register_frame = tk.Frame(notebook, bg="white")
        notebook.add(register_frame, text="Kayıt Ol")

        tk.Label(register_frame, text="Kullanıcı Adı:", bg="white",
                 font=("Arial", 12)).pack(pady=(12, 4))

        self.reg_name = self.rounded_entry(register_frame, "Kullanıcı adı")

        tk.Label(register_frame, text="Email:", bg="white",
                 font=("Arial", 12)).pack(pady=(12, 4))

        self.reg_email = self.rounded_entry(register_frame, "Email")

        tk.Label(register_frame, text="Şifre:", bg="white",
                 font=("Arial", 12)).pack(pady=(12, 4))

        self.reg_password = self.rounded_password_entry(register_frame, "Şifre")

        btn_register = tk.Button(register_frame, text="Kayıt Ol",
                  bg="#4CAF50", fg="white", font=("Arial", 12),
                  command=self.register)
        btn_register.pack(pady=30, ipadx=25, ipady=7)
        btn_register.bind("<Enter>", lambda e: btn_register.config(bg="#81C784"))
        btn_register.bind("<Leave>", lambda e: btn_register.config(bg="#4CAF50"))

        self.window.configure(bg="#e3f2fd")


        self.window.mainloop()

    def rounded_entry(self, parent, placeholder=""):
        
        canvas = tk.Canvas(parent, width=300, height=42,
                           bg="white", highlightthickness=0)
        canvas.pack(pady=0.000000001)

        # Yuvarlatılmış dikdörtgen (arka plan)
        x1, y1, x2, y2, r = 5, 5, 295, 37, 12
        canvas.create_arc(x1, y1, x1 + r, y1 + r, start=90, extent=90, fill="#f2f3f5", outline="#f2f3f5")
        canvas.create_arc(x2 - r, y1, x2, y1 + r, start=0, extent=90, fill="#f2f3f5", outline="#f2f3f5")
        canvas.create_arc(x1, y2 - r, x1 + r, y2, start=180, extent=90, fill="#f2f3f5", outline="#f2f3f5")
        canvas.create_arc(x2 - r, y2 - r, x2, y2, start=270, extent=90, fill="#f2f3f5", outline="#f2f3f5")
        canvas.create_rectangle(x1 + r / 2, y1, x2 - r / 2, y2, fill="#f2f3f5", outline="#f2f3f5")
        canvas.create_rectangle(x1, y1 + r / 2, x2, y2 - r / 2, fill="#f2f3f5", outline="#f2f3f5")

        entry = tk.Entry(canvas, font=("Arial", 11), bd=0, bg="#f2f3f5")
        entry.place(x=15, y=10, width=260)

        entry.insert(0, placeholder)
        entry.config(fg="#7c7c7c")

        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(fg="black")

        def on_focus_out(event):
            if entry.get() == "":
                entry.insert(0, placeholder)
                entry.config(fg="#7c7c7c")

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

        return entry

    def rounded_password_entry(self, parent, placeholder="Şifre"):

        canvas = tk.Canvas(parent, width=300, height=42,
                           bg="white", highlightthickness=0)
        canvas.pack(pady=0.00000001)

        # Yuvarlatılmış arka plan
        x1, y1, x2, y2, r = 5, 5, 295, 37, 12
        canvas.create_arc(x1, y1, x1 + r, y1 + r, start=90, extent=90, fill="#f2f3f5", outline="#f2f3f5")
        canvas.create_arc(x2 - r, y1, x2, y1 + r, start=0, extent=90, fill="#f2f3f5", outline="#f2f3f5")
        canvas.create_arc(x1, y2 - r, x1 + r, y2, start=180, extent=90, fill="#f2f3f5", outline="#f2f3f5")
        canvas.create_arc(x2 - r, y2 - r, x2, y2, start=270, extent=90, fill="#f2f3f5", outline="#f2f3f5")
        canvas.create_rectangle(x1 + r / 2, y1, x2 - r / 2, y2, fill="#f2f3f5", outline="#f2f3f5")
        canvas.create_rectangle(x1, y1 + r / 2, x2, y2 - r / 2, fill="#f2f3f5", outline="#f2f3f5")

        entry = tk.Entry(canvas, font=("Arial", 11), bd=0, bg="#f2f3f5", show="")  # show KAPALI
        entry.place(x=15, y=10, width=260)

        # Placeholder ekle
        entry.insert(0, placeholder)
        entry.config(fg="#7c7c7c")

        def on_focus_in(event):
            # Placeholder varsa temizle ve yıldız modu aç
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
            entry.config(fg="black", show="*")  # show AÇIK

        def on_focus_out(event):
            # Boş kaldıysa tekrar placeholder koy ve show kapat
            if entry.get() == "":
                entry.insert(0, placeholder)
                entry.config(fg="#7c7c7c", show="")

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

        return entry

    # =====================================================
    #  WINDOW CENTER
    # =====================================================
    def center_window(self, win, width, height):
        win.update_idletasks()
        sw = win.winfo_screenwidth()
        sh = win.winfo_screenheight()
        x = (sw // 2) - (width // 2)
        y = (sh // 2) - (height // 2)
        win.geometry(f"{width}x{height}+{x}+{y}")

    # =====================================================
    #  LOGIN
    # =====================================================
    def login(self):
        user = log_in(self.login_name.get(), self.login_password.get())
        if user != False:
            messagebox.showinfo("Başarılı", "Giriş yapıldı!".center(100))
            self.window.destroy()
            CarsGUI(user)
        else:
            messagebox.showwarning("Hata", "Kullanıcı adı veya şifre yanlış!")

    # =====================================================
    #  REGISTER
    # =====================================================

    # eledim
    def register(self):
        user = sign_in(self.reg_name.get(), self.reg_email.get(), self.reg_password.get())
        if user == True:
            messagebox.showinfo("Başarılı", "Kayıt tamamlandı!")
        else:
            messagebox.showerror("Hata", "Kayıt yapılamadı!",detail=user)

    # =====================================================
    #  FORGOT WINDOW
    # =====================================================
    def open_forgot_window(self):
        win = tk.Toplevel(self.window)
        win.title("Şifremi Unuttum")
        win.resizable(False, False)
        win.configure(bg="white")

        self.center_window(win, 350, 300)

        tk.Label(win, text="Email adresinizi girin:", bg="white",
                 font=("Arial", 12)).pack(pady=20)

        self.forgot_email = tk.Entry(win, font=("Arial", 12))
        self.forgot_email.pack(fill="x", padx=40, ipady=4)

        tk.Button(win, text="Gönder", font=("Arial", 12),
                  bg="#FF9800", fg="white",
                  command=self.forgot).pack(pady=20, ipadx=12, ipady=4)

    def forgot(self):
        send = sendmail(self.forgot_email.get())
        if send:
            messagebox.showinfo("Gönderildi", "Şifreniz mail ile gönderildi.")
        else:
            messagebox.showerror("Hata", "Mail bulunamadı!")