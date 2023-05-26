# %%
import secrets
import codecs
import ecdsa
import random as rand
import hashlib
from Crypto.Hash import _RIPEMD160
import ecdsa.ellipticcurve as eliptic
from address_generator import get_private_public_pair, get_wif, get_bitcoin_address, compress_public_key
# %%


def generate_vanity_address(target):
    while (True):
        key_pair = get_private_public_pair()
        generated_address = (get_bitcoin_address(key_pair[1]))
        print("Vanity Part", generated_address[1:4], "Private Key - Public Key", key_pair, "WIF Format Private Key ",
              get_wif(key_pair[0])
              )
        if target == generated_address[1:4]:
            print("Finally found an answer", generated_address, key_pair, get_wif(key_pair[0]))
            break

# %% 
generate_vanity_address(target='por')
# %%
##
# Finally found an answer mporAzdZ8wz2TSfQrbj5rStJ6nMvWeioKM('50a4c434ec308a805eb4168b274d1fbce14093d1d83b20aa3fd6c9ebb3d5ca84', ## '8cd70bbe962e2fce6d8e86d233d7ac3a09a89338407840c6060c5f5ece84d1285952b7f96443aa4f138ea6cff8275e9a1dfcc92d4a835bc8201d78e083900ef6')
get_wif("50a4c434ec308a805eb4168b274d1fbce14093d1d83b20aa3fd6c9ebb3d5ca84")

# %%
