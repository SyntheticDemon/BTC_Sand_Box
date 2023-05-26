# %%
from bitcoin.core import COIN, b2lx, serialize, x, lx, b2x, Hash
import bitcoin.wallet
from utils import *
import time
import struct
import os
import json
bitcoin.SelectParams('mainnet')
random_secret = os.urandom(32)
my_private_key = bitcoin.wallet.CBitcoinSecret.from_secret_bytes(
    random_secret, compressed=False)
my_public_key = my_private_key.pub

# %%

def pack_input(input):
    return bytes.fromhex(format(input, '08x')[::-1])

def calculate_target(bits):
    exponent = bits[2:4]
    coefficient = bits[4:]
    exponent2 = 8 * (int(exponent, 16) - 3)
    target = int(coefficient, 16) * (2**exponent2)
    target = format(target, 'x')
    target_byte = bytes.fromhex(str(target).zfill(64))
    return target_byte

def get_coinbase_tx(base_amount_to_send, coinbase_txid_to_spend, coinbase_utxo_index,
                    output_script, coinbase_script_sig):
    txin = create_txin(coinbase_txid_to_spend, coinbase_utxo_index)
    txout = create_txout(base_amount_to_send, output_script)
    tx = CMutableTransaction([txin], [txout])
    txin.scriptSig = coinbase_script_sig
    return tx


def create_merke_root(coinbase_tx):
    coinbase_serialized = b2x(coinbase_tx.serialize())
    merkle_root = b2lx(coinbase_tx.GetTxid())
    return merkle_root, coinbase_serialized

def create_header(version, last_block_hash, merkle_root, bits):
    time_now = int(time.time())
    return struct.pack("<L", version) + bytes.fromhex(last_block_hash)[::-1] + bytes.fromhex(merkle_root)[::-1] + struct.pack('<LL', time_now, int(bits, 16))

def mine_block(partial_header, target, MAX_TARGET=16 ** 7):
    nonce = 0
    while nonce <= MAX_TARGET:
        header = partial_header + struct.pack('<L', nonce)
        block_hash = Hash(header)
        if block_hash[::-1] < target:
            return header, block_hash,nonce
        nonce += 1
        
def gen_block(block_no,last_block_hash):
    Block = {}
    block_version = 2
    bits = '0x1f010000'   # 4 zeroes at epochs
    base_amount_to_send = 50
    coinbase_input_txid = (64*'0')
    coinbase_utxo_index = int('0xFFFFFFFF', 16)
    coinbase_hex_data = '810199395PouriyaTajmehrabi'.encode('utf-8').hex()
    output_script = [OP_DUP, OP_HASH160, Hash160(
        my_public_key), OP_EQUALVERIFY, OP_CHECKSIG]
    coinbase_script_sig = CScript(
        [int(coinbase_hex_data, 16).to_bytes(len(coinbase_hex_data)//2, 'big')])
    coinbase_tx = get_coinbase_tx(base_amount_to_send, coinbase_input_txid, coinbase_utxo_index,
                                  output_script, coinbase_script_sig)
    merkle_root, block_body = create_merke_root(coinbase_tx)
    target = calculate_target(bits)
    partial_header = create_header(
        block_version, last_block_hash, merkle_root, bits)
    header, block_hash,nounce = mine_block(partial_header, target)
    Block["header"] = b2x(header)    
    Block["body"] = block_body
    Block["nonce"] = nounce
    Block["height"] =block_no + 1
    Block["coinbase_hex"] = coinbase_hex_data
    Block["previous_block"] = last_block_hash
    Block["block_hash"] = b2lx(block_hash)
    print('Generated Block',  json.dumps(Block))
    return json.dumps(Block)

if __name__ == '__main__':
   last_block_hash = "000000005554bf1d8c846e738bb792a50fa1724e1e4111aa48fdddd8fe2b9b27"
   print (gen_block(9395,last_block_hash))

# %%

{"header": "02000000279b2bfed8ddfd48aa11411e4e72a10fa592b78b736e848c1dbf5455000000005a8a42029a61f8b18f8ebee4d62d5e1d051a64cd9397042d1f3c2cc99ab3a908950b71640000011febf90000", "body": "01000000010000000000000000000000000000000000000000000000000000000000000000ffffffff1b1a383130313939333935506f757269796154616a6d656872616269ffffffff0100f2052a010000001976a914037df6b1991ba1d0b0370b2abdad39d85dbf71f388ac00000000",
    "nonce": 63979, "height": 9396, "coinbase_hex": "383130313939333935506f757269796154616a6d656872616269", "previous_block": "000000005554bf1d8c846e738bb792a50fa1724e1e4111aa48fdddd8fe2b9b27", "block_hash": "00007fb4bb78450dfc521e74c7e34fff3a6123833827ec093d518289ef9a702b"}
