import hashlib
import time
from block import Block  # Import class Block từ block.py

class Blockchain:

    def __init__(self):
        """Khởi tạo một blockchain mới."""
        self.chain = []
        self.current_transactions = []
        self.create_block(proof=1, previous_hash='0')

    def create_block(self, proof, previous_hash):
        """Tạo một block mới và thêm nó vào blockchain."""
        block = Block(
            len(self.chain) + 1,
            previous_hash,
            time.time(),
            self.current_transactions,
            proof
        )
        self.current_transactions = []
        self.chain.append(block)
        return block

    def get_previous_block(self):
        """Trả về block cuối cùng trong blockchain."""
        if not self.chain:
            return None  # Xử lý trường hợp blockchain rỗng
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        """Thực hiện thuật toán proof-of-work."""
        new_proof = 1
        check_proof = False
        while not check_proof:
            hash_operation = hashlib.sha256(
                str(new_proof**2 - previous_proof**2).encode()
            ).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def add_transaction(self, sender, receiver, amount):
        """Thêm một giao dịch mới vào danh sách giao dịch hiện tại."""
        self.current_transactions.append({
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        })
        return self.get_previous_block().index + 1 if self.chain else 1 # xử lý trường hợp chain rỗng

    def is_chain_valid(self, chain):
        """Kiểm tra xem một blockchain có hợp lệ hay không."""
        if not chain:
            return True # blockchain rỗng là hợp lệ.
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block.previous_hash != previous_block.hash:
                return False
            previous_proof = previous_block.proof
            proof = block.proof
            hash_operation = hashlib.sha256(
                str(proof**2 - previous_proof**2).encode()
            ).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True