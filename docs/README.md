# Welcome to LockBox

Encrypted local password manager. Your passwords never leave your machine.

LockBox stores everything in an encrypted vault on your own computer using Argon2id + AES-128. Nothing is ever sent to a server or cloud.

## Download

Grab the latest binary from [GitHub Releases](https://github.com/yourname/lockbox/releases) — no Python needed.

## Two ways to use it

**Visual interface** — easiest way to start:
```
lockbox ui
```

**Command line** — fast once you know it:
```
lockbox init
lockbox add github
lockbox get github --copy-password
lockbox list
```

## Next steps

- [Getting Started](getting-started.md) — install and create your vault
- [CLI Reference](cli-reference.md) — every command explained
- [Security](security.md) — how encryption works
- [FAQ](faq.md) — common questions
