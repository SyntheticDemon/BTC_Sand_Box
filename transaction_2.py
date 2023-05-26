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
    txin_scriptPubKey = P2PKH_scriptPubKey(my_public_key)
    txout_1 = create_txout(amount_to_send,txin_scriptPubKey)
    txin = create_txin(txid_to_spend, 0)
    txin_scriptSig = P2PKH_scriptSig(
        txin, txout_1, txin_scriptPubKey)
    
    new_tx = create_signed_transaction(txin, txout_1, txin_scriptPubKey,
                                                 txin_scriptSig)

    return broadcast_transaction(new_tx)
# %%

# if __name__ == '__main__':
    ######################################################################
amount_to_send = 0.0009
txid_to_spend = 'dcd7b0c54602cba50f2b2f654e83f92489ff1132102a669f1e2e40be3db14a9f'
utxo_index = 1  # UTXO index among transaction outputs

######################################################################
print(my_address)  # Prints your address in base58
print(my_public_key.hex())  # Print your public key in hex
print(my_private_key.hex())  # Print your private key in hex
response = send_back(
    amount_to_send, txid_to_spend, utxo_index)
print(response.status_code, response.reason)
print(response.text)

# # %%
# %%
## Transaction HAsh