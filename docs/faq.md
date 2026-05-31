# FAQ

## Will I lose my passwords when I update LockBox?

No. Your vault lives in `~/.lockbox/` which is completely separate from the app. Updating LockBox never touches that folder.

## What happens if I forget my master password?

Your vault cannot be recovered. There is no reset mechanism by design — storing a recovery key would be a security hole. Write your master password down and keep it somewhere safe offline.

## Can I use LockBox on multiple computers?

Yes, but you have to sync manually. Copy `~/.lockbox/vault.enc` and `~/.lockbox/salt.bin` to the same location on the other machine. Both files are required.

## Can I have multiple accounts for the same service?

Yes, use labels:

```
lockbox add github --label work
lockbox add github --label personal
lockbox get github --label work
```

## Why is the app slow to unlock?

That's intentional. Argon2id deliberately takes ~300ms per unlock attempt. This makes brute-force attacks impractical. You only notice it once per session.

## Is my clipboard safe after copying a password?

LockBox copies to your system clipboard using your OS clipboard manager. It does not clear the clipboard automatically after copying. Be aware of clipboard history tools that may log it.

## Can someone crack my vault if they steal my files?

Only if your master password is weak. With a strong password (12+ random characters), Argon2id makes brute-force attacks computationally impractical even with specialized hardware. See [Security](security.md) for details.

## Does LockBox work without internet?

Yes, completely. LockBox never makes any network requests.
