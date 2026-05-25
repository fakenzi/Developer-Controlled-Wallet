# Circle-DevWallet-QuickStart

🚀 **Circle Developer Controlled Wallets（Agent Wallet）快速上手工具包**

5 分钟完成钱包初始化、测试网 USDC 领取与转账。

---

## ✨ 项目特点

- 使用 Circle 官方 SDK 开发者控制钱包（Agent Wallet）
- 一键初始化钱包 + 自动保存配置到 `.env`
- 支持测试网 USDC 转账
- 自动等待链上确认并显示 Explorer 链接
- 安全使用 `.env` 配置

---

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
### 5. 发送usdc 
python send_usdc.py
