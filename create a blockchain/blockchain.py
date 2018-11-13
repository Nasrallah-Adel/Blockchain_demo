# create blockchain

#lib
import datetime
import hashlib
import json
from flask import Flask, jsonify

#build a blockchain
class Blockchain:
    def __init__(self):
        self.chain=[]
        self.create_block(proof=1,previous_hash='0')
        
        
    def create_block(self,proof,previous_hash):
        block={'index':len(self.chain)+1,
               'timestamp':str(datetime.datetime.now()),
               'proof':proof,
               'previous_hash':previous_hash
               }
        
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
                
#mining  our blockchain
        

#create a web app flask
app =Flask(__name__)        

    

#create object of blockchain
blockchain_obj = Blockchain()

    # mining a new block



@app.route('/mining_block' , methods=['GET'])
def mining_block():
    previous_block=blockchain_obj.get_previous_block()
    previous_proof=previous_block['proof']
    proof=blockchain_obj.proof_of_work(previous_proof)
    previous_hash=blockchain_obj.hash(previous_block)
    block=blockchain_obj.create_block(proof,previous_hash)
    response={'message':"congrat you just mind a block",
              'index':block['index']
              ,'timestamp':block['timestamp']
              ,'proof':block['proof']
              ,'previous_hash':block['previous_hash']
              ,'hash':blockchain_obj.hash(block)}
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
    return jsonify(response),200
 
#run the app
app.run(host='127.0.0.1',port=5000 )
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
     
    