import os
import functions
import nacl.utils
import nacl.pwhash

BACKUP_DIRS = open("dirs.conf")
PASSWORD = "deepfriednz!".encode("utf-8")
SALT = nacl.utils.random(nacl.pwhash.argon2i.SALTBYTES)


def main() -> object:
    print("Backup script")

    print("Create key from password file...")
    enc_key = functions.generate_enc_key(SALT, PASSWORD)

    secret_msg = b"This is gonna be good..."
    encrypted_object = functions.encrypt_object(secret_msg, enc_key)

    files_to_backup = []
    encrypted_files = []

    for dirs in BACKUP_DIRS:
        files_to_backup.append(functions.get_files(dirs))

    for files in files_to_backup:
        encrypted_files.append(functions.encrypt_object(files, enc_key))

    print(files_to_backup)
    print(encrypted_files)



if __name__ == '__main__':
    main()
