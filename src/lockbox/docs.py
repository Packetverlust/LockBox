from __future__ import annotations

DOCS_INDEX = """\
LockBox docs

LockBox is an encrypted local password manager for the command line.
Your passwords never leave your machine. Everything is locked behind one master password.

Topics:
  overview       What LockBox is and how it works
  commands       All available commands
  usage          Common everyday usage
  advanced       Power-user flags and multi-account setup
  security       How encryption works

Run:
  lockbox docs <topic>
"""

DOCS_OVERVIEW = """\
Overview

LockBox stores your passwords in an encrypted file on your own machine (~/.lockbox/vault.enc).
Nothing is sent anywhere. No account needed.

How it works:
  1. You create a vault with one master password.
  2. Every time you run a command, you type that master password to unlock the vault.
  3. Your entries are decrypted in memory, used, then discarded.

The vault holds entries. Each entry is a service with:
  - username or email
  - password
  - optional label (for multiple accounts on the same service)

Multiple accounts per service:
  You can save more than one account under the same service name.
  Use --label to tell them apart:
    lockbox add github --label work
    lockbox add github --label personal
"""

DOCS_COMMANDS = """\
Commands

  lockbox init
    Create a new encrypted vault. Run this once before anything else.

  lockbox add <service>
    Save a password for a service. Works for existing accounts (type your password)
    or new ones (use --generate to create a strong password).

  lockbox get <service>
    Look up a saved entry. Password is hidden by default.
    Use --show-password to reveal it or --copy-password to copy it silently.

  lockbox list
    Show all saved entries (service, label, username).
    Passwords are hidden by default. Use --show-passwords to reveal all.

  lockbox update <service>
    Change the username or password for an existing entry.

  lockbox delete <service>
    Remove an entry from the vault. Asks for confirmation.

  lockbox generate
    Generate a strong password without saving it anywhere.

  lockbox changemaster
    Change your master password. Re-encrypts the entire vault.

  lockbox docs <topic>
    View documentation inside the CLI.
    Topics: overview, commands, usage, advanced, security
"""

DOCS_USAGE = """\
Usage

First time setup:
  lockbox init

Save a password you already have:
  lockbox add github
    - you will be asked for your username and your existing password

Create a new account with a generated password:
  lockbox add netflix --generate

Look up a saved password:
  lockbox get github --show-password
  lockbox get github --copy-password

See all saved entries:
  lockbox list

Update a password after changing it on the website:
  lockbox update github --new-password

Delete an entry you no longer need:
  lockbox delete github
"""

DOCS_ADVANCED = """\
Advanced usage

Multiple accounts for the same service:
  lockbox add github --label work
  lockbox add github --label personal
  lockbox get github               - shows both accounts
  lockbox get github --label work  - shows only the work account
  lockbox update github --label personal --generate
  lockbox delete github --label work

Inline flags to skip prompts:
  lockbox add github --username me@gmail.com --generate
  lockbox delete github --confirm

Password generation options:
  lockbox generate --length 32
  lockbox generate --length 16 --no-symbols
  lockbox generate --copy-password
  lockbox add github --generate --password-length 32 --no-symbols

List with passwords visible:
  lockbox list --show-passwords

Short aliases (for power users):
  -u   --username
  -g   --generate
  -l   --password-length
  -s   --show-password
  -c   --copy-password
  -p   --new-password
  -y   --confirm
"""

DOCS_SECURITY = """\
Security

Encryption:
  Vault is encrypted with Fernet (AES-128-CBC + HMAC-SHA256).
  This provides both confidentiality and integrity.
  If someone tampers with the vault file, decryption will fail.

Key derivation:
  Your master password is never stored anywhere on disk.
  It is derived into an encryption key using PBKDF2-HMAC-SHA256
  with 480,000 iterations.
  A random 16-byte salt is stored at ~/.lockbox/salt.bin.

What is stored on disk:
  ~/.lockbox/vault.enc
  ~/.lockbox/salt.bin

What is NOT stored:
  Your master password. Ever.
  If you forget it, the vault cannot be recovered.

Recommendations:
  - Use a strong master password you will remember.
  - Back up ~/.lockbox/ to a safe location.
  - Use --generate for new accounts to get a strong unique password per site.
  - Use --copy-password instead of --show-password when others can see your screen.
"""
