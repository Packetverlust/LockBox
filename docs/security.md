# Security

## How your vault is protected

LockBox uses multiple layers of protection. Your master password never touches disk.

## Encryption stack

| Layer | Algorithm | Purpose |
|---|---|---|
| Key derivation | Argon2id | Turns your password into an encryption key |
| Encryption | AES-128-CBC (Fernet) | Encrypts the vault contents |
| Integrity | HMAC-SHA256 | Detects tampering or corruption |
| Salt | 32 random bytes | Unique per vault, prevents rainbow tables |

## Why Argon2id?

Most tools use PBKDF2 for key derivation. LockBox uses Argon2id, recommended by the OWASP and German BSI, the winner of the Password Hashing Competition and the current industry standard.

The difference: Argon2id is **memory-hard**. Each password guess requires 64MB of RAM and multiple CPU passes. A GPU cracking rig that could make billions of PBKDF2 guesses per day is reduced to a few thousand Argon2id guesses per day.

## What an attacker needs

To crack your vault they need **both** lockbox files.

And then they still have to brute-force your master password against Argon2id. With a strong master password (12+ random characters), this is computationally impractical.

## What LockBox never does

- Never sends data over the network
- Never stores your master password
- Never logs passwords to disk
- Never connects to any server

## If you forget your master password

There is no recovery. No reset link, no backup key, no support email. The vault cannot be decrypted without the correct master password. Write it down somewhere safe offline.
