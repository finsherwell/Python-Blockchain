import hashlib
import datetime
from typing import List

def generate_hash(data):
    """Generate a SHA-256 hash for the given data."""
    return hashlib.sha256(data.encode()).hexdigest()

class Transaction:
    """Represents a single transaction in the blockchain."""
    def __init__(self, sender: str, receiver: str, amount: float):
        self.sender = sender # The sender of the transaction
        self.receiver = receiver # The receiver of the transaction
        self.amount = amount # The amount being transferred
        self.timestamp = datetime.datetime.now(datetime.UTC) # Timestamp of the transaction

    def __str__(self):
        """Returns a human-readable string representation of the transaction."""
        return f"{self.sender} -> {self.receiver}: {self.amount} BTC @ {self.timestamp}"

class Block:
    """Represents a single block in the blockchain."""
    def __init__(self, transactions: List[Transaction], previous_hash: str):
        self.transactions = transactions  # List of transactions in the block
        self.previous_hash = previous_hash  # Hash of the previous block
        self.timestamp = datetime.datetime.now(datetime.UTC)  # Timestamp for when the block is created
        self.merkle_root = self.calculate_merkle_root()  # Merkle root of the transactions
        self.nonce = 0  # Nonce used for mining (proof-of-work)
        self.hash = self.calculate_hash()  # Hash of the block (calculated based on block contents)
    
    def calculate_merkle_root(self) -> str:
        """Calculate the Merkle root of the transactions in the block."""
        if not self.transactions:
            return ""

        # Hash each transaction into a list of hashes
        transaction_hashes = [generate_hash(str(tx)) for tx in self.transactions]

        # Repeatedly combine and hash pairs of transaction hashes until one root hash remains
        while len(transaction_hashes) > 1:
            if len(transaction_hashes) % 2 == 1:  # Duplicate the last hash if there is an odd number
                transaction_hashes.append(transaction_hashes[-1])

            transaction_hashes = [
                generate_hash(transaction_hashes[i] + transaction_hashes[i + 1])
                for i in range(0, len(transaction_hashes), 2)
            ]

        return transaction_hashes[0]

    def calculate_hash(self) -> str:
        """Calculate the hash of the block using its contents."""
        block_data = f"{self.previous_hash}{self.timestamp}{self.merkle_root}{self.nonce}"
        return generate_hash(block_data)
    
    def mine_block(self, difficulty: int) -> None:
        """
        Perform proof of work by finding a hash that starts with a specified number of zeros.
        Difficulty determines the number of leading zeros.
        """
        target = 0 * difficulty  # The target pattern for the hash
        while not self.hash.startswith(str(target)):
            self.nonce += 1  # Increment the nonce to change the hash
            self.hash = self.calculate_hash()  # Recalculate the hash with the new nonce
    
    def __str__(self):
        """Returns a human-readable string representation of the block."""
        tx_list = "\n".join([str(tx) for tx in self.transactions])
        return f"Block: Transactions:\n{tx_list}\n  Previous Hash: {self.previous_hash}\n  Hash: {self.hash}\n  Merkle Root: {self.merkle_root}\n  Timestamp: {self.timestamp}\n  Nonce: {self.nonce}"

class Blockchain:
    """Represents the blockchain as a list of blocks."""
    def __init__(self, difficulty: int = 2):
        self.chain: List[Block] = []  # List to store all the blocks
        self.difficulty = difficulty  # Mining difficulty
        self.create_genesis_block()  # Create the genesis block (first block)

    def create_genesis_block(self) -> None:
        """Create the genesis block and add it to the chain."""
        genesis_block = Block(transactions=[], previous_hash="0")
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)

    def add_block(self, transactions: List[Transaction]) -> None:
        """Add a new block to the blockchain."""
        previous_hash = self.chain[-1].hash  # Use the hash of the last block in the chain
        new_block = Block(transactions, previous_hash)
        new_block.mine_block(self.difficulty)  # Perform proof-of-work mining
        self.chain.append(new_block)

    def is_chain_valid(self) -> bool:
        """Verify the integrity of the blockchain."""
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            # Check if the current block's hash matches its recalculated hash
            if current.hash != current.calculate_hash():
                print(f"Block {i} has been tampered with!")
                return False

            # Check if the current block's previous_hash matches the previous block's hash
            if current.previous_hash != previous.hash:
                print(f"Block {i} is not linked correctly to the previous block!")
                return False

        return True

    def print_chain(self) -> None:
        """Print the blockchain."""
        for i, block in enumerate(self.chain):
            print(f"Block {i}:")
            print(block)
            print("-" * 50)

if __name__ == "__main__":
    # VALID BLOCKCHAIN
    print("Valid Blockchain:")
    valid_blockchain = Blockchain()

    valid_blockchain.add_block([
        Transaction("Alice", "Bob", 1.5),
        Transaction("Charlie", "Dave", 2.7)
    ])

    valid_blockchain.add_block([
        Transaction("Eve", "Frank", 0.4),
        Transaction("Grace", "Heidi", 3.0)
    ])

    valid_blockchain.add_block([
        Transaction("Ivan", "Judy", 0.9)
    ])

    valid_blockchain.print_chain()
    print("Is blockchain valid?", valid_blockchain.is_chain_valid())
    print("\n" + "="*50 + "\n")

    # BLOCKCHAIN WITH TAMPERED HASH
    print("Blockchain with Tampered Hash:")
    tampered_blockchain = Blockchain()

    tampered_blockchain.add_block([
        Transaction("Alice", "Bob", 1.5),
        Transaction("Charlie", "Dave", 2.7)
    ])

    tampered_blockchain.add_block([
        Transaction("Eve", "Frank", 0.4),
        Transaction("Grace", "Heidi", 3.0)
    ])

    # Tamper with the hash of the second block
    tampered_blockchain.chain[1].hash = "tampered_hash"

    tampered_blockchain.print_chain()
    print("Is blockchain valid?", tampered_blockchain.is_chain_valid())
    print("\n" + "="*50 + "\n")

    # BLOCKCHAIN WITH BROKEN LINKAGE
    print("Blockchain with Broken Linkage:")
    broken_link_blockchain = Blockchain()

    broken_link_blockchain.add_block([
        Transaction("Alice", "Bob", 1.5),
        Transaction("Charlie", "Dave", 2.7)
    ])

    broken_link_blockchain.add_block([
        Transaction("Eve", "Frank", 0.4),
        Transaction("Grace", "Heidi", 3.0)
    ])

    # Break the chain linkage by modifying the previous_hash of the third block
    broken_link_blockchain.chain[2].previous_hash = "incorrect_previous_hash"

    broken_link_blockchain.print_chain()
    print("Is blockchain valid?", broken_link_blockchain.is_chain_valid())