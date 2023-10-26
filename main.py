import tkinter as tk
import sqlite3  # db
import hashlib  # hashovanie
import time  # čas
import tkinter.ttk as ttk
import os  # na subory path
import shutil  # na kopirovanie suborov
import pickle
import sys
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
from datetime import datetime


class LoginApp:
    def __init__(self):
        self.root = tk.Tk()
        self.user_id = None
        self.root.attributes('-fullscreen', True)

        # Nastavenie obrázka ako pozadia
        background_image = Image.open("background.png")
        background_photo = ImageTk.PhotoImage(background_image)
        background_label = tk.Label(self.root, image=background_photo)
        background_label.image = background_photo
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Formulár
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=0.32 * self.root.winfo_screenheight())

        self.username_label = tk.Label(self.frame, text="Username:")
        self.username_label.grid(row=0, column=0, padx=10, pady=5)
        self.username_entry = tk.Entry(self.frame)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)

        self.password_label = tk.Label(self.frame, text="Password:")
        self.password_label.grid(row=1, column=0, padx=10, pady=5)
        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        self.login_button = tk.Button(self.frame, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

        self.username_entry.bind('<Return>', lambda event: self.login())  # citlivosť na enter
        self.password_entry.bind('<Return>', lambda event: self.login())  # citlivosť na enter

        self.center_window()  # Centrovanie okna

    def center_window(self):  # Centrovanie okna
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) + (window_height // 6)  # Odsadenie odhora
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    @staticmethod
    def get_id(username):
        conn = sqlite3.connect("userdata.db")
        cur = conn.cursor()

        cur.execute("SELECT id FROM userdata WHERE username = ?", (username,))
        result = cur.fetchone()

        conn.close()

        if result:
            return result[0]
        else:
            return None

    @staticmethod
    def is_admin(username):
        conn = sqlite3.connect("userdata.db")
        cur = conn.cursor()

        cur.execute("SELECT is_admin FROM userdata WHERE username = ?", (username,))
        result = cur.fetchone()

        conn.close()

        if result:
            return result[0]
        else:
            return None

    @staticmethod
    def get_meno(username):
        conn = sqlite3.connect("userdata.db")
        cur = conn.cursor()

        cur.execute("SELECT meno FROM userdata WHERE username = ?", (username,))
        result = cur.fetchone()

        conn.close()

        if result:
            return result[0]
        else:
            return None

    @staticmethod
    def get_priezvisko(username):
        conn = sqlite3.connect("userdata.db")
        cur = conn.cursor()

        cur.execute("SELECT priezvisko FROM userdata WHERE username = ?", (username,))
        result = cur.fetchone()

        conn.close()

        if result:
            return result[0]
        else:
            return None

    @staticmethod
    def get_krycie_meno(username):
        conn = sqlite3.connect("userdata.db")
        cur = conn.cursor()

        cur.execute("SELECT krycie_meno FROM userdata WHERE username = ?", (username,))
        result = cur.fetchone()

        conn.close()

        if result:
            return result[0]
        else:
            return None

    @staticmethod
    def get_username(krycie_meno):
        conn = sqlite3.connect("userdata.db")
        cur = conn.cursor()

        cur.execute("SELECT username FROM userdata WHERE krycie_meno = ?", (krycie_meno,))
        result = cur.fetchone()

        conn.close()

        if result:
            return result[0]
        else:
            return None

    def login(self):
        # ziskanie inputu
        username = self.username_entry.get()
        password = self.password_entry.get()

        # rozšifrované heslo
        hashed_password = hashlib.sha3_256(password.encode()).hexdigest()

        # pripojenie do db
        conn = sqlite3.connect("userdata.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM userdata WHERE username = ? AND password = ?", (username, hashed_password))
        result = cur.fetchone()

        conn.close()

        if result:
            self.user_id = self.get_id(username)
            if self.user_id:
                self.root.withdraw()
                self.welcome_page(username, self.user_id)
            else:
                messagebox.showerror("Chyba", "Používateľské meno nie je platné.")
        else:
            messagebox.showerror("Chyba", "Neplatné používateľské meno alebo heslo.")

    def animate_text(self, label, text):
        for i in range(len(text)):
            label.config(text=text[:i + 1])
            self.root.update()
            time.sleep(0.05)

    def open_profile(self, user_id):
        conn = sqlite3.connect("userdata.db")
        cur = conn.cursor()

        cur.execute("SELECT meno, priezvisko, krycie_meno, password, vek, vyska, vaha FROM userdata WHERE id = ?",
                    (user_id,))
        result = cur.fetchone()

        conn.close()

        if result:
            profile_window = tk.Toplevel(self.root)
            profile_window.title("Profil")

            # Vytvor vstupné polia pre heslo
            current_password_label = tk.Label(profile_window, text="Aktuálne heslo:")
            current_password_entry = tk.Entry(profile_window, show="*")

            new_password_label = tk.Label(profile_window, text="Nové heslo:")
            new_password_entry = tk.Entry(profile_window, show="*")

            repeat_password_label = tk.Label(profile_window, text="Zopakujte nové heslo:")
            repeat_password_entry = tk.Entry(profile_window, show="*")

            current_password_label.grid(row=1, column=0, sticky=tk.W)
            current_password_entry.grid(row=1, column=1)
            new_password_label.grid(row=2, column=0, sticky=tk.W)
            new_password_entry.grid(row=2, column=1)
            repeat_password_label.grid(row=3, column=0, sticky=tk.W)
            repeat_password_entry.grid(row=3, column=1)

            # Funkcia na uloženie zmien hesla
            def save_password_change():
                current_password = current_password_entry.get()
                new_password = new_password_entry.get()
                repeat_password = repeat_password_entry.get()

                # Skontroluj aktuálne heslo
                hashed_password = hashlib.sha3_256(current_password.encode()).hexdigest()
                if hashed_password != result[3]:
                    messagebox.showerror("Chyba", "Zadané aktuálne heslo nie je správne.")
                    return

                # Skontroluj nové heslo
                if new_password == current_password:
                    messagebox.showerror("Chyba", "Nové heslo sa musí líšiť od aktuálneho hesla.")
                    return

                if new_password != repeat_password:
                    messagebox.showerror("Chyba", "Nové heslo sa nezhoduje v oboch poliach.")
                    return

                # Aktualizuj heslo v databáze
                hashed_new_password = hashlib.sha3_256(new_password.encode()).hexdigest()
                conn = sqlite3.connect("userdata.db")
                cur = conn.cursor()
                cur.execute("UPDATE userdata SET password = ? WHERE id = ?", (hashed_new_password, user_id))
                conn.commit()
                conn.close()

                messagebox.showinfo("Informácia", "Heslo bolo úspešne zmenené.")

                profile_window.destroy()

            # Tlačidlo na uloženie zmien hesla
            save_password_button = tk.Button(profile_window, text="Uložiť zmeny hesla", command=save_password_change)
            save_password_button.grid(row=4, column=0, columnspan=2)

            # Vytvor tabuľku
            table = ttk.Treeview(profile_window)
            table["columns"] = ("meno", "priezvisko", "krycie_meno", "vek", "vyska", "vaha")
            table.column("#0", width=0, stretch=tk.NO)
            table.column("meno", width=100, anchor=tk.W)
            table.column("priezvisko", width=100, anchor=tk.W)
            table.column("krycie_meno", width=100, anchor=tk.W)
            table.column("vek", width=100, anchor=tk.W)
            table.column("vyska", width=100, anchor=tk.W)
            table.column("vaha", width=100, anchor=tk.W)

            table.heading("#0", text="")
            table.heading("meno", text="Meno")
            table.heading("priezvisko", text="Priezvisko")
            table.heading("krycie_meno", text="Krycie meno")
            table.heading("vek", text="Vek")
            table.heading("vyska", text="Výška")
            table.heading("vaha", text="Váha")

            # Vlož záznamy do tabuľky
            table.insert("", tk.END,
                         values=(result[0], result[1], result[2], result[4], result[5], result[6]))

            table.grid(row=0, column=0, columnspan=2)

        else:
            messagebox.showerror("Chyba", "Nepodarilo sa získať informácie o používateľovi.")

    def logout(self, welcome_root):
        welcome_root.destroy()  # Zatvorí vedľajšie okno
        self.root.deiconify()  # Odkryje hlavné okno
        self.username_entry.delete(0, tk.END)  # Vyprázdni vstupné pole pre meno
        self.password_entry.delete(0, tk.END)  # Vyprázdni vstupné pole pre heslo

    @staticmethod
    def load_profile_image(user_id):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_directory, "faces", "{user_id}.jpg".format(user_id=user_id))
        try:
            image = Image.open(image_path)
            image = image.resize((50, 50), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(image)
            return photo
        except FileNotFoundError:
            messagebox.showwarning("Chyba", "Chýba obrázok používateľa.")

    def display_current_time(self, content_frame):
        current_time_label = tk.Label(content_frame, font=("Arial", 48))
        current_time_label.pack(pady=50)

        current_date_label = tk.Label(content_frame, font=("Arial", 24))
        current_date_label.pack()

        def update_time():
            current_time = datetime.now().strftime("%H:%M:%S")
            current_date = datetime.now().strftime("%d.%m.%Y")
            current_time_label.config(text=current_time)
            current_date_label.config(text=current_date)
            self.root.after(1000, update_time)

        update_time()

    def show_colleagues(self):
        conn = sqlite3.connect("userdata.db")
        cur = conn.cursor()

        cur.execute("SELECT meno, priezvisko, stav FROM userdata ORDER BY priezvisko")
        result = cur.fetchall()

        conn.close()

        original_result = result.copy()  # Pôvodný výsledok pre resetovanie filtra

        # Vytvorenie tabuľky pre zobrazenie kolegov
        colleagues_window = tk.Toplevel(self.root)
        colleagues_window.title("Kolegovia")

        filter_frame = tk.Frame(colleagues_window)
        filter_frame.pack(pady=10)

        filter_label = tk.Label(filter_frame, text="Filtrovať podľa písmena:")
        filter_label.pack(side=tk.LEFT)

        # Vytvorenie funkcie pre filtrovanie podľa abecedy
        def filter_names():
            letter = filter_entry.get().strip().lower()
            filtered_result = [ro for ro in result if ro[0].lower().startswith(letter)]
            table.delete(*table.get_children())
            for r in filtered_result:
                table.insert("", tk.END, values=(r[0], r[1], r[2]))

        filter_entry = tk.Entry(filter_frame, width=10)
        filter_entry.pack(side=tk.LEFT)

        filter_button = tk.Button(filter_frame, text="Filtrovať", command=filter_names)
        filter_button.pack(side=tk.LEFT)

        # Vytvorenie riadku tlačidiel pre filtre
        button_row_frame = tk.Frame(colleagues_window)
        button_row_frame.pack(pady=10)

        # Vytvorenie funkcie pre filtrovanie podľa stavu "In office"
        def filter_in_office():
            filtered_result = [ro for ro in result if ro[2] == "In office"]
            table.delete(*table.get_children())
            for r in filtered_result:
                table.insert("", tk.END, values=(r[0], r[1], r[2]))

        in_office_button = tk.Button(button_row_frame, text="In office", command=filter_in_office)
        in_office_button.pack(side=tk.LEFT)

        # Vytvorenie funkcie pre filtrovanie podľa stavu "Out of office"
        def filter_out_of_office():
            filtered_result = [ro for ro in result if ro[2] == "Out of office"]
            table.delete(*table.get_children())
            for r in filtered_result:
                table.insert("", tk.END, values=(r[0], r[1], r[2]))

        out_of_office_button = tk.Button(button_row_frame, text="Out of office", command=filter_out_of_office)
        out_of_office_button.pack(side=tk.LEFT)

        # Vytvorenie funkcie pre filtrovanie podľa stavu "Secret"
        def filter_secret():
            filtered_result = [ro for ro in result if ro[2] == "Secret"]
            table.delete(*table.get_children())
            for r in filtered_result:
                table.insert("", tk.END, values=(r[0], r[1], r[2]))

        secret_button = tk.Button(button_row_frame, text="Secret", command=filter_secret)
        secret_button.pack(side=tk.LEFT)

        # Vytvorenie funkcie pre resetovanie filtra
        def reset_filter():
            nonlocal result
            result = original_result
            table.delete(*table.get_children())
            for r in result:
                table.insert("", tk.END, values=(r[0], r[1], r[2]))

        reset_button = tk.Button(button_row_frame, text="Reset", command=reset_filter)
        reset_button.pack(side=tk.LEFT)

        table = ttk.Treeview(colleagues_window)
        table["columns"] = ("meno", "priezvisko", "poloha")
        table.column("#0", width=0, stretch=tk.NO)
        table.column("meno", width=100, anchor=tk.W)
        table.column("priezvisko", width=100, anchor=tk.W)
        table.column("poloha", width=100, anchor=tk.W)

        table.heading("#0", text="")
        table.heading("meno", text="Meno")
        table.heading("priezvisko", text="Priezvisko")
        table.heading("poloha", text="Poloha")

        for row in result:
            table.insert("", tk.END, values=(row[0], row[1], row[2]))

        table.pack()

    def show_location(self):
        conn = sqlite3.connect("userdata.db")
        cur = conn.cursor()

        cur.execute("SELECT stav FROM userdata WHERE id = ?", (self.user_id,))
        result = cur.fetchone()

        if result:
            current_status = result[0]
            cur.execute("SELECT DISTINCT stav FROM userdata WHERE stav != ?", (current_status,))
            select_result = cur.fetchall()
            select_result = [item[0] for item in select_result]

            conn.close()

            if select_result:
                select_window = tk.Toplevel(self.root)
                select_window.title("Vyberte stav")

                # Pridaný výpis aktuálnej polohy nad označením
                current_status_label = tk.Label(select_window, text="Aktuálna poloha: " + current_status)
                current_status_label.pack(pady=10)

                select_var = tk.StringVar(select_window)
                select_var.set(current_status)  # Nastaví hodnotu na prvý stav v zozname

                select_option_menu = tk.OptionMenu(select_window, select_var, *select_result)  # select stavov
                select_option_menu.pack(pady=10)

                def change_location():
                    selected_status = select_var.get()
                    user_id = self.get_id(self.username_entry.get())

                    if user_id:
                        conn = sqlite3.connect("userdata.db")
                        cur = conn.cursor()

                        cur.execute("UPDATE userdata SET stav = ? WHERE id = ?", (selected_status, user_id))
                        conn.commit()

                        conn.close()
                        select_window.destroy()

                    else:
                        messagebox.showerror("Chyba", "Nepodarilo sa nájsť ID")

                change_button = tk.Button(select_window, text="Zmeniť polohu", command=change_location)
                change_button.pack(pady=10)
            else:
                messagebox.showinfo("Error")
        else:
            messagebox.showerror("Chyba", "Nepodarilo sa získať aktuálnu polohu.")

    @staticmethod
    def create_message_database(file_path):
        if not os.path.exists(file_path):
            messages = []

            with open(file_path, 'wb+') as file:
                pickle.dump(messages, file)

    def spravy(self):
        username = self.username_entry.get()
        file_path = 'message_database.dat'
        self.create_message_database(file_path)

        select_window = tk.Toplevel(self.root)
        select_window.title("Správy")

        # Vytvoríme textové pole pre výpis obsahu
        text_box = tk.Text(select_window)
        text_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Vytvoríme scrollbar
        scrollbar = tk.Scrollbar(select_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Pripojíme scrollbar k textovému poľu
        text_box.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=text_box.yview)

        # Otvoríme súbor a vypíšeme jeho obsah do textového poľa
        with open(file_path, 'rb') as file:
            messages = pickle.load(file)
            for message in messages:
                text_box.insert(tk.END, message + '\n')

        # Posunie scrollbar na najnižšiu pozíciu
        text_box.see(tk.END)

        input_entry = tk.Entry(select_window)
        input_entry.pack()
        input_entry.focus()  # Zameriame sa na vstupné pole

        def posli_spravu():
            sprava = input_entry.get()

            if sprava:  # Kontrola, či je správa neprázdna
                krycie_meno = self.get_krycie_meno(username)  # Získanie krycieho mena
                current_date = datetime.now().strftime("[%d.%m.%Y]")
                current_time = datetime.now().strftime("[%H:%M:%S]")
                formatted_message = "{} {} Agent {} : {}".format(current_date, current_time, krycie_meno, sprava)

                # Otvoríme súbor a pridáme novú správu
                with open(file_path, 'rb') as file:
                    messages = pickle.load(file)
                    messages.append(formatted_message)

                with open(file_path, 'wb') as file:
                    pickle.dump(messages, file)

                select_window.destroy()  # Zatvoríme okno
                self.spravy()  # Otvoríme okno znova pre aktualizáciu obsahu suboru

        def on_enter(event):
            posli_spravu()

        # Pridáme spracovanie udalosti pre stlačenie klávesy Enter
        input_entry.bind('<Return>', on_enter)

        send_button = tk.Button(select_window, text="Pošli správu", command=posli_spravu)
        send_button.pack()

        # Spustíme metódu posli_spravu() pri vstupe do vstupného poľa
        input_entry.focus_set()
        posli_spravu()

    def pridaj_pouzivatela(self):
        # Vytvor nové okno pre pridanie používateľa
        pridaj_pouzivatela_window = tk.Toplevel(self.root)
        pridaj_pouzivatela_window.title("Pridaj používateľa")

        # Vytvor vstupné polia pre meno, priezvisko, stav
        meno_label = tk.Label(pridaj_pouzivatela_window, text="Meno:")
        meno_entry = tk.Entry(pridaj_pouzivatela_window)
        meno_label.grid(row=0, column=0, padx=10, pady=5)
        meno_entry.grid(row=0, column=1, padx=10, pady=5)

        priezvisko_label = tk.Label(pridaj_pouzivatela_window, text="Priezvisko:")
        priezvisko_entry = tk.Entry(pridaj_pouzivatela_window)
        priezvisko_label.grid(row=1, column=0, padx=10, pady=5)
        priezvisko_entry.grid(row=1, column=1, padx=10, pady=5)

        username_label = tk.Label(pridaj_pouzivatela_window, text="Username:")
        username_entry = tk.Entry(pridaj_pouzivatela_window)
        username_label.grid(row=3, column=0, padx=10, pady=5)
        username_entry.grid(row=3, column=1, padx=10, pady=5)

        heslo_label = tk.Label(pridaj_pouzivatela_window, text="Heslo:")
        heslo_entry = tk.Entry(pridaj_pouzivatela_window, show="*")
        heslo_label.grid(row=4, column=0, padx=10, pady=5)
        heslo_entry.grid(row=4, column=1, padx=10, pady=5)

        kmeno_label = tk.Label(pridaj_pouzivatela_window, text="Krycie meno:")
        kmeno_entry = tk.Entry(pridaj_pouzivatela_window)
        kmeno_label.grid(row=5, column=0, padx=10, pady=5)
        kmeno_entry.grid(row=5, column=1, padx=10, pady=5)

        vek_label = tk.Label(pridaj_pouzivatela_window, text="Vek:")
        vek_entry = tk.Entry(pridaj_pouzivatela_window)
        vek_label.grid(row=6, column=0, padx=10, pady=5)
        vek_entry.grid(row=6, column=1, padx=10, pady=5)

        vyska_label = tk.Label(pridaj_pouzivatela_window, text="Výška:")
        vyska_entry = tk.Entry(pridaj_pouzivatela_window)
        vyska_label.grid(row=7, column=0, padx=10, pady=5)
        vyska_entry.grid(row=7, column=1, padx=10, pady=5)

        vaha_label = tk.Label(pridaj_pouzivatela_window, text="Váha:")
        vaha_entry = tk.Entry(pridaj_pouzivatela_window)
        vaha_label.grid(row=8, column=0, padx=10, pady=5)
        vaha_entry.grid(row=8, column=1, padx=10, pady=5)

        pozicia_label = tk.Label(pridaj_pouzivatela_window, text="Pracovná pozícia:")
        pozicia_entry = tk.Entry(pridaj_pouzivatela_window)
        pozicia_label.grid(row=9, column=0, padx=10, pady=5)
        pozicia_entry.grid(row=9, column=1, padx=10, pady=5)

        kosoba_label = tk.Label(pridaj_pouzivatela_window, text="Kontaktná osoba:")
        kosoba_entry = tk.Entry(pridaj_pouzivatela_window)
        kosoba_label.grid(row=10, column=0, padx=10, pady=5)
        kosoba_entry.grid(row=10, column=1, padx=10, pady=5)

        narodenie_label = tk.Label(pridaj_pouzivatela_window, text="Miesto narodenia:")
        narodenie_entry = tk.Entry(pridaj_pouzivatela_window)
        narodenie_label.grid(row=11, column=0, padx=10, pady=5)
        narodenie_entry.grid(row=11, column=1, padx=10, pady=5)

        bydlisko_label = tk.Label(pridaj_pouzivatela_window, text="Trvalé bydlisko:")
        bydlisko_entry = tk.Entry(pridaj_pouzivatela_window)
        bydlisko_label.grid(row=12, column=0, padx=10, pady=5)
        bydlisko_entry.grid(row=12, column=1, padx=10, pady=5)

        admin_label = tk.Label(pridaj_pouzivatela_window, text="Admin:")
        admin_var = tk.StringVar()
        admin_checkbox1 = tk.Checkbutton(pridaj_pouzivatela_window, text="Áno", variable=admin_var, onvalue="Áno",
                                         offvalue="")
        admin_checkbox2 = tk.Checkbutton(pridaj_pouzivatela_window, text="Nie", variable=admin_var, onvalue="Nie",
                                         offvalue="")
        admin_label.grid(row=13, column=0, padx=10, pady=5)
        admin_checkbox1.grid(row=13, column=1, padx=10, pady=5)
        admin_checkbox2.grid(row=13, column=2, padx=10, pady=5)

        def skopirovat_subor():
            file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg")])
            if file_path:
                destination_path = "faces/obrazok.jpg"
                shutil.copy(file_path, destination_path)

        def rename(idc):
            priecinok = "faces/"
            idcko = str(idc)
            prepona = ".jpg"
            name = priecinok + idcko + prepona
            destination_path = "faces/obrazok.jpg"
            os.rename(destination_path, name)

        obrazok_button = tk.Button(pridaj_pouzivatela_window, text="Vyber obrázok (iba .jpg)", command=skopirovat_subor)
        obrazok_button.grid(row=14, column=0, columnspan=3, padx=10, pady=5)

        # Tlačidlo pre uloženie používateľa
        ulozit_button = tk.Button(pridaj_pouzivatela_window, text="Pridaj používateľa",
                                  command=lambda: uloz_pouzivatela(meno_entry.get(), priezvisko_entry.get(),
                                                                   username_entry.get(), heslo_entry.get(),
                                                                   kmeno_entry.get(), vek_entry.get(),
                                                                   vyska_entry.get(), vaha_entry.get(),
                                                                   pozicia_entry.get(), kosoba_entry.get(),
                                                                   narodenie_entry.get(), bydlisko_entry.get(),
                                                                   admin_var.get()))
        ulozit_button.grid(row=15, column=0, columnspan=3, padx=10, pady=5)

        def uloz_pouzivatela(meno, priezvisko, username, heslo, kmeno, vek, vyska, vaha, pozicia, kosoba, narodenie,
                             bydlisko, admin):
            # Kontrola mena a priezviska
            if not (meno.isalpha() and priezvisko.isalpha()):
                messagebox.showerror("Chyba", "Meno a priezvisko musia obsahovať iba písmena.")
                return

            if len(meno) < 2 or len(priezvisko) < 2:
                messagebox.showerror("Chyba", "Meno a priezvisko musia mať aspoň 2 znaky.")
                return

            # Kontrola username
            db = sqlite3.connect("userdata.db")
            cursor = db.cursor()
            cursor.execute("SELECT * FROM userdata WHERE username=?", (username,))
            result = cursor.fetchone()
            if result:
                messagebox.showerror("Chyba", "Zadaný username už existuje.")
                return

            # Kontrola hesla
            if len(heslo) < 4:
                messagebox.showerror("Chyba", "Heslo musí mať aspoň 4 znaky.")
                return

            password = hashlib.sha3_256(heslo.encode()).hexdigest()

            # Kontrola krycieho mena
            cursor.execute("SELECT * FROM userdata WHERE krycie_meno=?", (kmeno,))
            result = cursor.fetchone()
            if result:
                messagebox.showerror("Chyba", "Zadané krycie meno už existuje.")
                return

            # Kontrola veku, vysky a vahy
            try:
                vek = int(vek)
                vyska = int(vyska)
                vaha = int(vaha)
                if not (18 <= vek <= 60 and 150 <= vyska <= 230 and 50 <= vaha <= 140):
                    messagebox.showerror("Chyba", "Zadajte platné hodnoty pre vek, výšku a váhu.")
                    return
            except ValueError:
                messagebox.showerror("Chyba", "Vek, výška a váha musia byť čísla.")
                return

            # Kontrola pracovnej pozicie a kontaktnych osob
            if not (pozicia.replace(" ", "").isalpha() and kosoba.replace(" ", "").isalpha()):
                messagebox.showerror("Chyba", "Pracovná pozícia a kontaktná osoba musia obsahovať iba písmena.")
                return

            if len(pozicia) < 3:
                messagebox.showerror("Chyba", "Pracovná pozícia musí obsahovať viac ako 2 znaky")
                return

            # Kontrola miesta narodenia a trvaleho bydliska
            if len(narodenie) < 5 or len(bydlisko) < 5:
                messagebox.showerror("Chyba", "Miesto narodenia a trvalé bydlisko musia mať aspoň 5 znakov.")
                return

            # Kontrola admin hodnoty
            if admin not in ["Áno", "Nie"]:
                messagebox.showerror("Chyba", "Nezvolená hodnota pre admin")
                return

            if admin == "Áno":
                adminn = 1
            else:
                adminn = 0

            # Všetky kontroly prebehli úspešne, ulož používateľa do databázy
            cursor.execute(
                "INSERT INTO userdata (username, password, meno, priezvisko, is_admin, krycie_meno, vyska, vaha, stav, pozicia, kontaktna_osoba, vek, miesto_narodenia, bydlisko) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (username, password, meno, priezvisko, adminn, kmeno, vyska, vaha, 'In office', pozicia, kosoba, vek,
                 narodenie, bydlisko))
            db.commit()
            idcko = self.get_id(username)
            rename(idcko)
            db.close()

            pridaj_pouzivatela_window.destroy()

    def vymaz(self):
        # Vytvorenie nového okna
        vymaz_window = tk.Toplevel(self.root)
        vymaz_window.title("Vymaž používateľa")

        select_var = tk.StringVar()
        select_var.set("-")

        # Pripojenie k databáze
        conn = sqlite3.connect('userdata.db')
        cursor = conn.cursor()

        # Získanie dostupných krycích mien z databázy
        cursor.execute("SELECT krycie_meno FROM userdata")
        results = cursor.fetchall()

        message = tk.Label(vymaz_window, text="Vyber agenta na vymazanie :\n")
        message.pack()

        # Naplnenie OptionMenu dostupnými krycími menami
        select_menu = tk.OptionMenu(vymaz_window, select_var, *results)
        select_menu.pack()

        messagee = tk.Label(vymaz_window, text="")
        messagee.pack()

        def delete_user():
            username = select_var.get()

            us = ""
            for znak in username:
                if znak.isalpha() or znak.isdigit():
                    us += znak
            user = self.get_username(us)
            user_id = self.get_id(user)

            # Vymazanie riadku s daným user_id
            cursor.execute("DELETE FROM userdata WHERE id=?", (user_id,))
            conn.commit()

            cursor.close()
            conn.close()

            # Výpis informácie o vymazaní užívateľa
            messagebox.showinfo("Informácia", "Uživateľ bol uspešné vymazaný.")
            vymaz_window.destroy()
            path = f"faces/{user_id}.jpg"
            os.remove(path)

        vymaz_button = tk.Button(vymaz_window, text="Vymaž", command=delete_user)
        vymaz_button.pack()

    def dochadzka(self):
        now = datetime.now()
        aktualny_den = now.day
        aktualny_mesiac = now.month
        aktualny_rok = now.year
        username = self.username_entry.get()
        meno = self.get_meno(username)
        priezvisko = self.get_priezvisko(username)
        krycie_meno = self.get_krycie_meno(username)
        id = self.get_id(username)

        pole = []

        select_var = tk.StringVar()
        select_var.set(f"{aktualny_den}.{aktualny_mesiac}.{aktualny_rok}")

        for cislo in range(1, aktualny_den + 1):
            retazec = str(cislo) + "." + str(aktualny_mesiac) + "." + str(aktualny_rok)
            pole.append(retazec)

        dochadzka_window = tk.Toplevel(self.root)
        dochadzka_window.title("Dochádzka")

        datum_label = tk.Label(dochadzka_window, text="Dátum: ")
        dochadzka_menu = tk.OptionMenu(dochadzka_window, select_var, *pole)
        datum_label.grid(row=1, column=0, padx=10, pady=5)
        dochadzka_menu.grid(row=1, column=1, padx=10, pady=5)

        hodiny_label = tk.Label(dochadzka_window, text="Počet hodin: ")
        hodiny_label.grid(row=3, column=0, padx=10, pady=5)
        hodiny_var = tk.StringVar()
        hodiny_entry = tk.Entry(dochadzka_window, textvariable=hodiny_var, width=10)
        hodiny_entry.grid(row=3, column=1, padx=10, pady=5)

        poslat_button = tk.Button(dochadzka_window, text="Poslať / aktualizovať", command=lambda: poslat_dochadzku(meno, priezvisko, krycie_meno, select_var.get(), hodiny_var.get()))
        poslat_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

        # Nastavenie rozťahovateľnosti riadkov a stĺpcov
        dochadzka_window.grid_rowconfigure(0, weight=1)
        dochadzka_window.grid_columnconfigure(0, weight=1)
        dochadzka_window.grid_columnconfigure(1, weight=1)

        def poslat_dochadzku(meno, priezvisko, krycie_meno, datum, hodiny):
            # Kontrola vstupu hodín
            try:
                hodiny_cislo = int(hodiny)
                if 0 < hodiny_cislo < 25:
                    # Kontrola, či riadok už existuje v tabuľke
                    connection = sqlite3.connect("userdata.db")
                    cursor = connection.cursor()

                    cursor.execute(
                        "SELECT * FROM dochadzka WHERE meno = ? AND priezvisko = ? AND krycie_meno = ? AND datum = ?",
                        (meno, priezvisko, krycie_meno, datum))
                    existing_row = cursor.fetchone()

                    if existing_row:
                        # Riadok existuje, takže updatujeme stĺpec pocet_hodin
                        cursor.execute("UPDATE dochadzka SET pocet_hodin = ? WHERE datum = ?", (hodiny, datum))
                        messagebox.showinfo("Aktualizácia", "Riadok bol aktualizovaný.")
                    else:
                        # Riadok neexistuje, takže ho pridáme do tabuľky
                        cursor.execute(
                            "INSERT INTO dochadzka (id_pouzivatela, meno, priezvisko, krycie_meno, datum, pocet_hodin) VALUES (?, ?, ?, ?, ?, ?)",
                            (id, meno, priezvisko, krycie_meno, datum, hodiny))
                        messagebox.showinfo("Pridanie", "Riadok bol pridaný.")

                    connection.commit()
                    connection.close()
                    dochadzka_window.destroy()
                else:
                    messagebox.showerror("Chyba", "Zadajte číslo musí byť v rozmedzí 1-24")
            except ValueError:
                messagebox.showerror("Chyba", "Zadajte platné číslo pre počet hodín.")

    def akcie(self):
        akcie_window = tk.Toplevel(self.root)
        akcie_window.title("Akcie")

        username = self.username_entry.get()
        id = self.get_id(username)
        krycie_meno = self.get_krycie_meno(username)

        akcie_label = tk.Label(akcie_window, text="Názov akcie: ")
        akcie_entry = tk.Entry(akcie_window, width=20)
        akcie_label.grid(row=1, column=0, padx=10, pady=5)
        akcie_entry.grid(row=1, column=1, padx=10, pady=5)

        ucastnici_label = tk.Label(akcie_window, text="Účastníci: ")
        ucastnici_entry = tk.Entry(akcie_window, width=20)
        ucastnici_label.grid(row=2, column=0, padx=10, pady=5)
        ucastnici_entry.grid(row=2, column=1, padx=10, pady=5)

        miesto_label = tk.Label(akcie_window, text="Miesto: ")
        miesto_entry = tk.Entry(akcie_window, width=20)
        miesto_label.grid(row=3, column=0, padx=10, pady=5)
        miesto_entry.grid(row=3, column=1, padx=10, pady=5)

        msledovani_label = tk.Label(akcie_window, text="Mená sledovaných: ")
        msledovani_entry = tk.Entry(akcie_window, width=20)
        msledovani_label.grid(row=4, column=0, padx=10, pady=5)
        msledovani_entry.grid(row=4, column=1, padx=10, pady=5)

        datum_label = tk.Label(akcie_window, text="Dátum akcie (od-do): ")
        datum_entry = tk.Entry(akcie_window, width=20)
        datum_label.grid(row=5, column=0, padx=10, pady=5)
        datum_entry.grid(row=5, column=1, padx=10, pady=5)

        def pridaj_akciu():
            nazov_akcie = akcie_entry.get()
            ucastnici = ucastnici_entry.get()
            miesto = miesto_entry.get()
            sledovani = msledovani_entry.get()
            datum = datum_entry.get()

            # Kontrola, či je názov akcie prázdny
            if not nazov_akcie:
                messagebox.showerror("Chyba", "Názov akcie nemôže byť prázdny.")
                return

            # Pripojenie k databáze
            connection = sqlite3.connect("userdata.db")
            cursor = connection.cursor()

            # Kontrola, či existuje akcia s daným názvom
            cursor.execute("SELECT * FROM akcie WHERE nazov_akcie = ?", (nazov_akcie,))
            existing_row = cursor.fetchone()

            if existing_row:
                # Aktualizácia existujúceho riadku
                cursor.execute("""
                    UPDATE akcie SET id_pouzivatela = ?, krycie_meno = ?, ucastnici = ?, miesto = ?, okruh_sledovanych = ?, datum_od_do = ?
                    WHERE nazov_akcie = ?
                """, (id, krycie_meno, ucastnici, miesto, sledovani, datum, nazov_akcie))
                messagebox.showinfo("Úspech", "Akcia bola aktualizovaná v databáze.")
            else:
                # Vloženie nového riadku
                cursor.execute("""
                    INSERT INTO akcie (id_pouzivatela, krycie_meno, nazov_akcie, ucastnici, miesto, okruh_sledovanych, datum_od_do)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (id, krycie_meno, nazov_akcie, ucastnici, miesto, sledovani, datum))
                messagebox.showinfo("Úspech", "Akcia bola úspešne pridaná do databázy.")

            connection.commit()
            connection.close()
            akcie_window.destroy()

        pridaj_button = tk.Button(akcie_window, text="Pridaj akciu", command=pridaj_akciu)
        pridaj_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    def welcome_page(self, meno, user_id):
        def create_sidebar(root):
            sidebar_frame = tk.Frame(root, bg="gray", width=200)
            sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

            photo = self.load_profile_image(user_id)

            if photo is not None:
                profile_button = tk.Button(sidebar_frame, image=photo, command=lambda: self.open_profile(user_id))
                profile_button.image = photo
                profile_button.pack(pady=10)
            else:
                messagebox.showwarning("Chyba", "Chýba obrázok používateľa.")

            colleagues_button = tk.Button(sidebar_frame, text="Kolegovia", command=self.show_colleagues, width=10)
            colleagues_button.pack(pady=10)

            dochadzka_button = tk.Button(sidebar_frame, text="Docházka", command=self.dochadzka, width=10)
            dochadzka_button.pack(pady=10)

            location_button = tk.Button(sidebar_frame, text="Poloha", command=self.show_location, width=10)
            location_button.pack(pady=10)

            spravy_button = tk.Button(sidebar_frame, text="Správy", command=self.spravy, width=10)
            spravy_button.pack(pady=10)

            akcie_button = tk.Button(sidebar_frame, text="Akcie", command=self.akcie, width=10)
            akcie_button.pack(pady=10)

            if self.is_admin(meno) == 1:
                pridaj_button = tk.Button(sidebar_frame, text="Pridaj", command=self.pridaj_pouzivatela, width=10)
                pridaj_button.pack(pady=10)

                vymaz_button = tk.Button(sidebar_frame, text="Vymaž", command=self.vymaz, width=10)
                vymaz_button.pack(pady=10)

            logout_button = tk.Button(sidebar_frame, text="Odhlásiť sa", command=lambda: self.logout(welcome_root), width=10)
            logout_button.pack(side=tk.BOTTOM, pady=20)

            def shutdown_program():
                self.root.destroy()
                sys.exit()

            vypnut_button = tk.Button(sidebar_frame, text="Vypnúť", command=shutdown_program, width=10)
            vypnut_button.pack(side=tk.BOTTOM, pady=20)

        welcome_root = tk.Toplevel(self.root)
        welcome_root.attributes('-fullscreen', True)

        create_sidebar(welcome_root)

        # Content
        content_frame = tk.Frame(welcome_root, bg="white", width=500)
        content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        welcome_label = tk.Label(content_frame, font=("Arial", 24),
                                 text=f"Vitajte v systéme FBI, agent {self.get_krycie_meno(meno)}!")
        welcome_label.pack(pady=100)

        mini_logo = Image.open("mini_logo.png")
        mini_logo = mini_logo.resize((200, 200), Image.ANTIALIAS)

        mini_logo_label = tk.Label(content_frame)
        mini_logo_label.pack(pady=10)

        def animate_logo(idx=0):
            if idx < mini_logo.height:
                row = mini_logo.crop((0, 0, mini_logo.width, idx + 1))
                row_photo = ImageTk.PhotoImage(row)
                mini_logo_label.config(image=row_photo)
                mini_logo_label.image = row_photo
                idx += 1
                mini_logo_label.after(10, lambda: animate_logo(idx))

        animate_logo()

        self.animate_text(welcome_label, f"Vitajte v systéme FBI, agent {self.get_krycie_meno(meno)}!")

        self.display_current_time(content_frame)

    def run(self):
        self.root.mainloop()


app = LoginApp()
app.run()
