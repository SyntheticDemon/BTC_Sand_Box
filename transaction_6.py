# %%
from bitcoin.wallet import CBitcoinSecret, P2PKHBitcoinAddress
import bitcoin
import os
from bitcoin.wallet import CBitcoinAddress, CBitcoinSecret
import bitcoin.wallet
from bitcoin.core import COIN, b2lx, serialize, x, lx, b2x
from utils import *
bitcoin.SelectParams("testnet")

# random_secret = os.urandom(32)
my_private_key = CBitcoinSecret(
    "93B97jotm72MU5cuG8fh8fkdowjA5mVRVxi64YEssWAPeM1wBdZ")
my_public_key = my_private_key.pub
my_address = bitcoin.wallet.P2PKHBitcoinAddress.from_pubkey(my_public_key)
print("Your bitcoin testnet address\n", my_address,
      " Your bitcoin private key\n", my_private_key)

# %%

# %%

def scriptPubkey(sum, sub):
    return [OP_2DUP, OP_ADD, sum, OP_EQUALVERIFY, OP_SUB, sub, OP_EQUAL]

def PWPKH_scriptPubKey(public_key):
    return [OP_DUP, OP_HASH160, Hash160(public_key), OP_EQUALVERIFY, OP_CHECKSIG]

def scriptsigKey(prime_2, prime_1):
    return [prime_2, prime_1]

# %%

def send_from_P2PKH_transaction(amount_to_send, txid_to_spend, utxo_index,
                                ):
    sub = (11 - 7).to_bytes(1, 'little')
    sum = (11 + 7).to_bytes(1, 'little')
    prime_2 = 11
    prime_1 = 7
    prime_2 = prime_2.to_bytes(1, 'little')
    prime_1 = prime_1.to_bytes(1, 'little')
    txout_scriptPubKey = PWPKH_scriptPubKey(my_public_key)
    txin = create_txin(txid_to_spend, utxo_index)
    txin_scriptPubKey = scriptPubkey(sum,sub)
    txout = create_txout(amount_to_send, txout_scriptPubKey)
    txin_scriptSig = scriptsigKey(prime_2,prime_1)
    new_tx = create_signed_transaction(txin,txout,txin_scriptPubKey,txin_scriptSig)

    return broadcast_transaction(new_tx)
# %%


# if __name__ == '__main__':
    ######################################################################
amount_to_send = 0.00001023
txid_to_spend = 'dcef734cf985cc3305118e166e99abf1881c11526623272f543ea9fbce41679c'
utxo_index = 0  # UTXO index among transaction outputs

######################################################################
print(my_address)  # Prints your address in base58
print(my_public_key.hex())  # Print your public key in hex
print(my_private_key.hex())  # Print your private key in hex
# their_address = CBitcoinAddress("n4jYk1zbgY5qJA7omAeBm8e3STW7mGFMJi")
# txout_scriptPubKey = P2PKH_scriptPubKey(their_address)
response = send_from_P2PKH_transaction(
    amount_to_send, txid_to_spend, utxo_index)
print(response.status_code, response.reason)
# Report the hash of transaction which is printed in this section result
print(response.text)

# # %%

# %%

# {
#     "tx": {
#         "block_height": -1,
#         "block_index": -1,
#         "hash": "0feadbf50a1fbe15196ce6755649c0d4d072ad351a27152d20ba46c63b637280",
#         "addresses": [
#             "n1MUqSwtPqh94i6cpq92HE49MC2TzZpKsz"
#         ],
#         "total": 1023,
#         "fees": 1000,
#         "size": 89,
#         "vsize": 89,
#         "preference": "low",
#         "relayed_by": "5.117.195.137",
#         "received": "2023-05-26T08:00:45.51113442Z",
#         "ver": 1,
#         "double_spend": False,
#         "vin_sz": 1,
#         "vout_sz": 1,
#         "confirmations": 0,
#         "inputs": [
#             ...]
#         }
    
# }

