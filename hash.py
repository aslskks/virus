import hashlib

def hash_file(path, algorithm="sha256", chunk_size=1024 * 1024):  # 1 MB chunks
    hasher = hashlib.new(algorithm)
    
    with open(path, "rb") as f:
        while chunk := f.read(chunk_size):
            hasher.update(chunk)
    
    return hasher.hexdigest()

with open("hash.txt", "w") as file:
    file.write(hash_file("main.exe"))