import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet
import base64
import hashlib
import datetime

# ---------------- LOGGING ----------------
def log(action):
    with open("crypto_tool.log", "a") as f:
        f.write(f"[{datetime.datetime.now()}] {action}\n")


# ---------------- PASSWORD → KEY ----------------
def password_to_key(password):
    digest = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(digest)


# ---------------- CAESAR (FULL ASCII) ----------------
ASCII_START = 32
ASCII_END = 126
ASCII_RANGE = ASCII_END - ASCII_START + 1

def caesar(text, shift):
    result = ""
    for c in text:
        o = ord(c)
        if ASCII_START <= o <= ASCII_END:
            result += chr(ASCII_START + (o - ASCII_START + shift) % ASCII_RANGE)
        else:
            result += c
    return result


# ---------------- AES FUNCTIONS ----------------
def aes_encrypt(text, password):
    key = password_to_key(password)
    f = Fernet(key)
    return f.encrypt(text.encode()).decode()

def aes_decrypt(token, password):
    key = password_to_key(password)
    f = Fernet(key)
    return f.decrypt(token.encode()).decode()


# ---------------- GUI ACTIONS ----------------
def encrypt_caesar():
    try:
        if shift_entry.get().strip() == "":
            messagebox.showerror("Input Error", "Please enter a shift value")
            return

        t = input_box.get("1.0", tk.END)
        s = int(shift_entry.get())

        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, caesar(t, s))
        log("Caesar Encryption")

    except ValueError:
        messagebox.showerror("Input Error", "Shift value must be a number")


def decrypt_caesar():
    try:
        if shift_entry.get().strip() == "":
            messagebox.showerror("Input Error", "Please enter a shift value")
            return

        t = input_box.get("1.0", tk.END)
        s = int(shift_entry.get())

        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, caesar(t, -s))
        log("Caesar Decryption")

    except ValueError:
        messagebox.showerror("Input Error", "Shift value must be a number")


def brute_force():
    t = input_box.get("1.0", tk.END)
    output_box.delete("1.0", tk.END)
    for i in range(1, ASCII_RANGE):
        output_box.insert(tk.END, f"[Shift {i}] {caesar(t, -i)}\n")
    log("Caesar Brute Force")

def encrypt_aes():
    t = input_box.get("1.0", tk.END)
    p = password_entry.get()
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, aes_encrypt(t, p))
    log("AES Encryption")

def decrypt_aes():
    t = input_box.get("1.0", tk.END)
    p = password_entry.get()
    try:
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, aes_decrypt(t.strip(), p))
        log("AES Decryption")
    except:
        messagebox.showerror("Error", "Invalid password or data")

def encrypt_file():
    path = filedialog.askopenfilename()
    if not path: return
    p = password_entry.get()
    with open(path, "r", errors="ignore") as f:
        data = f.read()
    enc = aes_encrypt(data, p)
    with open(path + ".aes", "w") as f:
        f.write(enc)
    log("File Encrypted")
    messagebox.showinfo("Success", "File encrypted")

def decrypt_file():
    path = filedialog.askopenfilename()
    if not path: return
    p = password_entry.get()
    with open(path, "r") as f:
        data = f.read()
    dec = aes_decrypt(data, p)
    with open(path + ".dec", "w") as f:
        f.write(dec)
    log("File Decrypted")
    messagebox.showinfo("Success", "File decrypted")

def clear_all():
    input_box.delete("1.0", tk.END)
    output_box.delete("1.0", tk.END)
    shift_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    log("Cleared all fields")

# ---------------- THEME TOGGLE ----------------
dark = True
def toggle_theme():
    global dark
    dark = not dark
    bg = "#121212" if dark else "#FFFFFF"
    fg = "#00FFAA" if dark else "#000000"
    root.configure(bg=bg)
    for w in widgets:
        try:
            w.configure(bg=bg, fg=fg)
        except:
            pass


# ---------------- GUI ----------------
root = tk.Tk()
root.title("Advanced Encryption Suite")
root.geometry("850x700")
root.configure(bg="#121212")

widgets = []

def lbl(t):
    l = tk.Label(root, text=t, bg="#121212", fg="#00FFAA")
    l.pack(anchor="w", padx=20)
    widgets.append(l)

lbl("Input Text:")
input_box = tk.Text(root, height=6, bg="#1f1f1f", fg="white")
input_box.pack(fill="x", padx=20)
widgets.append(input_box)

lbl("Shift (Caesar):")
shift_entry = tk.Entry(root)
shift_entry.pack(padx=20)
widgets.append(shift_entry)

lbl("Password (AES):")
password_entry = tk.Entry(root, show="*")
password_entry.pack(padx=20)
widgets.append(password_entry)

frame = tk.Frame(root, bg="#121212")
frame.pack(pady=10)
widgets.append(frame)

buttons = [
    ("Encrypt Caesar", encrypt_caesar),
    ("Decrypt Caesar", decrypt_caesar),
    ("Brute Force", brute_force),
    ("Encrypt AES", encrypt_aes),
    ("Decrypt AES", decrypt_aes),
    ("Encrypt File", encrypt_file),
    ("Decrypt File", decrypt_file),
    ("Toggle Theme", toggle_theme),
    ("Clear All", clear_all)
]

for t, c in buttons:
    b = tk.Button(frame, text=t, command=c)
    b.pack(side="left", padx=5)
    widgets.append(b)

lbl("Output:")
output_box = tk.Text(root, height=12, bg="#1f1f1f", fg="white")
output_box.pack(fill="both", expand=True, padx=20)
widgets.append(output_box)

root.mainloop()
