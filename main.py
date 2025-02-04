from web3 import Web3
import time
import random

# Подключение к провайдерам для разных сетей
provider_op = ""https://opt-sepolia.g.alchemy.com/v2/5ldNCcjz_ocN-wBjQSyZlUYxzl5H7mkI"  # OP Sepolia
provider_arb = ""https://arb-sepolia.g.alchemy.com/v2/5ldNCcjz_ocN-wBjQSyZlUYxzl5H7mkI"  # Arbitrum Sepolia

web3_op = Web3(Web3.HTTPProvider(provider_op))
web3_arb = Web3(Web3.HTTPProvider(provider_arb))

# Проверяем подключение к сетям
if not web3_op.is_connected():
    raise ConnectionError("Failed to connect to OP Sepolia network.")
if not web3_arb.is_connected():
    raise ConnectionError("Failed to connect to Arbitrum Sepolia network.")

# Данные отправителя и приватный ключ
sender_address = "0x92Eb2fc672C74df59F110004818Ac907f0208594"
private_key = "0xYourPrivateKeyHere"  # Укажите ваш приватный ключ

# Функция для отправки транзакции
def send_transaction(web3, chain_id, to_address, data):
    try:
        nonce = web3.eth.get_transaction_count(sender_address)
        print(f"Using nonce: {nonce} on chain ID {chain_id}")

        base_fee = web3.eth.get_block("latest")["baseFeePerGas"]
        max_priority_fee = web3.to_wei(2, "gwei")
        max_fee = base_fee + max_priority_fee

        transaction = {
            "chainId": chain_id,
            "from": sender_address,
            "to": to_address,
            "value": web3.to_wei(1.6, "ether"),
            "maxFeePerGas": max_fee,
            "maxPriorityFeePerGas": max_priority_fee,
            "nonce": nonce,
            "data": data,
        }

        transaction["gas"] = web3.eth.estimate_gas(transaction)

        signed_tx = web3.eth.account.sign_transaction(transaction, private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"Transaction sent! Hash: {tx_hash.hex()}")

        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"Transaction {tx_hash.hex()} confirmed in block {receipt['blockNumber']}")
   
     # Увеличиваем счетчик успешных транзакций
        successful_transactions += 1

    except Exception as e:
        print(f"Error sending transaction: {str(e)}")

# Основной цикл чередования транзакций
for i in range(10000):
    print(f"\n--- Iteration {i+1} ---")

    # 1. Отправка транзакции в OP Sepolia
    send_transaction(
        web3=web3_op,
        chain_id=11155420,
        to_address="0xF221750e52aA080835d2957F2Eed0d5d7dDD8C38",
        data="0x56591d596172627400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000092Eb2fc672C74df59F110004818Ac907f020859400000000000000000000000000000000000000000000000015eef6f64cc9e0a30000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000016345785d8a00000"
    )

    # Пауза 2–5 секунд
    time.sleep(random.randint(2, 5))

    # 2. Отправка транзакции в Arbitrum Sepolia
    send_transaction(
        web3=web3_arb,
        chain_id=421614,
        to_address="0x8D86c3573928CE125f9b2df59918c383aa2B514D",
        data="0x56591d596f70737000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000092Eb2fc672C74df59F110004818Ac907f020859400000000000000000000000000000000000000000000000015eefbc4f29eb1d30000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000016345785d8a00000"
    )

    # Пауза 2–5 секунд
    wait_time = random.randint(2, 5)
    print(f"Waiting for {wait_time} seconds before the next iteration...")
    time.sleep(wait_time)

    print(f"\nTotal successful transactions so far: {successful_transactions}\n")
