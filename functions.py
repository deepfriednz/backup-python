import os
import nacl.secret
import nacl.utils
import nacl.pwhash
import base64


def traverse(dirs):
    for root, dirs, files in os.walk(dirs):
        for file in files:
            if file.endswith(".txt"):
                print(os.path.join(root, file))


def get_files(work_dir: object):
    scan_list = os.scandir(work_dir)
    file_list = []

    for the_file in scan_list:
        file_list.append(os.path.realpath(the_file))

    return file_list


def generate_enc_key(salt: object, password: object):
    derived_key = nacl.pwhash.argon2i.kdf(nacl.secret.SecretBox.KEY_SIZE, password, salt)
    return derived_key


def encrypt_object(file, enc_key, tempdir):
    box = nacl.secret.SecretBox(enc_key)
    output_file = tempdir + encrypt_file_name(file, enc_key)
    nonce = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)

    with open(output_file, 'wb') as fout:
        with open(file, 'rb') as fin:
            for chunk, index in read_in_chunks(fin, chunk_size=16 * 1024 - 40):
                enc = box.encrypt(chunk, chunk_nonce(nonce, index))
                fout.write(enc)

    return output_file


def encode_base64(file):
    encoded = base64.urlsafe_b64encode(file).decode("ascii")
    return encoded


def read_in_chunks(file_object, chunk_size=32 * 1024):
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 16k."""
    index = 0
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield (data, index)
        index += 1


def encrypt_file_name(file_name, enc_key):
    box = nacl.secret.SecretBox(enc_key)

    enc_name = box.encrypt(file_name)
    base64_name = encode_base64(enc_name)

    return base64_name


def chunk_nonce(base, index):
    size = nacl.secret.SecretBox.NONCE_SIZE
    return int.to_bytes(int.from_bytes(base, byteorder='big') + index, length=size, byteorder='big')
