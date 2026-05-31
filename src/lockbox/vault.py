from __future__ import annotations

import json
import os
import base64

from argon2.low_level import hash_secret_raw, Type
from cryptography.fernet import Fernet, InvalidToken

vaultDir  = os.path.join(os.path.expanduser("~"), ".lockbox")
vaultFile = os.path.join(vaultDir, "vault.enc")
saltFile  = os.path.join(vaultDir, "salt.bin")

ARGON2_TIME_COST   = 3
ARGON2_MEMORY_COST = 65536
ARGON2_PARALLELISM = 4
ARGON2_HASH_LEN    = 32


def firstRun() -> bool:
    return not os.path.exists(vaultFile)


def loadSalt() -> bytes:
    os.makedirs(vaultDir, exist_ok=True)
    if not os.path.exists(saltFile):
        salt = os.urandom(32)
        with open(saltFile, "wb") as f:
            f.write(salt)
    with open(saltFile, "rb") as f:
        return f.read()


def deriveKey(masterPw: str, salt: bytes) -> bytes:
    raw = hash_secret_raw(
        secret=masterPw.encode(),
        salt=salt,
        time_cost=ARGON2_TIME_COST,
        memory_cost=ARGON2_MEMORY_COST,
        parallelism=ARGON2_PARALLELISM,
        hash_len=ARGON2_HASH_LEN,
        type=Type.ID,
    )
    return base64.urlsafe_b64encode(raw)


def getFernet(masterPw: str) -> Fernet:
    return Fernet(deriveKey(masterPw, loadSalt()))


def loadVault(masterPw: str) -> dict | None:
    if not os.path.exists(vaultFile):
        return {}
    fernet = getFernet(masterPw)
    with open(vaultFile, "rb") as f:
        raw = f.read()
    try:
        return json.loads(fernet.decrypt(raw).decode())
    except (InvalidToken, Exception):
        return None


def saveVault(masterPw: str, data: dict) -> None:
    os.makedirs(vaultDir, exist_ok=True)
    encrypted = getFernet(masterPw).encrypt(json.dumps(data).encode())
    with open(vaultFile, "wb") as f:
        f.write(encrypted)
