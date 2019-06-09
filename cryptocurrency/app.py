from flask import Flask, jsonify, request
import uuid
from cryptocurrency.olicoin import Blockchain

app = Flask(__name__)
node_address = str(uuid.uuid4()).replace('-', '')
blockchain = Blockchain()


@app.route('/mine_block', methods=['GET'])
def mine_block():
    blockchain.add_transaction(sender=node_address, receiver='Oli', amount=1)
    block = blockchain.mine_block()

    response = {'message': 'Congratulations, you just mined a block!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],
                'transactions': block['transactions']}

    return jsonify(response), 200


@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}

    return jsonify(response), 200


@app.route('/is_valid', methods=['GET'])
def is_valid():
    if Blockchain.is_chain_valid(blockchain.chain):
        response = {'message': 'All good. The Blockchain is valid.'}
    else:
        response = {'message': 'Houston, we have a problem. The Blockchain is not valid.'}

    return jsonify(response), 200


@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    json = request.get_json()
    transaction_keys = ['sender', 'receiver', 'amount']

    if not all(key in json for key in transaction_keys):
        error = {'message': 'Some elements of the transaction are missing.'}
        return jsonify(error), 400

    index = blockchain.add_transaction(sender=json['sender'], receiver=json['receiver'], amount=json['amount'])
    response = {'message': f'This transaction will be added to Block {index}'}

    return jsonify(response), 201


@app.route('/connect_node', methods=['POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')

    if nodes is None:
        error = {'message': 'No node.'}
        return jsonify(error), 400

    for node in nodes:
        blockchain.add_node(node)

    response = {'message': f'All the nodes are now connected.',
                'total_nodes': list(blockchain.nodes)}

    return jsonify(response), 201


@app.route('/replace_chain', methods=['GET'])
def replace_chain():
    if blockchain.replace_chain():
        response = {'message': 'The nodes had different chains so the chain was replaced by the longest one.',
                    'new_chain': blockchain.chain}
    else:
        response = {'message': 'All good. The chain is the largest one.',
                    'chain': blockchain.chain}

    return jsonify(response), 200


if __name__ == '__main__':
    app.run()
