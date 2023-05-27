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


def P2PKH_scriptSig(txin, txout, txin_scriptPubKey):
    signature = create_OP_CHECKSIG_signature(
        txin, txout, txin_scriptPubKey, my_private_key)
    return [signature, my_public_key]

def scriptPubkey(sum, sub):
    return [OP_2DUP, OP_ADD, OP_HASH160, Hash160(sum), OP_EQUALVERIFY,
                                     OP_SUB, OP_HASH160, Hash160(sub), OP_EQUAL]

def PWPKH_scriptPubKey(public_key):
    return [OP_DUP, OP_HASH160, Hash160(public_key), OP_EQUALVERIFY, OP_CHECKSIG]


# %%

def send_custom_transaction(amount_to_send, txid_to_spend, utxo_index,
                            ):
    prime_2 = 7507
    prime_1 = 3469
    sub = (prime_2 - prime_1).to_bytes(2, 'little')
    sum = (prime_2 + prime_1).to_bytes(2, 'little')
    prime_2 = prime_2.to_bytes(2, 'little')
    prime_1 = prime_1.to_bytes(2, 'little')
    custom_scriptPubKey = scriptPubkey(sum, sub)
    txout = create_txout(amount_to_send, custom_scriptPubKey)
    txin_scriptPubKey = PWPKH_scriptPubKey(my_public_key)
    txin = create_txin(txid_to_spend, utxo_index)
    txin_scriptSig = P2PKH_scriptSig(
        txin, txout, txin_scriptPubKey)
    new_tx = create_signed_transaction(txin, txout, txin_scriptPubKey,
                                       txin_scriptSig)

    return broadcast_transaction(new_tx)
# %%


# if __name__ == '__main__':
    ######################################################################
amount_to_send = 0.0000355
txid_to_spend = '0d3bd2f0e05dd1d86fecec64533a0caa2d530a32655eda905e20325e8f042504'
utxo_index = 1  # UTXO index among transaction outputs

######################################################################
print(my_address)  # Prints your address in base58
print(my_public_key.hex())  # Print your public key in hex
print(my_private_key.hex())  # Print your private key in hex
# their_address = CBitcoinAddress("n4jYk1zbgY5qJA7omAeBm8e3STW7mGFMJi")
# txout_scriptPubKey = P2PKH_scriptPubKey(their_address)
response = send_custom_transaction(
    amount_to_send, txid_to_spend, utxo_index)
print(response.status_code, response.reason)
# Report the hash of transaction which is printed in this section result
print(response.text)
# c478220578227f8aa65b2d248274237ef3e297acf477096910f12438df87c512

# # %%

# %%
# print(response.text)
# {
#   "tx": {
#     "block_height": -1,
#     "block_index": -1,
#     "hash": "8c287b7cf4918a6c84839194046a214a8d96fe4c36f90a507aad52b225b69788",
#     "addresses": [
#       "n1MUqSwtPqh94i6cpq92HE49MC2TzZpKsz"
#     ],
#     "total": 3550,
#     "fees": 3000,
#     "size": 248,
#     "vsize": 248,
#     "preference": "low",
#     "relayed_by": "178.62.251.62",
#     "received": "2023-05-27T17:50:38.71058315Z",
#     "ver": 1,
#     "double_spend": false,
#     "vin_sz": 1,
#     "vout_sz": 1,
#     "confirmations": 0,
#     "inputs": [
# ...
#       }
#     ]
#   }
# }