from blockchain import Blockchain

def main():

    # Tạo một blockchain mới
    my_blockchain = Blockchain()

    # Nhập giao dịch từ bàn phím
    sender = input("Nhập người gửi: ")
    receiver = input("Nhập người nhận: ")
    try:
        amount = int(input("Nhập số tiền: "))
    except ValueError:
        print("Số tiền phải là một số nguyên.")
        return  # Dừng chương trình nếu nhập sai

    # Thêm giao dịch vào blockchain
    transaction_index = my_blockchain.add_transaction(sender, receiver, amount)
    print(f"Giao dịch được thêm vào block tiếp theo (index: {transaction_index})")

    # Khai thác một block mới
    previous_block = my_blockchain.get_previous_block()
    previous_proof = previous_block.proof
    new_proof = my_blockchain.proof_of_work(previous_proof)
    previous_hash = previous_block.hash

    # Thêm giao dịch khai thác (reward)
    my_blockchain.add_transaction('Genesis', 'Miner', 1)

    # Tạo block mới
    new_block = my_blockchain.create_block(new_proof, previous_hash)
    print(f"Block mới được khai thác (index: {new_block.index})")

    # Hiển thị blockchain
    print("\nBlockchain:")
    for block in my_blockchain.chain:
        print(f"Block #{block.index}")
        print(f"  Timestamp: {block.timestamp}")
        print(f"  Transactions: {block.transactions}")
        print(f"  Proof: {block.proof}")
        print(f"  Previous Hash: {block.previous_hash}")
        print(f"  Hash: {block.hash}")
        print("  -------------------")

    # Kiểm tra tính hợp lệ của blockchain
    is_valid = my_blockchain.is_chain_valid(my_blockchain.chain)
    print(f"\nIs Blockchain Valid: {is_valid}")

if __name__ == "__main__":
    main()