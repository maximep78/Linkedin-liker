from cryptography.fernet import Fernet

# Générer une clé et l'écrire dans un fichier
key = Fernet.generate_key()
with open("encryption.key", "wb") as key_file:
    key_file.write(key)

print("Clé générée et sauvegardée dans 'encryption.key'")
