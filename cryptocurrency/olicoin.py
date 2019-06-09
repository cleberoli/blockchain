import hashlib
import json
import requests
from datetime import datetime
from urllib import parse


class Blockchain:

    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block(proof=1, previous_hash='0')
        self.nodes = set()

    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash,
                 'transactions': self.transactions}
        self.transactions = []
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def mine_block(self):
        previous_block = self.get_previous_block()
        previous_proof = previous_block['proof']
        proof = Blockchain.proof_of_work(previous_proof)
        previous_hash = Blockchain.hash(previous_block)

        return self.create_block(proof, previous_hash)

    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({'sender': sender,
                                  'receiver': receiver,
                                  'amount': amount})

        return self.get_previous_block()['index'] + 1

    def add_node(self, node_address):
        parsed_url = parse.urlparse(node_address)
        self.nodes.add(parsed_url.netloc)

    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)

        for node in network:
            response = requests.get(f'http://{node}/get_chain')

            if response.status_code == 200:
                lenght = response.json()['length']
                chain = response.json()['chain']

                if lenght > max_length and self.is_chain_valid(chain):
                    max_length = lenght
                    longest_chain = chain

        if longest_chain:
            self.chain = longest_chain
            return True

        return False

    @staticmethod
    def proof_of_work(previous_proof):
        new_proof = 1
        check_proof = False

        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()

            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1

        return new_proof

    @staticmethod
    def hash(block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    @staticmethod
    def is_chain_valid(chain):
        previous_block = chain[0]
        block_index = 1

        while block_index < len(chain):
            current_block = chain[block_index]
            current_proof = current_block['proof']
            previous_proof = previous_block['proof']
            hash_operation = hashlib.sha256(str(current_proof ** 2 - previous_proof ** 2).encode()).hexdigest()

            if current_block['previous_hash'] != Blockchain.hash(previous_block) or hash_operation[:4] != '0000':
                return False

            previous_block = current_block
            block_index += 1

        return True
