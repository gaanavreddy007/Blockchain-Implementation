import hashlib
import time
import json
from typing import List, Optional

class Transaction:
    """Represents a single transaction in the blockchain."""
    def __init__(self, sender: str, recipient: str, amount: float):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = time.time()
    
    def to_dict(self) -> dict:
        """Convert transaction to dictionary for hashing."""
        return {
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount,
            'timestamp': self.timestamp
        }

class Block:
    """Represents a single block in the blockchain."""
    def __init__(self, index: int, transactions: List[Transaction], previous_hash: str):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """
        Calculate the hash of the block using SHA-256.
        Includes all block data in the hash calculation.
        """
        block_content = {
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': [t.to_dict() for t in self.transactions],
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }
        block_string = json.dumps(block_content, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty: int) -> None:
        """
        Implements proof-of-work algorithm.
        The block hash must start with the specified number of zeros.
        """
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block mined! Nonce: {self.nonce}")

class IndianBlockchain:
    """Manages the blockchain with support for adding and validating blocks."""
    def __init__(self, difficulty: int = 4):
        self.chain: List[Block] = []
        self.difficulty = difficulty
        self.pending_transactions: List[Transaction] = []
        self.create_genesis_block()
    
    def create_genesis_block(self) -> None:
        """Create the first block (genesis block) in the chain."""
        genesis_block = Block(0, [], "0" * 64)
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)
        print("Genesis block created and mined!")
    
    def get_latest_block(self) -> Block:
        """Return the most recent block in the chain."""
        return self.chain[-1]
    
    def add_transaction(self, sender: str, recipient: str, amount: float) -> None:
        """Add a new transaction to pending transactions."""
        transaction = Transaction(sender, recipient, amount)
        self.pending_transactions.append(transaction)
        print(f"Transaction added: {sender} -> {recipient}: ₹{amount}")
    
    def mine_pending_transactions(self, miner_address: str) -> None:
        """
        Create a new block with pending transactions and add it to the chain.
        Miner receives a reward in cryptocurrency.
        """
        # Add mining reward
        self.add_transaction("Network", miner_address, 10.0)
        
        block = Block(
            len(self.chain),
            self.pending_transactions,
            self.get_latest_block().hash
        )
        
        print(f"\nMining block {block.index}...")
        block.mine_block(self.difficulty)
        
        self.chain.append(block)
        self.pending_transactions = []
        print(f"Block {block.index} has been added to the chain!")
    
    def is_chain_valid(self) -> bool:
        """
        Validate the entire blockchain.
        Returns True if the chain is valid, False if tampering is detected.
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            # Check current block hash
            if current_block.hash != current_block.calculate_hash():
                print(f"❌ Invalid hash detected in block {i}")
                return False
            
            # Check block linkage
            if current_block.previous_hash != previous_block.hash:
                print(f"❌ Invalid chain linkage detected at block {i}")
                return False
            
            # Verify proof of work
            if current_block.hash[:self.difficulty] != "0" * self.difficulty:
                print(f"❌ Invalid proof of work detected in block {i}")
                return False
        
        print("✅ Blockchain is valid!")
        return True

def demonstrate_blockchain():
    """Demonstrate the blockchain's functionality with Indian names."""
    # Create blockchain
    print("🔗 Creating IndianBlockchain...")
    blockchain = IndianBlockchain(difficulty=4)
    
    # Add transactions
    print("\n📝 Adding transactions...")
    blockchain.add_transaction("Rajesh", "Priya", 1000.0)
    blockchain.add_transaction("Priya", "Amit", 500.0)
    blockchain.add_transaction("Amit", "Sneha", 200.0)
    
    # Mine first block
    print("\n⛏️ Mining first block...")
    blockchain.mine_pending_transactions("Suresh")
    
    # Add more transactions
    print("\n📝 Adding more transactions...")
    blockchain.add_transaction("Vikram", "Neha", 300.0)
    blockchain.add_transaction("Neha", "Rahul", 150.0)
    
    # Mine second block
    print("\n⛏️ Mining second block...")
    blockchain.mine_pending_transactions("Suresh")
    
    # Validate the chain
    print("\n🔍 Validating blockchain...")
    blockchain.is_chain_valid()
    
    # Demonstrate tampering detection
    print("\n🔐 Demonstrating tampering detection...")
    print("Attempting to modify a transaction...")
    blockchain.chain[1].transactions[0].amount = 2000.0
    blockchain.is_chain_valid()
    
    # Print the entire blockchain
    print("\n📊 Blockchain contents:")
    for block in blockchain.chain:
        print(f"\nBlock #{block.index}")
        print(f"Timestamp: {time.ctime(block.timestamp)}")
        print(f"Previous Hash: {block.previous_hash}")
        print(f"Hash: {block.hash}")
        print("Transactions:")
        for tx in block.transactions:
            print(f"  {tx.sender} -> {tx.recipient}: ₹{tx.amount}")

if __name__ == "__main__":
    demonstrate_blockchain()
