import hashlib
import datetime

def generate_hash(data):
    hash = hashlib.sha256(data.encode())
    return hash.hexdigest()

class Transaction:
    def __init__(self, transaction_type, amount):
        self.transaction_type = transaction_type
        self.amount = amount


class Block:
    def __init__(self, transactions, hash, previousHash):
        self.transactions = transactions
        self.hash = hash
        self.previousHash = previousHash
        self.timestamp = datetime.datetime.now(datetime.UTC)
    
    def get_previous_hash(self):
        return self.previousHash
    
    def get_transactions(self):
        return self.transactions
    
class Blockchain:
    def __init__(self):
        hash_first = generate_hash('hash_first')
        hash_last = generate_hash('hash_last')
        transaction = Transaction('btc', 1.2)

        genesis = Block(transaction, hash_first, hash_last)
        self.chain = [genesis]

    def add_block(self, data):
        prev_hash = self.chain[-1].hash
        hash = generate_hash(data+prev_hash)
        block = Block(data, hash, prev_hash)
        self.chain.append(block)

if __name__ == "__main__":
