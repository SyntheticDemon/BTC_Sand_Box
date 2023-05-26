# %%
import secrets as secrets
import codecs
import ecdsa
import random as rand
import hashlib
from Crypto.Hash import _RIPEMD160
import ecdsa.ellipticcurve as eliptic
BITCOIN_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
TEST_NET_PREFIX = 'ef'
TEST_NET_ADDRESS_PREFIX = '6f'

MAIN_NET_PREFIX = '80'
COMPRESSION_BYTE = '01'


def get_checksum(key):
    key_bytes = codecs.decode(key, 'hex')
    first_sha256 = hashlib.sha256(key_bytes)
    first_sha256_digest = first_sha256.digest()
    sha256_2 = hashlib.sha256(first_sha256_digest)
    sha_256_2_digest = sha256_2.digest()
    sha256_2_hex = codecs.encode(sha_256_2_digest, 'hex')
    checksum = sha256_2_hex[:8]
    return str(checksum)[2:-1]

# %%

# %%


def base58encode(address_hex):
    result = ''
    leading_zeros = len(address_hex) - len(address_hex.lstrip('0'))
    address_int = int(address_hex, 16)
    while (address_int > 0):
        digit_char = BITCOIN_ALPHABET[address_int % 58]
        result = digit_char + result
        address_int //= 58
    ones = (leading_zeros // 2)
    result = '1'*ones + result
    return result
# %%


def get_private_public_pair():
    bits = secrets.randbits(256)
    bits_hex = hex(bits)
    lengthy = len(bits_hex[2:])
    if (lengthy < 64):
        private_key_str = '0'* (64 - lengthy)  + bits_hex[2:]
    else:
        private_key_str = bits_hex[2:]
    private_key_bytes = codecs.decode(private_key_str, 'hex')
    public_key = ecdsa.SigningKey.from_string(
        private_key_bytes, curve=ecdsa.SECP256k1).verifying_key
    key_bytes = public_key.to_string()
    key_hex = codecs.encode(key_bytes, 'hex')
    key_string = str(key_hex)
    public_key_str = key_string[2:-1]
    return (private_key_str, public_key_str)

# %%


def get_wif(private_key_str,prefix=TEST_NET_PREFIX):
    extended_private_key = prefix + private_key_str + COMPRESSION_BYTE
    extended_private_key = extended_private_key + \
        get_checksum(extended_private_key)
    return base58encode(
        extended_private_key
    )


def HASH160(public_key):
    key_bytes = codecs.decode(public_key, 'hex')
    sha256_result = hashlib.sha256(key_bytes)
    sha256_result_digest = sha256_result.digest()
    ripemd_new = _RIPEMD160.new('ripemd160')
    ripemd_new.update(sha256_result_digest)
    ripemd_new_digest = ripemd_new.digest()
    ripemd_new_digest_str_digest = str(codecs.encode(ripemd_new_digest, 'hex'))
    return ripemd_new_digest_str_digest[2:-1]


def get_public_key(private_key_str):
    private_key_bytes = codecs.decode(private_key_str, 'hex')
    public_key = ecdsa.SigningKey.from_string(
        private_key_bytes, curve=ecdsa.SECP256k1).verifying_key
    return public_key.to_string().hex()[2:-1]

# https://en.bitcoin.it/wiki/BIP_0137

def compress_public_key(key):
    comp_key = key[:len(key)//2]
    if (int('0x'+key[-1], 16) % 2 == 0):
        return '02' + comp_key
    return '03' + comp_key

def get_bitcoin_address(public_key, network_prefix=TEST_NET_ADDRESS_PREFIX):
    hash_160 = HASH160(compress_public_key(public_key))
    # print("Encrypted Public Key", hash_160, "Compressed Key", compress_public_key(public_key))
    extended_public_key = network_prefix + hash_160
    check_sum = get_checksum(extended_public_key)
    extended_public_key = extended_public_key + check_sum
    return base58encode(extended_public_key)

# %%
