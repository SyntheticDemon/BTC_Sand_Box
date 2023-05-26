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


def P2PKH_scriptSig_for_two_outputs(txin, txout_1, txout_2, txin_scriptPubKey):
    signature = create_OP_CHECKMULTISIG_signature(
        txin, txin_scriptPubKey, txout_1, txout_2, my_private_key)
    return [signature, my_public_key]


def P2PKH_freezing_scriptPubKey():
    return [OP_RETURN]


def P2PKH_freeing_scriptPubKey():
    return [OP_CHECKSIG]


# %%
def send_from_P2PKH_transaction(amount_to_send, txid_to_spend, utxo_index,
                                freeing_script,
                                freezing_script):
    txout_freezing = create_txout(amount_to_send, freeing_script)
    txout_freeing = create_txout(amount_to_send, freezing_script)
    txin_scriptPubKey = P2PKH_scriptPubKey(my_public_key)
    txin = create_txin(txid_to_spend, utxo_index)
    txin_scriptSig = P2PKH_scriptSig_for_two_outputs(
        txin, txout_freeing, txout_freezing, txin_scriptPubKey)
    new_tx = create_signed_transaction_2_outputs(txin, txout_freeing, txout_freezing, txin_scriptPubKey,
                                                 txin_scriptSig)

    return broadcast_transaction(new_tx)
# %%


# if __name__ == '__main__':
    ######################################################################
amount_to_send = 0.008
txid_to_spend = '0642841ce707a2d59274bc415ca043c2498cf1cfbdd4b554048dea5b88a66ad2'
utxo_index = 0  # UTXO index among transaction outputs

######################################################################
print(my_address)  # Prints your address in base58
print(my_public_key.hex())  # Print your public key in hex
print(my_private_key.hex())  # Print your private key in hex
# their_address = CBitcoinAddress("n4jYk1zbgY5qJA7omAeBm8e3STW7mGFMJi")
# txout_scriptPubKey = P2PKH_scriptPubKey(their_address)
txout_freeing = P2PKH_freeing_scriptPubKey()
txout_freezing = P2PKH_freezing_scriptPubKey()
response = send_from_P2PKH_transaction(
    amount_to_send, txid_to_spend, utxo_index, txout_freeing, txout_freezing)
# print(response.status_code, response.reason)
# print(response.text) # Report the hash of transaction which is printed in this section result

# # %%

# %%
print(response.text)
# %%
# Transaction hash {
# "tx": {
#     "block_height": -1,
#     "block_index": -1,
#     "hash": "2640675e03bb08c8b7cee585b6dd1ecc0ad238b1fe3a674b7a6af870a5322db5",
#     "addresses": [
#         "n1MUqSwtPqh94i6cpq92HE49MC2TzZpKsz"
#     ],
#     "total": 1600000,
#     "fees": 54487,
#     "size": 209,
#     "vsize": 209,
#     "preference": "high",
#     "relayed_by": "178.62.251.62",
#     "received": "2023-05-26T17:00:44.50915564Z",
#     "ver": 1,
#     "double_spend": false,
#     "vin_sz": 1,
#     "vout_sz": 2,
#     "confirmations": 0,
#     "inputs": [
#         {
#             "prev_hash": "0642841ce707a2d59274bc415ca043c2498cf1cfbdd4b554048dea5b88a66ad2",
#             "output_index": 0,
#             "script": "47304402205572027969c05068b74f2891e377d9e6463cad0325158f8f530e261d1e44b0d50220448d65b615b0b3d7337517e485078777ee38177db026159bb9c81c826168c0030141042cd52601aa227cc1c7987a975bcc2782aa7a67f1667828b6019cecc64cee654e0b81378a2a66c55bc62d96e1d46d7b94d8532d7722ff6164a6b259285b739680",
#             ...
#         }
#     ]
# }
# }
