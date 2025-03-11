import hashlib
import time
import random
import string


# Helper function to create unique IDs for obfuscation
def unique_address():
    timestamp = str(int(time.time()))  # Using current timestamp for uniqueness
    random_part = ''.join(random.choices(string.ascii_letters + string.digits, k=16))  # Random string part
    combined_string = timestamp + random_part  # Combine timestamp and random part
    return hashlib.sha256(combined_string.encode('utf-8')).hexdigest()  # Return hash as a unique address


# Block class to represent a single block in the blockchain
class Block:
    def __init__(self, sender, receiver, amount, previous_hash=''):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.previous_hash = previous_hash
        self.timestamp = time.time()
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.sender}{self.receiver}{self.amount}{self.timestamp}{self.previous_hash}"
        return hashlib.sha256(block_string.encode('utf-8')).hexdigest()


# Blockchain class to represent the entire chain
class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.vortex_reached = False
        self.create_genesis_block()

    def create_genesis_block(self):
        # Create the first block (genesis block)
        genesis_block = Block(sender="0", receiver="0", amount=0)
        self.chain.append(genesis_block)

    def add_transaction(self, sender, receiver, amount):
        if self.vortex_reached:
            print("Blockchain has reached vortex. Transaction will not be processed.")
            return

        # Add transaction to pending list
        self.pending_transactions.append({'sender': sender, 'receiver': receiver, 'amount': amount})

    def process_transactions(self):
        if self.vortex_reached:
            print("Blockchain has reached vortex. Processing is no longer possible.")
            return

        if not self.pending_transactions:
            print("No transactions to process.")
            return

        # Process each pending transaction
        for transaction in self.pending_transactions:
            sender = transaction['sender']
            receiver = transaction['receiver']
            amount = transaction['amount']
            last_block = self.chain[-1]

            # Create a new block for the transaction
            new_block = Block(sender, receiver, amount, previous_hash=last_block.hash)
            self.chain.append(new_block)

            # Print the transaction details
            print(f"Transaction added to block: {transaction}")

        # Clear pending transactions
        self.pending_transactions = []

        # Simulate reaching the vortex server after a certain number of blocks
        if len(self.chain) >= 5:  # Example condition for reaching the vortex
            self.reach_vortex()

    def reach_vortex(self):
        # Handle the destruction of the blockchain and creation of a new one for obfuscation
        print("Blockchain has reached the vortex server!")
        self.vortex_reached = True

        # Retain tokens and create a new blockchain with a new unique sender address
        retained_tokens = sum(block.amount for block in self.chain)
        print(f"Tokens retained: {retained_tokens}")

        # Create a new unique address for the new blockchain
        obfuscated_sender = unique_address()
        print(f"New obfuscated sender: {obfuscated_sender}")

        # Generate a new blockchain for the obfuscated sender
        new_blockchain = Blockchain()
        new_blockchain.add_transaction(sender=obfuscated_sender, receiver="recipient", amount=retained_tokens)
        print("New blockchain created with retained tokens.")

        # Destroy this blockchain
        self.destroy_blockchain()

    def destroy_blockchain(self):
        # "Destroy" the blockchain (clear all data)
        self.chain.clear()
        self.pending_transactions.clear()
        print("Blockchain destroyed.")

    def get_balance(self, address):
        balance = 0
        for block in self.chain:
            if block.receiver == address:
                balance += block.amount
            elif block.sender == address:
                balance -= block.amount
        return balance


# Example usage of the blockchain program
if __name__ == "__main__":
    blockchain = Blockchain()

    # Adding some transactions
    blockchain.add_transaction("Alice", "Bob", 50)
    blockchain.add_transaction("Bob", "Charlie", 30)

    # Process transactions
    blockchain.process_transactions()

    # Adding more transactions
    blockchain.add_transaction("Charlie", "David", 40)
    blockchain.add_transaction("David", "Alice", 20)

    # Process transactions again
    blockchain.process_transactions()

    # Getting balance of an address (e.g., Alice)
    print("Alice's balance:", blockchain.get_balance("Alice"))

    # Once the blockchain reaches the vortex, it will be destroyed
    blockchain.process_transactions()  # This will trigger vortex and destruction
