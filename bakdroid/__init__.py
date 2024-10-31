ENCRYPTION_MECHANISM = "AES/CBC/PKCS5Padding"

SUPPORTED_BACKUP_VERSIONS = {1, 2, 3, 4, 5}

AES_IV_SIZE = 16  # 16 bytes = 128 bits
MASTER_KEY_SIZE = 256 // 8  # Convert bits to bytes (32 bytes for AES-256)
MASTER_KEY_BLOB_SIZE = 32  # Assuming the same as MASTER_KEY_SIZE

PBKDF2_KEY_SIZE = 256 // 8  # Convert bits to bytes (32 bytes for derived key)
PBKDF2_SALT_SIZE = 512 // 8  # Convert bits to bytes (64 bytes salt)
PBKDF2_HASH_ROUNDS = 10000  # Number of PBKDF2 iterations
