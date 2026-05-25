
## 🚀 ** Circle Developer Controlled Wallets（Agent Wallet）Arc Testnet 快速上手工具包**

5 分钟完成钱包初始化、测试网 USDC 领取与转账。

---

## ✨ 项目特点

使用 Circle 官方 SDK 开发者控制钱包（Developer Controlled / Agent Wallet）
一键初始化钱包 + 自动保存配置到 .env
专为 Arc Testnet 优化：USDC 作为原生 Gas Token，无需额外 Gas 代币
支持ARC 测试网  发送转账
自动等待链上确认并显示 Arcscan Explorer 链接
安全使用 .env 配置，适合快速原型和 AI Agent 开发



## 🚀 快速开始

### 1. 克隆或下载项目

```bash
https://github.com/fakenzi/Developer-Controlled-Wallet.git
cd Circle-DevWallet-QuickStart
```
### 2.安装依赖
pip install -r requirements.txt

### 3. 配置环境变量
cp .env.example .env
### 4. 初始化钱包
python init.wallet.py
<img width="865" height="546" alt="03dac7c9deabb1f1c7feedf388a1a19c" src="https://github.com/user-attachments/assets/bfd225bf-30f8-4d71-9e58-d94e9d1c3018" />

### 5. 发送usdc 
python send_usdc.py

<img width="865" height="734" alt="383db8ab54c0b1630c327d327ea7b6ce" src="https://github.com/user-attachments/assets/d1a99935-3a47-4ad6-a618-a86e7e89bf06" />
