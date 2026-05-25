import time
import uuid

from circle.web3 import developer_controlled_wallets
from circle.web3 import utils




API_KEY = "    " 

ENTITY_SECRET = "      "

WALLET_ID = "     "


TOKEN_ID = "15dc2b5d-0994-58b0-bf8c-3a0501148ee8"#usdc 的token id 




client = utils.init_developer_controlled_wallets_client(
    api_key=API_KEY,
    entity_secret=ENTITY_SECRET
)

tx_api = developer_controlled_wallets.TransactionsApi(client)




def get_transaction(tx_id):

    response = tx_api.get_transaction(id=tx_id)

    data = response.model_dump()

    return data["data"]["transaction"]




def send_usdc(destination_address: str, amount: str):

    print(f"\n🚀 开始发送 {amount} USDC")
    print(f"📬 接收地址: {destination_address}")

    request = developer_controlled_wallets.CreateTransferTransactionForDeveloperRequest.from_dict({

        "idempotencyKey": str(uuid.uuid4()),

        "walletId": WALLET_ID,

        "destinationAddress": destination_address,

        "amounts": [amount],

        "tokenId": TOKEN_ID,

        
        "feeLevel": "MEDIUM"
    })

    response = tx_api.create_developer_transaction_transfer(
        create_transfer_transaction_for_developer_request=request
    )

    result = response.model_dump()

    tx_id = result["data"]["id"]

    print(f"\n🆔 Transaction ID:")
    print(tx_id)

    return tx_id




def wait_for_complete(tx_id, timeout=120):

    print("\n⏳ 等待链上确认...")

    start = time.time()

    while True:

        tx = get_transaction(tx_id)

        state = tx["state"]

        print(f"当前状态: {state}")

        
        if state == "COMPLETE":

            tx_hash = tx["tx_hash"]

            print("\n✅ 转账成功!")
            print(f"🔗 TX HASH:\n{tx_hash}")

            explorer = f"https://testnet.arcscan.app/tx/{tx_hash}"

            print(f"\n🌐 Explorer:")
            print(explorer)

            return tx

        
        if state == "FAILED":

            print("\n❌ 转账失败")

            print(tx.get("error_reason"))

            return None

        # 超时
        if time.time() - start > timeout:

            print("\n⌛ 等待超时")

            return None

        time.sleep(3)




if __name__ == "__main__":

    
    to_address = "    "# 这里要给你发送测试币的钱包地址

    
    amount = "3"

    tx_id = send_usdc(
        destination_address=to_address,
        amount=amount
    )

    wait_for_complete(tx_id)