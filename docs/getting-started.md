# Getting Started

## Install

### Windows

```powershell
irm https://raw.githubusercontent.com/yourname/lockbox/main/install.ps1 | iex
```

### Linux

```bash
curl -fsSL https://raw.githubusercontent.com/yourname/lockbox/main/install.sh | bash
```

Or download the binary directly from [Releases](https://github.com/yourname/lockbox/releases).

## First run

If you're not comfortable with the command line, start with the visual interface:

```
lockbox ui
```

It opens a terminal UI where you can create your vault and manage passwords without any commands.

If you prefer the CLI:

```
lockbox init
```

You'll be asked to create a master password. This is the only password you need to remember — it encrypts everything else.

## Adding your first password

```
lockbox add github
```

You'll be prompted for a username and password. Or generate one automatically:

```
lockbox add github --generate
```

## Looking up a password

```
lockbox get github
lockbox get github --show-password
lockbox get github --copy-password
```

## Your vault location

```
~/.lockbox/vault.enc    encrypted vault
~/.lockbox/salt.bin     key derivation salt
```

These files survive app updates. Never delete them unless you want to lose your vault.
