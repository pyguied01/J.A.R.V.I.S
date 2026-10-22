```python
import tkinter as tk
from tkinter import ttk, messagebox
import socket
import subprocess
import platform
import threading
import ipaddress
import os
import re
import hashlib
import secrets
import string
from datetime import datetime

APP_NAME = "J.A.R.V.I.S. // CYBER SECURITY"

BG = "#07111D"
PANEL = "#0C1D2B"
BLUE = "#00C8FF"
GREEN = "#00FF9C"
ORANGE = "#FFB347"
RED = "#FF4C64"
WHITE = "#E6F7FF"


class JarvisSecurity:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry("1050x720")
        self.root.minsize(850, 600)
        self.root.configure(bg=BG)

        self.scanning = False
        self.devices = []

        self.build_ui()
        self.log("JARVIS wurde initialisiert.")
        self.log("Sicherheitsmodus: lokale, autorisierte Prüfungen.")
        self.log("System: " + platform.system() + " " + platform.release())

    def build_ui(self):
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", padx=24, pady=(20, 8))

        tk.Label(
            header,
            text="J.A.R.V.I.S.",
            font=("Consolas", 29, "bold"),
            fg=BLUE,
            bg=BG
        ).pack(side="left")

        tk.Label(
            header,
            text="CYBER SECURITY SYSTEM",
            font=("Consolas", 11),
            fg=GREEN,
            bg=BG
        ).pack(side="right", pady=12)

        tk.Label(
            self.root,
            text="NETWORK INTELLIGENCE  /  DEVICE AUDIT  /  SECURITY",
            font=("Consolas", 10),
            fg="#7899AE",
            bg=BG
        ).pack(anchor="w", padx=28, pady=(0, 14))

        self.status = tk.Label(
            self.root,
            text="● SYSTEM ONLINE",
            font=("Consolas", 11, "bold"),
            fg=GREEN,
            bg=BG
        )
        self.status.pack(anchor="w", padx=28, pady=(0, 12))

        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True, padx=20, pady=5)

        sidebar = tk.Frame(body, bg=PANEL, width=245)
        sidebar.pack(side="left", fill="y", padx=(0, 12))
        sidebar.pack_propagate(False)

        tk.Label(
            sidebar,
            text="COMMAND CENTER",
            font=("Consolas", 12, "bold"),
            fg=BLUE,
            bg=PANEL
        ).pack(anchor="w", padx=16, pady=(18, 14))

        self.button(sidebar, "NETWORK SCAN", self.network_scan)
        self.button(sidebar, "USB DEVICE CHECK", self.usb_check)
        self.button(sidebar, "ANDROID ADB CHECK", self.android_check)
        self.button(sidebar, "PASSWORD AUDIT", self.password_audit)
        self.button(sidebar, "GENERATE PASSWORD", self.generate_password)
        self.button(sidebar, "SYSTEM INFORMATION", self.system_info)
        self.button(sidebar, "CLEAR CONSOLE", self.clear_console)

        tk.Label(
            sidebar,
            text="AUTHORIZED TESTING ONLY",
            font=("Consolas", 8),
            fg=ORANGE,
            bg=PANEL
        ).pack(side="bottom", pady=18)

        main = tk.Frame(body, bg=BG)
        main.pack(side="left", fill="both", expand=True)

        cards = tk.Frame(main, bg=BG)
        cards.pack(fill="x", pady=(0, 12))

        self.device_card = self.card(cards, "DEVICES FOUND", "0")
        self.device_card.pack(side="left", fill="x", expand=True, padx=(0, 8))

        self.network_card = self.card(cards, "NETWORK STATUS", "READY")
        self.network_card.pack(side="left", fill="x", expand=True, padx=8)

        self.security_card = self.card(cards, "SECURITY MODE", "ACTIVE")
        self.security_card.pack(side="left", fill="x", expand=True, padx=(8, 0))

        tk.Label(
            main,
            text="SYSTEM CONSOLE",
            font=("Consolas", 12, "bold"),
            fg=BLUE,
            bg=BG
        ).pack(anchor="w", pady=(4, 8))

        self.console = tk.Text(
            main,
            bg="#030A10",
            fg=GREEN,
            insertbackground=WHITE,
            font=("Consolas", 10),
            relief="flat",
            wrap="word",
            padx=12,
            pady=12,
            height=20
        )
        self.console.pack(fill="both", expand=True)

        self.console.tag_config("error", foreground=RED)
        self.console.tag_config("info", foreground=BLUE)
        self.console.tag_config("warning", foreground=ORANGE)

        footer = tk.Label(
            self.root,
            text="JARVIS SECURITY SUITE  |  LOCAL DIAGNOSTICS  |  WINDOWS",
            font=("Consolas", 8),
            fg="#567487",
            bg=BG
        )
        footer.pack(pady=(4, 12))

    def button(self, parent, text, command):
        btn = tk.Button(
            parent,
            text="> " + text,
            command=command,
            bg="#102A3C",
            fg=WHITE,
            activebackground=BLUE,
            activeforeground=BG,
            font=("Consolas", 9, "bold"),
            relief="flat",
            anchor="w",
            padx=12,
            pady=11,
            cursor="hand2"
        )
        btn.pack(fill="x", padx=10, pady=4)

    def card(self, parent, title, value):
        frame = tk.Frame(parent, bg=PANEL, padx=12, pady=12)

        tk.Label(
            frame,
            text=title,
            font=("Consolas", 8),
            fg="#83A8BC",
            bg=PANEL
        ).pack(anchor="w")

        value_label = tk.Label(
            frame,
            text=value,
            font=("Consolas", 13, "bold"),
            fg=BLUE,
            bg=PANEL
        )
        value_label.pack(anchor="w", pady=(7, 0))

        frame.value_label = value_label
        return frame

    def update_card(self, card, value, color=BLUE):
        self.root.after(
            0,
            lambda: (
                card.value_label.config(text=str(value), fg=color)
            )
        )

    def log(self, text, tag=None):
        timestamp = datetime.now().strftime("%H:%M:%S")
        line = f"[{timestamp}] {text}\n"

        def append():
            self.console.insert("end", line, tag or "")
            self.console.see("end")

        if threading.current_thread() is threading.main_thread():
            append()
        else:
            self.root.after(0, append)

    def run_thread(self, function):
        if self.scanning:
            self.log("Ein Vorgang läuft bereits.", "warning")
            return

        self.scanning = True
        self.status.config(text="● ANALYSIS RUNNING", fg=ORANGE)

        def worker():
            try:
                function()
            except Exception as exc:
                self.log(f"Fehler: {exc}", "error")
            finally:
                self.root.after(0, self.finish_task)

        threading.Thread(target=worker, daemon=True).start()

    def finish_task(self):
        self.scanning = False
        self.status.config(text="● SYSTEM ONLINE", fg=GREEN)

    def network_scan(self):
        self.run_thread(self._network_scan)

    def _network_scan(self):
        self.log("Starte Netzwerkdiagnose ...", "info")

        # Ermittelt zunächst die lokale IPv4-Adresse.
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.connect(("192.0.2.1", 80))
                local_ip = sock.getsockname()[0]
        except OSError:
            self.log("Lokale IPv4-Adresse konnte nicht bestimmt werden.",
                     "error")
            return

        self.log(f"Lokale IPv4-Adresse: {local_ip}")

        # Aus Sicherheitsgründen wird nur das lokale /24-Netz geprüft.
        network = ipaddress.ip_network(
            local_ip + "/24", strict=False
        )

        self.log(f"Prüfe erreichbare Hosts in {network} ...")

        found = []

        # Begrenzt die Anzahl der geprüften Hosts.
        hosts = list(network.hosts())[:254]

        def check_host(ip):
            try:
                with socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM
                ) as sock:
                    sock.settimeout(0.25)
                    result = sock.connect_ex((str(ip), 80))

                # Ein offener Port 80 ist ein Hinweis auf einen
                # erreichbaren Webdienst, kein allgemeiner Gerätetest.
                if result == 0:
                    try:
                        hostname = socket.gethostbyaddr(str(ip))[0]
                    except (socket.herror, socket.gaierror, OSError):
                        hostname = "Hostname unbekannt"

                    found.append((str(ip), hostname))
            except OSError:
                pass

        threads = []

        for ip in hosts:
            if str(ip) == local_ip:
                continue

            thread = threading.Thread(
                target=check_host,
                args=(ip,),
                daemon=True
            )
            threads.append(thread)
            thread.start()

            # Begrenzte Parallelität.
            if len(threads) >= 40:
                for running in threads:
                    running.join()
                threads = []

        for running in threads:
            running.join()

        self.devices = found
        self.update_card(self.device_card, len(found), GREEN)
        self.update_card(self.network_card, "SCAN DONE", GREEN)

        self.log(
            f"Netzwerkdiagnose beendet. "
            f"{len(found)} Hosts mit offenem Port 80 gefunden."
        )

        if not found:
```
