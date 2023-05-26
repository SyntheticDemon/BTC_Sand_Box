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
amount_to_send = 0.001
txid_to_spend = '2a048df915fbb5edb3eb5ad07b6c722fa30520cefb22dfac39fb819cc4f76598'
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
# Transaction hash 7294dae72803755fe7e9362d1c831edc8efea1dd13baab7f69fa409f661a2d8b
