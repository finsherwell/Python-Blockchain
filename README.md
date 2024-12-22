# Python-Blockchain
Simple, lightweight blockchain written primarily in python.

## Blockchain Implementation with Validation Tests
# Overview
This project includes a simple implementation of a blockchain, written in python. It includes features such as:
- Adding transactions and blocks
- Validating the integrity of the blockchain
- Implements proof-of-work mining
- Simulating invalid scenarios to test blockchain validation

# Features
- **Transaction Handling:** Tracks sender, receiver, and amount for each transaction.
- **Block Structure:** Stores a list of transactions, a timestamp, the Merkle root of transactions, the hash of the previous block, and a proof-of-work nonce.
- **Blockchain:** Ensures integrity and linkage between blocks.
- **Validation:** Verifies that each block’s hash matches its contents and that all blocks are linked correctly.

# Code Structure
1. **Transaction Class:**
- Represents a transaction with attributes for the sender, receiver, amount, and timestamp.
2. **Block Class:**
- Contains a list of transactions, the Merkle root, a hash of the previous block, and its own hash.
- Implements proof-of-work mining.
3. **Blockchain Class:**
- Manages a list of blocks.
- Creates a genesis block and adds new blocks while maintaining integrity.
- Validates the chain to ensure it has not been tampered with.

# Testing Validity
Three test cases are included to evaluate the blockchain:
1. **Valid Blockchain:**
A properly functioning blockchain that passes all validation checks.

**Expected Output:**
- The blockchain prints all blocks with valid hashes.
- Validation output: Is blockchain valid? True

2. **Blockchain with Tampered Hash:**
A blockchain where the hash of a block is deliberately altered.

**Expected Output:**
- The blockchain prints the tampered block.
- Validation output: ```Block <index> has been tampered with! Is blockchain valid? False```

3. **Blockchain with Broken Linkage:**
A blockchain where the previous_hash of a block is deliberately altered.

**Expected Output:**
- The blockchain prints the block with broken linkage.
- Validation output: ```Block <index> is not linked correctly to the previous block! Is blockchain valid? False```

# Usage
To run the program:
1. Install Python
2. Clone the repository
3. Execute the script
```
python main.py
```

# Example Output
Below is a sample output demonstrating the three test cases:
```
Valid Blockchain:
Block 0:
<Details of Genesis Block>
...
Is blockchain valid? True

-------------------------------------------------

Blockchain with Tampered Hash:
Block 0:
<Details of Genesis Block>
Block 1:
<Details of Tampered Block>
...
Block 1 has been tampered with!
Is blockchain valid? False

-------------------------------------------------

Blockchain with Broken Linkage:
Block 0:
<Details of Genesis Block>
Block 1:
<Details of Block 1>
Block 2:
<Details of Block 2 with broken linkage>
...
Block 2 is not linked correctly to the previous block!
Is blockchain valid? False
```

# Additional Notes
- **Proof-Of-Work:** The ```mine_block``` method simulates mining by requiring a hash with a specific number of leading zeros.
- **Merkle Root:** Ensures efficient and secure transaction representation.
- **Validation:** Ensures that tampered data is detected to prevent fraudulent modifications.

# Future Enhancements
In the future, I may add more features to improve this blockchain implementation, such as:
- Persistant storage for the blockchain
- Cryptographic signatures for transactions
- Network simulation for multi-node blockchain communication