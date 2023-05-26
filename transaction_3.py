# %%
from bitcoin.wallet import CBitcoinSecret, P2PKHBitcoinAddress
import bitcoin
import os
from bitcoin.wallet import CBitcoinAddress, CBitcoinSecret
import bitcoin.wallet
from utils import *
bitcoin.SelectParams("testnet")
# %% 

def get_address_from_private_key(private_key_str):
    return bitcoin.wallet.P2PKHBitcoinAddress.from_pubkey(CBitcoinSecret(private_key_str).pub)

# %% 
first_private_key = CBitcoinSecret("91o27PAoB98iUUPcH8kRXv6ehCFdcHYi1eauZ4osmtq4GxEeLch")
second_private_key = CBitcoinSecret("92VEdxrgo7mjShet5MmsySfFiQ5x76VNAW6PxgPX9CPZNfwAzNm")
third_private_key = CBitcoinSecret("91hUp4umWUabTBdd3TJ5dCxGR49hwME5oeWD6Mdi8xaWmidUK6K")
first_public_key = first_private_key.pub
second_public_key = second_private_key.pub
third_public_key = third_private_key.pub

# %% 
private_key = "93B97jotm72MU5cuG8fh8fkdowjA5mVRVxi64YEssWAPeM1wBdZ"
my_private_key = CBitcoinSecret(private_key)
my_public_key = my_private_key.pub
my_address = bitcoin.wallet.P2PKHBitcoinAddress.from_pubkey(my_public_key)
print("Your bitcoin testnet address\n", my_address,
      " Your bitcoin private key\n", my_private_key)

# %%
def MultiSig_LockingScript(pk1,pk2,pk3):
    return [OP_2,pk1,pk2,pk3,OP_3,OP_CHECKMULTISIG]
    
def P2PKH_scriptPubKey(address):
    return [OP_DUP, OP_HASH160, Hash160(address), OP_EQUALVERIFY, OP_CHECKSIG]


def P2PKH_scriptSig(txin, txout, txin_scriptPubKey):
    signature = create_OP_CHECKSIG_signature(
        txin, txout, txin_scriptPubKey, my_private_key)
    return [signature, my_public_key]

# %%
def send_multi_sig(amount_to_send, txid_to_spend, utxo_index):
    txout_unlocking_script = MultiSig_LockingScript(
        first_public_key, second_public_key, third_public_key)
    txout = create_txout(amount_to_send, txout_unlocking_script)
    txin_scriptPubKey = P2PKH_scriptPubKey(my_public_key)
    txin = create_txin(txid_to_spend, utxo_index)
    txin_scriptSig = P2PKH_scriptSig(txin, txout, txin_scriptPubKey)
    new_tx = create_signed_transaction(txin, txout, txin_scriptPubKey,
                                       txin_scriptSig)
    # print(new_tx)
    return broadcast_transaction(new_tx)
# %%


# if __name__ == '__main__':
    ######################################################################
amount_to_send = 0.00005023
txid_to_spend = '713ec84da8748f0b476a02d2b587a7fc6ad0fb31ce2de8b2a5091c8ed866a1a6'
utxo_index = 1  # UTXO index among transaction outputs

######################################################################
print(my_address)  # Prints your address in base58 
print(my_public_key.hex())  # Print your public key in hex
print(my_private_key.hex())  # Print your private key in hex
response = send_multi_sig(
    amount_to_send, txid_to_spend, utxo_index)

# # %%
# %%
print(response.status_code, response.reason)
print(response.text)

# %%

{
    "tx": {
        "block_height": -1,
        "block_index": -1,
        "hash": "89a47d8ba3c8c80c062bcf308aa655b502ea5abbb327114070fe4769c892ea58",
        "addresses": [
            "n1MUqSwtPqh94i6cpq92HE49MC2TzZpKsz",
            "zMZxsfvMxyq7yVmxXd3o3GRTNSo65z4UVf"
        ],
        "total": 5023,
        "fees": 9700,
        "size": 400,
        "vsize": 400,
        "preference": "low",
        "relayed_by": "5.117.195.137",
        "received": "2023-05-25T22:54:14.449084371Z",
        "ver": 1,
        "double_spend": False,
        "vin_sz": 1,
        "vout_sz": 1,
        "confirmations": 0,
        "inputs": [
            {
                "prev_hash": "713ec84da8748f0b476a02d2b587a7fc6ad0fb31ce2de8b2a5091c8ed866a1a6",
            }
        ]
    }
}

# %% 