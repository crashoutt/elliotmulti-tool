# Copyright (c) ElliotNiggerson (https://ElliotNiggerson.shop)
# See the file 'LICENSE' for copying permission
# ----------------------------------------------------------------------------------------------------------------------------------------------------------|
# EN: 
#     - Do not touch or modify the code below. If there is an error, please contact the owner, but under no circumstances should you touch the code.
#     - Do not resell this tool, do not credit it to yours.
# FR: 
#     - Ne pas toucher ni modifier le code ci-dessous. En cas d'erreur, veuillez contacter le propriétaire, mais en aucun cas vous ne devez toucher au code.
#     - Ne revendez pas ce tool, ne le créditez pas au vôtre.


import tkinter as tk
import re
from tkinter import ttk
from tkinter import scrolledtext, messagebox
from PIL import Image, ImageTk
import threading
import time
import random
import requests
from tkinter.simpledialog import askstring

label_style = {
    "fg": "white", 
    "bg": "black", 
    "font": ("Courier", 12)
}

entry_style = {
    "fg": "black", 
    "bg": "white", 
    "font": ("Courier", 12), 
    "insertbackground": "black"
}

stop_event = threading.Event()

def fake_console_output(console, ip, port, duration, cons, stop_event, progress_bar):
    start = time.time()
    elapsed = 0
    while elapsed < duration:
        if stop_event.is_set():
            console.insert(tk.END, "\n[!] Attack stopped.\n")
            console.see(tk.END)
            return
        ping = random.randint(50, 999)
        console.insert(tk.END, f"Pinging {ip}:{port} with {cons} connection(s) — {ping}ms\n")
        console.see(tk.END)
        time.sleep(0.2)
        elapsed = time.time() - start
        progress_bar['value'] = (elapsed / duration) * 100
        root.update_idletasks()
    
    console.insert(tk.END, "\n[+] Attack Finished (fake)\n")
    console.see(tk.END)
    progress_bar['value'] = 0

def start_attack():
    ip = ip_entry.get().strip()
    port = port_entry.get().strip()

    if not ip and not port:
        console.insert(tk.END, "[-] Please input IP address and port\n")
        return
    elif not ip:
        console.insert(tk.END, "[-] Please input IP address\n")
        return
    elif not port:
        console.insert(tk.END, "[-] Please input port\n")
        return

    if not is_valid_ip(ip):
        console.insert(tk.END, "[-] Invalid IP address format. Please input a valid IP address.\n")
        return
    if not port.isdigit() or not (1 <= int(port) <= 65535):
        console.insert(tk.END, "[-] Invalid port number. Please input a valid port (1-65535).\n")
        return

    try:
        duration = int(time_combo.get().replace("s", ""))
        cons = int(cons_combo.get())
    except ValueError:
        console.insert(tk.END, "[-] Invalid selection. Please pick valid values.\n")
        return

    start_button.config(state=tk.DISABLED)
    status_label.config(text="Attack in progress...")

    console.delete(1.0, tk.END)

    console.insert(tk.END, f"\n[~] Starting fake DDoS on {ip}:{port} for {duration}s using {cons} connection(s)...\n")
    stop_event.clear()
    threading.Thread(target=fake_console_output, args=(console, ip, port, duration, cons, stop_event, progress_bar), daemon=True).start()

def stop_attack():
    if messagebox.askyesno("Stop Attack", "Are you sure you want to stop the attack?"):
        stop_event.set()
        console.delete(1.0, tk.END)
        progress_bar['value'] = 0
        start_button.config(state=tk.NORMAL)
        status_label.config(text="Attack stopped.")

def is_valid_ip(ip):
    parts = ip.split(".")
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit():
            return False
        num = int(part)
        if not (0 <= num <= 255):
            return False
    return True

import random
import tkinter as tk

email_index = 0

def request_gov_mail():
    global email_index

    try:
        response = requests.get("https://pastebin.com/raw/rk3LcE9q")
        response.raise_for_status()
        gov_emails = response.text.splitlines()

        filtered_emails = [email.strip() for email in gov_emails if any(domain in email for domain in ["@DHS.gov", "@FBI.gov", "@CIA.gov", "@lapd.gov"])]

        if filtered_emails:
            if email_index < len(filtered_emails):
                email = filtered_emails[email_index]
                osint_console.insert(tk.END, f"Email Found: {email}\n")
                osint_console.see(tk.END)
                email_index += 1
            else:
                osint_console.insert(tk.END, "[-] No more emails found.\n")
                osint_console.see(tk.END)
                email_index = 0
        else:
            osint_console.insert(tk.END, "[-] No matching .gov emails found in the fetched data.\n")
            osint_console.see(tk.END)

    except requests.exceptions.RequestException as e:
        osint_console.insert(tk.END, f"[-] Error fetching .gov emails: {str(e)}\n")
        osint_console.see(tk.END)

def reset_email_request():
    global email_index
    email_index = 0
    osint_console.insert(tk.END, "\n[+] Ready to start requesting .gov emails again...\n")
    osint_console.see(tk.END)

def reset_email_request():
    global email_index
    email_index = 0
    gov_mail_button.config(state=tk.NORMAL)
    osint_console.insert(tk.END, "\n[+] Ready to start requesting .gov emails again...\n")
    osint_console.see(tk.END)

def request_edr():
    platform = platform_combo.get()
    if platform:
        username = askstring("Enter Username", f"Enter username for {platform}:")
        if username:
            osint_console.insert(tk.END, f"Requesting EDR data for {platform} user: {username}\n")
            osint_console.see(tk.END)
        else:
            osint_console.insert(tk.END, "[-] Username not provided.\n")
            osint_console.see(tk.END)
    else:
        osint_console.insert(tk.END, "[-] Please select a platform.\n")
        osint_console.see(tk.END)

def clear_osint_console():
    osint_console.delete(1.0, tk.END)

def mail_search():
    mail_address = mail_search_entry.get().strip()
    if mail_address:
        if "@" not in mail_address:
            osint_console.insert(tk.END, "[-] Please input @.\n")
        else:
            osint_console.insert(tk.END, f"Failed for mail address: {mail_address}\n")
        osint_console.see(tk.END)
    else:
        osint_console.insert(tk.END, "[-] Please enter a mail address to search.\n")
        osint_console.see(tk.END)

def format_phone_number(phone_number):
    phone_number = re.sub(r'\D', '', phone_number)
    if len(phone_number) > 10:
        phone_number = phone_number[:10]
    return f"{phone_number[:3]}-{phone_number[3:6]}-{phone_number[6:]}" if len(phone_number) == 10 else phone_number

def phone_search():
    phone_number = format_phone_number(phone_search_entry.get().strip())
    if phone_number and len(phone_number) == 12:
        osint_console.insert(tk.END, f"Searching for phone number: {phone_number}\n")
        osint_console.see(tk.END)
    else:
        osint_console.insert(tk.END, "[-] Please enter a valid 10-digit phone number.\n")
        osint_console.see(tk.END)

def on_phone_input_change(*args):
    current_value = phone_search_entry.get()
    formatted_value = format_phone_number(current_value)
    phone_search_entry.delete(0, tk.END)
    phone_search_entry.insert(0, formatted_value)

def go_to_osint_page():
    main_frame.pack_forget()
    osint_page.pack(fill="both", expand=True)

def go_back_to_main_page():
    osint_page.pack_forget()
    main_frame.pack(fill="both", expand=True)

root = tk.Tk()
root.title("fsociety DDoS Tool")
root.geometry("600x650")
root.configure(bg="black")

try:
    logo_img = Image.open("img/Fsociety.jpg")
    logo_img = logo_img.resize((550, 150), Image.LANCZOS)
    logo = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(root, image=logo, bg="black")
    logo_label.image = logo
    logo_label.pack(pady=10)
except Exception as e:
    print("Failed to load logo:", e)

main_frame = tk.Frame(root, bg="black")
main_frame.pack(fill="both", expand=True)

console = scrolledtext.ScrolledText(main_frame, bg="black", fg="lime", insertbackground="white", height=12, font=("Courier", 9))
console.pack(padx=10, pady=10, fill="both", expand=False)

status_label = tk.Label(main_frame, text="Status: Waiting for input...", fg="white", bg="black", font=("Courier", 10))
status_label.pack(pady=5)

frame = tk.Frame(main_frame, bg="black")
frame.pack(pady=10)

tk.Label(frame, text="IP Address: ", **label_style).grid(row=0, column=0, sticky="e", pady=8)
ip_entry = tk.Entry(frame, **entry_style)
ip_entry.grid(row=0, column=1, padx=8)

tk.Label(frame, text="Port: ", **label_style).grid(row=1, column=0, sticky="e", pady=8)
port_entry = tk.Entry(frame, **entry_style)
port_entry.grid(row=1, column=1, padx=8)

tk.Label(frame, text="Duration: ", **label_style).grid(row=2, column=0, sticky="e", pady=8)
time_combo = ttk.Combobox(frame, values=["5s", "10s", "15s", "20s", "30s", "60s"], **entry_style)
time_combo.set("10s")
time_combo.grid(row=2, column=1, padx=8)

tk.Label(frame, text="Connections: ", **label_style).grid(row=3, column=0, sticky="e", pady=8)
cons_combo = ttk.Combobox(frame, values=["1", "2", "5", "10", "50", "100"], **entry_style)
cons_combo.set("10")
cons_combo.grid(row=3, column=1, padx=8)

start_button = tk.Button(main_frame, text="Start Attack", bg="green", fg="white", font=("Courier", 12), command=start_attack)
start_button.pack(pady=10)

stop_button = tk.Button(main_frame, text="Stop Attack", bg="red", fg="white", font=("Courier", 12), command=stop_attack)
stop_button.pack(pady=10)

progress_bar = ttk.Progressbar(main_frame, length=400, mode="determinate")
progress_bar.pack(pady=10)

root.mainloop()
