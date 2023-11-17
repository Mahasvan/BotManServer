import secrets


def generate_otp() -> int:
    return secrets.randbits(16)
