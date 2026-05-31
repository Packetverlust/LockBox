from __future__ import annotations

import secrets
import string


def generatePassword(length: int = 20, symbols: bool = True) -> str:
    chars = string.ascii_letters + string.digits
    if symbols:
        chars += "!@#$%^&*()-_=+[]{}|;:,.<>?"
    return "".join(secrets.choice(chars) for _ in range(length))
