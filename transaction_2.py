# %%
from bitcoin.wallet import CBitcoinSecret, P2PKHBitcoinAddress
import bitcoin
import os
from bitcoin.wallet import CBitcoinAddress, CBitcoinSecret
import bitcoin.wallet
from utils import *
bitcoin.SelectParams("testnet")

# random_secret = os.urandom(32)
# my_private_key = CBitcoinSecret.from_secret_bytes(random_secret,compressed=False)
private_key = "93B97jotm72MU5cuG8fh8fkdowjA5mVRVxi64YEssWAPeM1wBdZ"
my_private_key = CBitcoinSecret(private_key)
my_public_key = my_private_key.pub
my_address = bitcoin.wallet.P2PKHBitcoinAddress.from_pubkey(my_public_key)
print("Your bitcoin testnet address\n", my_address,
      " Your bitcoin private key\n", my_private_key)

# %%

def P2PKH_scriptPubKey(address):
    return [OP_DUP, OP_HASH160, Hash160(address), OP_EQUALVERIFY, OP_CHECKSIG]

def P2PKH_scriptSig(txin, txout, txin_scriptPubKey):
    signature = create_OP_CHECKSIG_signature(
        txin, txout, txin_scriptPubKey, my_private_key)
    return [signature, my_public_key]

def P2PKH_freezing_scriptPubKey():
    return [OP_RETURN]

def P2PKH_freeing_scriptPubKey():
    return [OP_CHECKSIG]


# %%
def send_back(amount_to_send, txid_to_spend, utxo_index):
    txout_scriptPubKey = P2PKH_scriptPubKey(my_public_key)
    txin_scriptPubKey = P2PKH_freeing_scriptPubKey()
    txout_1 = create_txout(amount_to_send,txout_scriptPubKey)
    txin = create_txin(txid_to_spend, utxo_index)
    txin_scriptSig = P2PKH_scriptSig(
        txin, txout_1, txin_scriptPubKey)
    
    new_tx = create_signed_transaction(txin, txout_1, txin_scriptPubKey,
                                                 txin_scriptSig)

    return broadcast_transaction(new_tx)
# %%

# if __name__ == '__main__':
    ######################################################################
amount_to_send = 0.004
txid_to_spend = '2640675e03bb08c8b7cee585b6dd1ecc0ad238b1fe3a674b7a6af870a5322db5'
utxo_index = 1  # UTXO index among transaction outputs

######################################################################
print(my_address)  # Prints your address in base58
print(my_public_key.hex())  # Print your public key in hex
print(my_private_key.hex())  # Print your private key in hex
response = send_back(
    amount_to_send, txid_to_spend, utxo_index)
print(response.status_code, response.reason)

# # %%
# %%
print(response.text)

## Transaction HAsh
# %%
# 9eb0350e2e6e47b8f6e9d9a48fbc0f8b3ba7f2cea712228acf4bd30e12a529dc

# "tx": {
#     "block_height": -1,
#     "block_index": -1,
#     "hash": "9eb0350e2e6e47b8f6e9d9a48fbc0f8b3ba7f2cea712228acf4bd30e12a529dc",
#     "addresses": [
#         "n1MUqSwtPqh94i6cpq92HE49MC2TzZpKsz"
#     ],
#     "total": 400000,
#     "fees": 400000,
#     "size": 224,
#     "vsize": 224,
#     "preference": "high",
#     "relayed_by": "178.62.251.62",
#     "received": "2023-05-26T18:01:59.331557384Z",
#     "ver": 1,
#     "double_spend": false,
#     "vin_sz": 1,
#     "vout_sz": 1,
#     "confirmations": 0,
#     "inputs": [
#         {
#             "prev_hash": "2640675e03bb08c8b7cee585b6dd1ecc0ad238b1fe3a674b7a6af870a5322db5",
#             "output_index": 1,
#             "script": "483045022100b08d6bd785f9e379d24c249819abaa003d531e3bd39233800f59d17aa00161fd02206ea9c5f9c10ec5f4577a932264a4e81b6f26ec450ed4c7c758265c06889bb4e40141042cd52601aa227cc1c7987a975bcc2782aa7a67f1667828b6019cecc64cee654e0b81378a2a66c55bc62d96e1d46d7b94d8532d7722ff6164a6b259285b739680",
#             ...
#         }
#     ]
# }
# }
