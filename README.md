# 🔐 Advanced Encryption Suite

An advanced GUI-based encryption tool built using **Python** and **Tkinter**, implementing both **classical** and **modern cryptographic techniques**.

This project combines **Caesar Cipher**, **AES-256 password-based encryption**, file encryption, brute-force analysis, logging, and theming into a single application.

---

## 🚀 Features

### 🔒 Cryptography
- Caesar Cipher (Full ASCII support)
- Brute-force Caesar decryption
- AES-256 encryption (password-based)
- Secure file encryption & decryption
- Integrity-checked decryption

### 🖥️ User Interface
- GUI built with Tkinter
- Dark / Light theme toggle
- Input validation with popup errors
- Clear All functionality

### 🛡️ Security Enhancements
- Password-derived AES key (SHA-256)
- Encrypted file output (`.aes`)
- Activity logging (`crypto_tool.log`)

---

## 🧠 How AES Works in This Project

- User enters a password
- Password is hashed using SHA-256
- Hash is converted into a 256-bit AES key
- AES encryption is performed using Fernet (AES + HMAC)
- Same password is required for decryption

## 📥 Clone the Repository

Use the following command to clone this repository:

```bash
git clone https://github.com/parthboghara/Advanced-Encryption-Suite.git
