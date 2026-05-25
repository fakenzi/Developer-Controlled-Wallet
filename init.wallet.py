import os
import sys
import secrets
import time

from dotenv import load_dotenv
from circle.web3 import utils
from circle.web3 import developer_controlled_wallets


# =========================================================
# 加载环境变量
# =========================================================

load_dotenv()

API_KEY = os.getenv("CIRCLE_API_KEY")

if not API_KEY:
    print("❌ 请先在 .env 文件中配置 CIRCLE_API_KEY")
    sys.exit(1)


print("🌟 === 开始初始化 Circle Arc Agent Wallet === 🌟\n")


# =========================================================
# 1. 检查 Entity Secret
# =========================================================

ENTITY_SECRET_HEX = os.getenv("CIRCLE_ENTITY_SECRET")

if ENTITY_SECRET_HEX:

    print("🔑 1. 检测到已有 Entity Secret")
    print("   ✅ 将继续使用已有主密钥")

else:

    print("🎲 1. 未检测到 Entity Secret")
    print("   正在生成新的主密钥...")

    ENTITY_SECRET_HEX = secrets.token_hex(32)

    print("   ✅ Entity Secret 已生成")


# =========================================================
# 2. 检查 Recovery File
# =========================================================

print("\n📂 2. 正在检查 Recovery File...")

dat_files = [f for f in os.listdir(".") if f.endswith(".dat")]

if dat_files:

    print("   ⚠️ 检测到已有 Recovery File:")

    for file in dat_files:
        print(f"   - {file}")

    # 如果没有 ENV Secret 但存在 dat 文件
    if not os.getenv("CIRCLE_ENTITY_SECRET"):

        print("\n❌ 检测到 Recovery File，但 .env 中没有 Entity Secret")
        print("说明你之前生成过钱包，但丢失了主密钥")

        print("\n👉 请删除:")
        print("1. 当前目录下所有 .dat 文件")
        print("2. .env")

        print("\n然后重新运行脚本")

        sys.exit(1)

else:

    print("   ✅ 未检测到旧 Recovery File")


# =========================================================
# 3. 注册 Entity Secret
# =========================================================

print("\n🔐 3. 正在登记 Entity Secret...")

try:

    utils.register_entity_secret_ciphertext(
        api_key=API_KEY,
        entity_secret=ENTITY_SECRET_HEX
    )

    print("   ✅ Entity Secret 注册成功")
    print("   ✅ Recovery File 已下载")

except Exception as e:

    error_msg = str(e).lower()

    # 已注册属于正常情况
    if "already registered" in error_msg:

        print("   ⚠️ Entity Secret 已注册")
        print("   ✅ 自动继续执行")

    else:

        print(f"   ❌ Entity Secret 注册失败:\n{e}")
        sys.exit(1)


# =========================================================
# 4. 初始化 Circle Client
# =========================================================

print("\n🔌 4. 正在初始化 Circle Client...")

try:

    dcw_client = utils.init_developer_controlled_wallets_client(
        api_key=API_KEY,
        entity_secret=ENTITY_SECRET_HEX
    )

    print("   ✅ Circle Client 初始化成功")

except Exception as e:

    print(f"   ❌ Circle Client 初始化失败:\n{e}")

    print("\n💡 可能原因:")
    print("1. Entity Secret 与 Recovery File 不匹配")
    print("2. 你删除了 .env")
    print("3. 你重新生成了新的 Entity Secret")

    print("\n👉 请删除:")
    print("- .env")
    print("- 所有 .dat 文件")

    print("\n然后重新运行脚本")

    sys.exit(1)


# =========================================================
# 5. 创建 Wallet Set
# =========================================================

print("\n📦 5. 正在创建 Wallet Set...")

try:

    wallet_sets_api = developer_controlled_wallets.WalletSetsApi(dcw_client)

    unique_set_name = f"Auto_Agent_Set_{int(time.time())}"

    set_request = developer_controlled_wallets.CreateWalletSetRequest.from_dict({
        "name": unique_set_name
    })

    set_response = wallet_sets_api.create_wallet_set(
        create_wallet_set_request=set_request
    )

    wallet_set = (
        set_response
        .model_dump()
        .get("data", {})
        .get("wallet_set", {})
    )

    wallet_set_id = wallet_set.get("id")

    print("   ✅ Wallet Set 创建成功")

    print(f"\n   🆔 Wallet Set ID:")
    print(f"   {wallet_set_id}")

except Exception as e:

    print(f"   ❌ 创建 Wallet Set 失败:\n{e}")
    sys.exit(1)


# =========================================================
# 6. 创建 ARC Wallet
# =========================================================

print("\n🚀 6. 正在创建 ARC-TESTNET Wallet...")

try:

    wallets_api = developer_controlled_wallets.WalletsApi(dcw_client)

    wallet_request = {
        "blockchains": ["ARC-TESTNET"],
        "walletSetId": wallet_set_id,
        "count": 1
    }

    wallet_response = wallets_api.create_wallet(
        create_wallet_request=wallet_request
    )

    wallets_list = (
        wallet_response
        .model_dump()
        .get("data", {})
        .get("wallets", [])
    )

    if not wallets_list:

        print("   ❌ 未获取到钱包信息")
        sys.exit(1)

    agent_wallet = wallets_list[0]

    wallet_id = agent_wallet.get("id")
    agent_address = agent_wallet.get("address")

    print("   ✅ ARC Wallet 创建成功")

    print(f"\n   🆔 Wallet ID:")
    print(f"   {wallet_id}")

    print(f"\n   🌐 Wallet Address:")
    print(f"   {agent_address}")

except Exception as e:

    print(f"   ❌ 创建 ARC Wallet 失败:\n{e}")
    sys.exit(1)


# =========================================================
# 7. 写入 .env
# =========================================================

print("\n💾 7. 正在写入 .env 文件...")

env_content = f"""
# ==========================================
# Circle Agent Wallet
# ==========================================

CIRCLE_API_KEY={API_KEY}

CIRCLE_ENTITY_SECRET={ENTITY_SECRET_HEX}

CIRCLE_WALLET_SET_ID={wallet_set_id}

CIRCLE_AGENT_WALLET_ID={wallet_id}

CIRCLE_AGENT_ADDRESS={agent_address}
"""

try:

    with open(".env", "w", encoding="utf-8") as f:
        f.write(env_content.strip())

    print("   ✅ .env 写入成功")

except Exception as e:

    print(f"   ❌ .env 写入失败:\n{e}")


# =========================================================
# 完成
# =========================================================

print("\n========================================================")
print("🎉 Circle Agent Wallet 初始化完成")
print("========================================================")

print("\n🌐 Agent Address:")
print(agent_address)

print("\n💡 下一步:")
print("1. 去 Faucet 领取测试 USDC")
print("2. 运行 send_usdc.py")
print("3. 查询 tx hash")

print("\n========================================================")