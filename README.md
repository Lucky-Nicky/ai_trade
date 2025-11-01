# AI Trade Game 🤖📈

一个多AI模型加密货币交易竞赛平台，让不同的AI模型在模拟环境中进行实时交易对决。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-3.0-green.svg)](https://flask.palletsprojects.com/)

[English](README.md) | [中文文档](AITradeGame/README_ZH.md)

## 📸 预览

实时监控多个AI模型的交易表现，支持：
- 📊 实时交易图表
- 🤖 多AI模型同时运行
- 💰 虚拟资金交易
- 🔐 操作密码保护
- 📈 持仓和盈亏分析

## ✨ 核心特性

### 🎯 多AI模型竞技
- 支持同时运行多个AI交易模型
- 兼容OpenAI、DeepSeek等主流AI API
- 每个模型独立账户和资金
- 实时排行榜比较模型表现

### 📊 实时数据源
- **多数据源支持**：Odaily星球日报、528btc、Binance、CoinGecko
- **自动切换**：主数据源失败时自动切换备用源
- **实时价格**：支持50+主流加密货币
- **灵活配置**：可自定义数据源优先级

### 💼 模拟交易功能
- 支持多空双向交易
- 杠杆交易（1-10倍）
- 实时盈亏计算
- 交易手续费模拟
- 完整的交易历史记录

### 🎨 现代化界面
- 响应式Web界面
- ECharts实时图表
- 多时间范围切换（30分钟-全部）
- 聚合视图 vs 单模型视图
- AI对话记录查看

### 🔒 安全特性
- **操作密码保护**：防止未授权操作
- **后端验证**：所有敏感操作后端强制验证
- **密码加密**：SHA256哈希存储
- **保护范围**：添加/删除模型、管理API、修改设置

## 🚀 快速开始

### 环境要求

- Python 3.12+
- Linux服务器（推荐Ubuntu/Debian）
- Nginx（可选，用于生产部署）

### 本地运行

```bash
# 1. 克隆仓库
git clone https://github.com/Lucky-Nicky/ai_trade.git
cd ai_trade/AITradeGame

# 2. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 初始化数据库
python init_db.py

# 5. 启动应用
python app.py
```

访问 http://localhost:5002

### 生产部署

完整部署指南请查看：[DEPLOY.md](DEPLOY.md)

**一键部署脚本**：
```bash
cd AITradeGame
sudo bash deploy.sh
```

自动配置：
- ✅ Flask应用（Systemd服务）
- ✅ Nginx反向代理
- ✅ 自动启动
- ✅ 日志管理

## 📖 使用指南

### 1. 设置操作密码（推荐）

首次使用建议设置密码保护：

1. 点击右上角"设置"按钮
2. 滚动到"操作密码保护"区域
3. 输入新密码（至少4位）
4. 确认密码并保存

详细说明：[PASSWORD_PROTECTION.md](PASSWORD_PROTECTION.md)

### 2. 添加AI API提供方

1. 点击"API提供方"按钮
2. 填写API信息：
   - 名称：例如 "OpenAI"
   - API地址：`https://api.openai.com`
   - API密钥：你的API Key
   - 可用模型：`gpt-4,gpt-3.5-turbo`
3. 保存

### 3. 创建交易模型

1. 点击"添加模型"按钮
2. 选择API提供方
3. 选择模型（如 gpt-4）
4. 设置显示名称和初始资金
5. 测试连接（可选）
6. 确认添加

### 4. 监控交易

- **聚合视图**：查看所有模型的汇总数据
- **单模型视图**：点击左侧模型列表查看详情
- **持仓**：查看当前持仓和盈亏
- **交易记录**：查看历史交易
- **AI对话**：查看AI的决策思考过程

## 🏗️ 项目结构

```
AITradeGame/
├── app.py                 # Flask主应用
├── database.py            # 数据库管理
├── ai_trader.py          # AI交易逻辑
├── trading_engine.py     # 交易引擎
├── market_data.py        # 市场数据获取
├── odaily_fetcher.py     # Odaily数据源
├── templates/            # HTML模板
│   └── index.html
├── static/               # 静态资源
│   ├── app.js           # 前端JavaScript
│   └── style.css        # 样式文件
├── requirements.txt      # Python依赖
├── deploy.sh            # 部署脚本
└── init_db.py           # 数据库初始化
```

## 🔧 配置选项

### 数据源配置

在"设置"界面可配置数据源优先级：

```
优先级示例：odaily,528btc,binance,coingecko
```

系统会按顺序尝试，第一个成功的将被使用。

### 交易参数

- **交易频率**：AI决策间隔（默认60分钟）
- **交易费率**：手续费比例（默认0.1%）
- **初始资金**：每个模型的起始资金

## 📊 数据来源

| 数据源 | 支持币种 | 稳定性 | 推荐指数 |
|--------|---------|--------|----------|
| Odaily星球日报 | 50+ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 528btc币界网 | 30+ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Binance API | 全部 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| CoinGecko | 全部 | ⭐⭐⭐ | ⭐⭐ |

## 🛠️ 常用命令

### 开发环境

```bash
# 停止应用
pkill -f "python.*app\.py"

# 启动应用
source venv/bin/activate
python app.py

# 查看日志
tail -f app.log

# 数据库迁移
python init_db.py
```

### 生产环境（Systemd）

```bash
# 重启服务
systemctl restart ai-trade-game.service

# 查看状态
systemctl status ai-trade-game.service

# 查看日志
journalctl -u ai-trade-game.service -f
```

完整命令参考：[QUICK_START.md](QUICK_START.md)

## 🔐 安全建议

### 本地开发
- ✅ 可以不设置密码
- ✅ 仅本地访问，风险较低

### 公网部署
- ⚠️ **必须**设置操作密码
- ⚠️ 使用强密码（8位以上）
- ⚠️ 配置HTTPS（SSL证书）
- ⚠️ 使用防火墙限制访问
- ⚠️ 定期更新密码

## 🐛 故障排查

### 502 Bad Gateway

```bash
# 检查Flask是否运行
ps aux | grep "python app.py"

# 检查端口
netstat -tulpn | grep 5002

# 查看日志
journalctl -u ai-trade-game.service -n 50
```

### 无法获取市场数据

检查数据源配置和网络连接：

```bash
# 测试数据源
python test_data_sources.py

# 查看详细错误
tail -f app.log | grep ERROR
```

### 密码忘记

重置密码：

```bash
cd AITradeGame
sqlite3 AITradeGame.db "UPDATE settings SET operation_password = NULL;"
# 重启应用后重新设置
```

## 📝 开发计划

- [ ] 添加更多AI模型支持（Claude、Gemini等）
- [ ] 支持更多交易对
- [ ] 历史数据回测功能
- [ ] 策略分析报告
- [ ] 邮件/Webhook通知
- [ ] Docker容器化
- [ ] 移动端适配

## 🤝 贡献

欢迎提交Issue和Pull Request！

1. Fork本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](AITradeGame/LICENSE) 文件。

## 🙏 致谢

- [Flask](https://flask.palletsprojects.com/) - Web框架
- [ECharts](https://echarts.apache.org/) - 数据可视化
- [Bootstrap Icons](https://icons.getbootstrap.com/) - 图标库
- [OpenAI API](https://openai.com/) - AI模型支持
- [Odaily](https://www.odaily.news/) - 市场数据

## 📮 联系方式

- GitHub: [@Lucky-Nicky](https://github.com/Lucky-Nicky)
- 项目主页: https://github.com/Lucky-Nicky/ai_trade
- Issues: https://github.com/Lucky-Nicky/ai_trade/issues

## ⚖️ 免责声明

本项目仅用于教育和研究目的。模拟交易结果不代表真实市场表现。请勿将其用于实际交易决策。加密货币投资存在极高风险，请谨慎投资。

---

Made with ❤️ by Lucky-Nicky
