# Import libraries
import streamlit as st
from dataclasses import dataclass
from datetime import datetime
from typing import Any, List
import datetime as datetime
import pandas as pd
import hashlib

# Create a Record Data Class
@dataclass # dataclass decorator defines our data class
class Record:
    sender: str
    receiver: str
    amount: float

# Create Block Data Class to store the record data by adding a data attribute called "record" 
@dataclass 
class Block:
    record: Record # Add class "Record" defined above
    creator_id: int
    timestamp: str = datetime.datetime.utcnow().strftime("%H:%M:%S")
    prev_hash: str = "0"
    nonce: int = 0 
        
# Here we are encrypting the "Block" data class, adding it to the hash, and then returning the hash:
    def hash_block(self):
        sha = hashlib.sha256()
    
        record = str(self.record).encode()
        sha.update(record)
    
        creator_id = str(self.creator_id).encode()
        sha.update(creator_id)
    
        prev_hash = str(self.prev_hash).encode()
        sha.update(prev_hash)

        timestamp = str(self.timestamp).encode()
        sha.update(timestamp)
    
        nonce = str(self.nonce).encode()
        sha.update(nonce)
    
        return sha.hexdigest()

# Create PyChain class
@dataclass 
class PyChain:
    chain: List[Block] # Connect blocks together using PyChain
    difficulty: int = 4

# Create Proof of Work function
    def proof_of_work(self, block):
        calculated_hash = block.hash_block()  # Calculates hash of current block
        num_of_zeroes = "0" * self.difficulty # Defines the difficulty/pattern we are looking for 
        while not calculated_hash.startswith(num_of_zeroes): # Loop until we find the pattern of four "0"s at the beginning of our hash code (i.e. the hash pattern)          
            block.nonce += 1 # Matches the difficulty level given above and increases the number of nonces until we meet the pattern of four "0"s at the beginning of the hash code
            calculated_hash = block.hash_block()
        print("Winning Hash", calculated_hash)
        return block  # If matching pattern is found, print the "winning hash" 

# Validate Candidate Block and Verify Chain is Valid
    def add_block(self, candidate_block): 
        block = self.proof_of_work(candidate_block) 
        self.chain += [block] 
        
    def is_valid(self): 
        block_hash = self.chain[0].hash_block() # Identify hash value of first block in chain
        
        for block in self.chain[1:]: # For each block within the remainder of the chain, check if the hash of the current block is different than the hash of the previous block 
            if block_hash != block.prev_hash: 
                print("Blockchain is invalid!") 
                return False
            
            block_hash = block.hash_block() # At this step we know that each block in the chain has been validated and there were no differences - the blockchain is valid
        print("Blockchain is Valid")
        return True 

# Streamlit Code
@st.cache(allow_output_mutation=True) # This will only update content that has changed, everything else will be cached when a button is clicked
def setup():
    print("Initializing Chain")
    return PyChain([Block("Genesis", 0)]) # Create first "Genesis" block on PyChain

st.markdown("# PyChain")
st.markdown("## Store a Transaction Record in the PyChain")

pychain = setup()

########################################################################################################################

# Add Relevant User Inputs to the Streamlit Interface

# Create input for getting the sender from the user
sender = st.text_input("Sender")

# Create input for getting the receiver from the user
receiver = st.text_input("Receiver")

# Create input for getting the value to be sent
amount = st.number_input("Amount")

# Create "Add Block" button 
if st.button("Add Block"):
    prev_block = pychain.chain[-1]
    prev_block_hash = prev_block.hash_block()

# Set value of the last block's hash in chain
last_block_hash = pychain.chain[-1].hash_block() 

# Update 'new_block' with sender, receiver and amount values
new_block = Block(
    record = Record(amount, sender, receiver),
    creator_id = 42,
    prev_hash = last_block_hash
)

pychain.add_block(new_block)
st.balloons()

########################################################################################################################

# Streamlit Code (continues)

st.markdown("## The PyChain Ledger")

pychain_df = pd.DataFrame(pychain.chain).astype(str)
st.write(pychain_df)

difficulty = st.sidebar.slider("Block Difficulty", 1, 5, 2)
pychain.difficulty = difficulty

st.sidebar.write("# Block Inspector")
selected_block = st.sidebar.selectbox(
    "Which block would you like to see?", pychain.chain
)

st.sidebar.write(selected_block)

if st.button("Validate Chain"):
    st.write(pychain.is_valid())
