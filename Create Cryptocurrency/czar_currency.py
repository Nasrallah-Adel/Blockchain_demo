# create czar currency 

#lib
import datetime
import hashlib
import json
from flask import Flask, jsonify,request
import requests
from uuid import uuid4
from urllib.parse import urlparse

#build a blockchain
class Blockchain:
    
    def __init__(self):
        self.chain=[]
        self.transactions=[]
        self.create_block(proof=1,previous_hash='0')
        self.nodes=set()
            
        
        
    def create_block(self,proof,previous_hash):
        block={'index':len(self.chain)+1,
               'timestamp':str(datetime.datetime.now()),
               'proof':proof,
               'previous_hash':previous_hash,
               'transactions':self.transactions}
        self.transactions=[]
        self.chain.append(block)
        return block
    
    
    def get_previous_block(self):
        return self.chain[-1]
    
    def proof_of_work(self,previous_proof):
        new_proof=1
        check_proof=False
        while check_proof is False:
            hash_operation=hashlib.sha256(str(new_proof**2-previous_proof**2).encode( )).hexdigest()
            if hash_operation [:4] == '0000':
                check_proof=True
            else:
                new_proof+=1
        
        return new_proof
    
    
    def hash(self,block):
        encoded_block =  json.dumps(block,sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self,chain):
        previous_block=chain[0]
        block_index=1
        while block_index < len(chain):
             block = chain[block_index]
             if block['previous_hash'] !=self.hash(previous_block):
                 return False
             previous_proof = previous_block['proof']
             proof=block['proof']
             hash_operation=hashlib.sha256(str(proof**2-previous_proof**2).encode( )).hexdigest()
             if hash_operation [:4] != '0000':
                 return False
             previous_block = block
             block_index +=1
        return True
    
       
    def add_transaction(self, sender , receiver, amount):
        self.transactions.append({'sender':sender,'receiver':receiver,'amount':amount})
        previous_block=self.get_previous_block()
        return previous_block['index']+1
    
    
    def add_node(self,address_of_node):
        parse_url = urlparse(address_of_node)
        self.nodes.add(parse_url.netloc)
        
    def replace_chain(self):
        network=self.nodes
        longest_chain=None
        max_length=len(self.chain)
        for nodes in network:
            response = requests.get(f'http://{nodes}/get_chain')
            if response.status_code == 200:
               length= response.json()['length']
               chain= response.json()['chain']
               if length > max_length and self.is_chain_valid(chain):
                   max_length=length
                   longest_chain = chain
        if longest_chain:
            self.chain = longest_chain

            return True
        return False
        
#mining  our blockchain
        

#create a web app flask
app =Flask(__name__)        
#create address for the node
node_address= str(uuid4()).replace('-','')

    
#create object of blockchain
blockchain_obj = Blockchain()

    # mining a new block

@app.route('/mining_block' , methods=['GET'])
def mining_block():
    previous_block=blockchain_obj.get_previous_block()
    previous_proof=previous_block['proof']
    proof=blockchain_obj.proof_of_work(previous_proof)
    previous_hash=blockchain_obj.hash(previous_block)
    blockchain_obj.add_transaction(sender=node_address,receiver='nasrallah',amount=10)
    block=blockchain_obj.create_block(proof,previous_hash)
    response={'message':"congrat you just mind a block",
              'index':block['index']
              ,'timestamp':block['timestamp']
              ,'proof':block['proof']
              ,'previous_hash':block['previous_hash']
              ,'transactions':block['transactions']}
    
    return jsonify(response),200
    
    
@app.route('/get_chain' , methods=['GET'])
def get_chain():
    response={'chain':blockchain_obj.chain,
              'length':len(blockchain_obj.chain)}
    
    return jsonify(response),200
    
   
@app.route('/is_chain_valid' , methods=['GET'])
def is_chain_valid():
    is_valid=blockchain_obj.is_chain_valid(blockchain_obj.chain)
    if is_valid:
        response={'message':'all good the blockchain is valid'}
    else:
        response={'message':'we have a problem , the blockchain not valid'}
    return jsonify(response),200 #ok

@app.route('/add_transaction' , methods=['POST'])
def add_transactions():
    json = request.get_json()
    transactions_keys=['sender','receiver','amount']
    if not all (key in json for key in transactions_keys):
        return 'some data missing',400 
    index = blockchain_obj.add_transaction(json['sender'],json['receiver'],json['amount'])
    response = {'message':f'your transaction will be added to block {index}'}
    return jsonify(response),201 #created

# decentrslizing our blockchain 
#connecting new nodes
@app.route('/connect_node' , methods=['POST'])
def connect_node():
    json=request.get_json()
    nodes=json.get('nodes')
    if nodes is None:
        return "No node", 400
    for node in nodes:
        blockchain_obj.add_node(node)
    response={'message':'all the nodes are now connected','total_nodes':list(blockchain_obj.nodes)}
    return jsonify(response),201
#replace the chain by the longest chain if needed
     
@app.route('/replace_chain' , methods=['GET'])
def replace_chain():
    is_chain_replaced=blockchain_obj.replace_chain()
    
    if is_chain_replaced:
        response={'message':'all good the nodes had differant chaines so the chain was replaced by the longest one'
                  ,'new chain':blockchain_obj.chain}
    else:
        response={'message':'all good , the chain is the largest one'
                  ,'the chain':blockchain_obj.chain}
    return jsonify(response),200 #ok

#run the app
app.run(host='127.0.0.1',port=5000 )
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
     
    