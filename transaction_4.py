# %% 
import bitcoin.wallet
from utils import *
from bitcoin.wallet import CBitcoinAddress, CBitcoinSecret

# %%
bitcoin.SelectParams("testnet")
fpk = CBitcoinSecret(
    "91o27PAoB98iUUPcH8kRXv6ehCFdcHYi1eauZ4osmtq4GxEeLch")
spk = CBitcoinSecret(
    "92VEdxrgo7mjShet5MmsySfFiQ5x76VNAW6PxgPX9CPZNfwAzNm")
tpk = CBitcoinSecret(
    "91hUp4umWUabTBdd3TJ5dCxGR49hwME5oeWD6Mdi8xaWmidUK6K")
fpubk = fpk.pub
spubk = spk.pub
tpubk = tpk.pub

private_key = "93B97jotm72MU5cuG8fh8fkdowjA5mVRVxi64YEssWAPeM1wBdZ"
my_private_key = CBitcoinSecret(private_key)
my_public_key = my_private_key.pub
my_address = bitcoin.wallet.P2PKHBitcoinAddress.from_pubkey(my_public_key)
print("Your bitcoin testnet address\n", my_address,
      " Your bitcoin private key\n", my_private_key)
# %%

def P2PKH_output_scriptPubKey(public_key):
    return [OP_DUP, OP_HASH160, Hash160(public_key), OP_EQUALVERIFY, OP_CHECKSIG]


def MultiSigScript_output(fpubk, spubk, tpubk):
    return [OP_2, fpubk, spubk, tpubk, OP_3, OP_CHECKMULTISIG]

def P2PKH_scriptSig(txin, txout, txin_scriptPubKey):
    first_signature = create_OP_CHECKSIG_signature(
        txin, txout, txin_scriptPubKey, fpk)
    second_signature = create_OP_CHECKSIG_signature(
        txin, txout, txin_scriptPubKey, spk)
    return [OP_0, first_signature, second_signature]

def make_P2PKH_transaction(amount_to_send, txid_to_spend, utxo_index,
                           txout_scriptPubKey):
    txout = create_txout(amount_to_send, txout_scriptPubKey)
    txin_scriptPubKey = MultiSigScript_output(fpubk, spubk, tpubk)
    txin = create_txin(txid_to_spend, utxo_index)
    txin_scriptSig = P2PKH_scriptSig(txin, txout, txin_scriptPubKey)
    new_tx = create_signed_transaction(txin, txout, txin_scriptPubKey,
                                       txin_scriptSig)
    return broadcast_transaction(new_tx)

if __name__ == '__main__':
    amount_to_send = 0.00003023
    txid_to_spend = (
        '89a47d8ba3c8c80c062bcf308aa655b502ea5abbb327114070fe4769c892ea58')
    utxo_index = 0
    txout_scriptPubKey = P2PKH_output_scriptPubKey(my_public_key)
    response = make_P2PKH_transaction(
        amount_to_send, txid_to_spend, utxo_index, txout_scriptPubKey)
    print(response.status_code, response.reason)
    print(response.text)
# Transaction hash 
# # %%
# {
#     "tx": {
#         "block_height": -1,
#         "block_index": -1,
#         "hash": "4b68d02dc039be6dabaefe36a66e2b270af196f056785977ec45937a1ce9017d",
#         "addresses": [
#             "zMZxsfvMxyq7yVmxXd3o3GRTNSo65z4UVf",
#             "n1MUqSwtPqh94i6cpq92HE49MC2TzZpKsz"
#         ],
#         "total": 3023,
#         "fees": 2000,
#         "size": 232,
#         "vsize": 232,
#         "preference": "low",
#         "relayed_by": "5.117.195.137",
#         "received": "2023-05-25T22:56:35.049471867Z",
#         "ver": 1,
#         "double_spend": False,
#         "vin_sz": 1,
#         "vout_sz": 1,
#         "confirmations": 0,
#         "inputs": [
#             {
#                 "prev_hash": "89a47d8ba3c8c80c062bcf308aa655b502ea5abbb327114070fe4769c892ea58",
#             }
#         ]
#     }
# }
