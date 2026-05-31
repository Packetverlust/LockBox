# CLI Reference

## Global

| Command | Description |
|---|---|
| `lockbox --version` | Show version |
| `lockbox --help` | Show help |
| `lockbox ui` | Open visual TUI |

## Vault

### `lockbox init`
Create a new encrypted vault. Asks you to set a master password.

### `lockbox changemaster`
Re-encrypts the entire vault with a new master password.

## Passwords

### `lockbox add <service>`
Save a password for a service.

```
lockbox add github
lockbox add github --username me@email.com
lockbox add github --generate
lockbox add github --generate --password-length 32
lockbox add github --label work
```

| Flag | Description |
|---|---|
| `--username` / `-u` | Username or email |
| `--label` | Tag for multiple accounts per service |
| `--generate` / `-g` | Auto-generate a strong password |
| `--password-length` / `-l` | Length of generated password (default 20) |
| `--no-symbols` | Letters and numbers only |

### `lockbox get <service>`
Look up a saved entry.

```
lockbox get github
lockbox get github --show-password
lockbox get github --copy-password
lockbox get github --label work
```

### `lockbox list`
Show all saved entries.

```
lockbox list
lockbox list --show-passwords
```

### `lockbox update <service>`
Change an existing entry.

```
lockbox update github --new-password
lockbox update github --username new@email.com
lockbox update github --generate
lockbox update github --label work --generate
```

### `lockbox delete <service>`
Remove an entry.

```
lockbox delete github
lockbox delete github --label personal
lockbox delete github --confirm
```

## Generator

### `lockbox generate`
Generate a strong password without saving it.

```
lockbox generate
lockbox generate --length 32
lockbox generate --no-symbols
lockbox generate --copy-password
```

## Docs

### `lockbox docs <topic>`
Read documentation inside the CLI.

Topics: `overview` `commands` `usage` `advanced` `security`
