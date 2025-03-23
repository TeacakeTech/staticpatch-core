import subprocess


def crypt_apache_password(password: str) -> str:
    """Crypt a password using Apache's htpasswd command with bcrypt algorithm."""
    result = subprocess.run(["htpasswd", "-nbB", "dummy", password], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Failed to crypt password: {result.stderr}")
    return result.stdout[len("dummy:") :].strip()
