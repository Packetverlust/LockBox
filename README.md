<div align="center">

<img src="https://img.shields.io/badge/-LockBox-0d1117?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0iIzU4YTZmZiIgZD0iTTEyIDFMMy41IDUuNXYxMWMwIDQuNDIgMy41OCA3Ljk5IDguNSA3LjVzOC41LTMuMDggOC41LTcuNVY1LjVMMTIgMXptMCA0YTMgMyAwIDEgMSAwIDYgMyAzIDAgMCAxIDAtNnoiLz48L3N2Zz4=&logoColor=58a6ff" />

# 🔐 LockBox

**Encrypted local password manager. Your passwords never leave your machine.**

[![Release](https://img.shields.io/github/v/release/yourname/lockbox?style=flat-square&color=388bfd&label=latest)](https://github.com/yourname/lockbox/releases)
[![Windows](https://img.shields.io/badge/Windows-0078D6?style=flat-square&logo=windows&logoColor=white)](https://github.com/yourname/lockbox/releases)
[![Linux](https://img.shields.io/badge/Linux-FCC624?style=flat-square&logo=linux&logoColor=black)](https://github.com/yourname/lockbox/releases)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-3fb950?style=flat-square)](LICENSE)
[![Docs](https://img.shields.io/badge/Docs-GitBook-58a6ff?style=flat-square&logo=gitbook&logoColor=white)](https://yourname.gitbook.io/lockbox)

<br/>

<img src="https://raw.githubusercontent.com/yourname/lockbox/main/extra/demo.gif" alt="LockBox demo" width="700"/>

</div>

---

## ✨ Why LockBox?

| | LockBox | Cloud managers |
|---|---|---|
| **Your data stays local** | ✅ Always | ❌ Synced to servers |
| **Works offline** | ✅ Always | ❌ Needs internet |
| **Open source** | ✅ Auditable | ⚠️ Often closed |
| **Argon2id encryption** | ✅ Memory-hard | ⚠️ Varies |
| **No account needed** | ✅ Never | ❌ Required |
| **TUI + CLI** | ✅ Both | ❌ Usually neither |

---

## 🚀 Install

### Windows

```powershell
irm https://raw.githubusercontent.com/yourname/lockbox/main/install.ps1 | iex
```

### Linux

```bash
curl -fsSL https://raw.githubusercontent.com/yourname/lockbox/main/install.sh | bash
```

Or grab the binary directly from [**Releases**](https://github.com/yourname/lockbox/releases).

---

## 🖥️ Two ways to use it

### Visual interface — start here if you're new

```
lockbox ui
```

Opens a full terminal UI. Create your vault, add passwords, copy them to clipboard — no commands needed.

<img src="https://raw.githubusercontent.com/yourname/lockbox/main/extra/tui.png" alt="LockBox TUI" width="650"/>

### Command line — fast once you know it

```
lockbox init                          # create your vault
lockbox add github                    # save a password
lockbox get github --copy-password    # copy it to clipboard
lockbox list                          # see everything
lockbox generate --length 32          # generate a strong password
```

---

## ⚡ Quick reference

```
lockbox add <service>               Save a password
lockbox add <service> --generate    Auto-generate a strong password
lockbox add <service> --label work  Multiple accounts for one service

lockbox get <service>               Look up an entry
lockbox get <service> --show-password
lockbox get <service> --copy-password

lockbox list                        List all saved entries
lockbox list --show-passwords

lockbox update <service>            Change username or password
lockbox delete <service>            Remove an entry

lockbox generate                    Generate without saving
lockbox changemaster                Change your master password
lockbox ui                          Open the visual TUI
lockbox docs <topic>                Read docs inside the CLI
```

---

## 🔒 Security

LockBox is built around one principle: **your master password never touches disk**.

| Layer | What it does |
|---|---|
| **Argon2id** | Memory-hard key derivation — GPU brute-force is impractical |
| **AES-128-CBC (Fernet)** | Authenticated encryption — tampering is detected |
| **HMAC-SHA256** | Integrity check on every read |
| **Random 32-byte salt** | Unique per vault — no rainbow tables |
| **Zero network calls** | LockBox never connects to anything |

> **If you forget your master password, the vault cannot be recovered.** There is no reset, no backup key, no support email. Write it down somewhere safe.

---

## 📁 Vault location

```
~/.lockbox/vault.enc    encrypted vault
~/.lockbox/salt.bin     key derivation salt
```

These files survive app updates. Deleting them permanently destroys your vault.

---

## 📖 Documentation

Full docs on [**GitBook →**](https://yourname.gitbook.io/lockbox)

Or read inside the CLI:

```
lockbox docs overview
lockbox docs commands
lockbox docs security
lockbox docs advanced
```

---

## 🛠️ Build from source

```bash
git clone https://github.com/yourname/lockbox
cd lockbox
pip install -e .
lockbox --version
```

---

## 📄 License

MIT © [yourname](https://github.com/yourname)
