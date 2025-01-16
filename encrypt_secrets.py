from cryptography.fernet import Fernet
import os

# Charger la clé de chiffrement
with open("encryption.key", "rb") as key_file:
    key = key_file.read()

cipher = Fernet(key)

def encrypt_file(input_file, output_file):
    """Chiffre le contenu d'un fichier."""
    if not os.path.exists(input_file):
        print(f"Fichier introuvable : {input_file}, traitement ignoré.")
        return

    with open(input_file, "rb") as file:
        data = file.read()
    encrypted_data = cipher.encrypt(data)
    with open(output_file, "wb") as file:
        file.write(encrypted_data)
    print(f"Fichier {input_file} chiffré avec succès dans {output_file}")

# Liste des fichiers à chiffrer
files_to_encrypt = [
    ("linkedin_username.txt", "linkedin_username.enc"),
    ("linkedin_password.txt", "linkedin_password.enc"),
    ("linkedin_profiles.txt", "linkedin_profiles.enc")
]

# Chiffrer les fichiers existants
for input_file, output_file in files_to_encrypt:
    encrypt_file(input_file, output_file)