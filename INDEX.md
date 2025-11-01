# 📚 AITradeGame 部署文档索引

## 快速导航

### 🚀 想要快速开始？
→ 阅读 **QUICK_START.md** (2.7K)

### 📖 想要详细了解？
→ 阅读 **DEPLOY.md** (6.9K)

### ⚙️ 想要自动部署？
→ 运行 **deploy.sh** (4.7K)

### 📋 想要查看总结？
→ 查看 **DEPLOYMENT_SUMMARY.txt** (3.3K)

---

## 📄 文件说明

| 文件 | 大小 | 用途 | 优先级 |
|------|------|------|--------|
| **QUICK_START.md** | 2.7K | 快速参考卡，常用命令 | ⭐⭐⭐ |
| **DEPLOY.md** | 6.9K | 完整部署指南，详细步骤 | ⭐⭐⭐ |
| **deploy.sh** | 4.7K | 一键自动部署脚本 | ⭐⭐⭐ |
| **README_DEPLOY.md** | 3.0K | 文档说明和使用建议 | ⭐⭐ |
| **DEPLOYMENT_SUMMARY.txt** | 3.3K | 部署完成总结报告 | ⭐⭐ |
| **INDEX.md** | 此文件 | 文档导航索引 | ⭐ |

---

## 🎯 按使用场景选择

### 场景1：首次部署新服务器
1. 阅读 DEPLOY.md (了解流程)
2. 运行 deploy.sh (自动部署)
3. 保存 QUICK_START.md (日常使用)

### 场景2：日常维护和操作
- 使用 QUICK_START.md 查询命令
- 遇到问题时查阅 DEPLOY.md 故障排查

### 场景3：快速部署到新系统
```bash
cd /root/AITradeGame/AITradeGame
sudo bash deploy.sh
```

### 场景4：学习部署流程
1. 阅读 README_DEPLOY.md (理解架构)
2. 阅读 DEPLOY.md (学习步骤)
3. 运行 deploy.sh (实际操作)

---

## 💡 推荐阅读顺序

### 对于新手
1. README_DEPLOY.md - 了解部署文档的组织方式
2. DEPLOY.md - 学习完整的部署步骤
3. QUICK_START.md - 掌握常用命令

### 对于有经验的用户
1. QUICK_START.md - 快速查询命令
2. deploy.sh - 运行自动化脚本
3. DEPLOYMENT_SUMMARY.txt - 确认部署状态

---

## 🔑 关键信息速查

### 部署命令
```bash
sudo bash deploy.sh
```

### 访问地址
- 域名: http://ai_trade.nicky.org.cn/
- 本地: http://localhost/

### 常用命令
```bash
# 查看状态
systemctl status ai-trade-game.service

# 查看日志
journalctl -u ai-trade-game.service -f

# 重启应用
systemctl restart ai-trade-game.service
```

### 文件位置
- 项目: `/root/AITradeGame/AITradeGame/`
- Nginx配置: `/etc/nginx/sites-available/ai_trade`
- Systemd服务: `/etc/systemd/system/ai-trade-game.service`

---

## ✅ 部署检查清单

### 首次部署完成后验证
- [ ] 可访问应用: http://localhost/
- [ ] Flask运行: `systemctl status ai-trade-game.service`
- [ ] Nginx运行: `systemctl status nginx`
- [ ] 端口正确: `netstat -tulpn | grep -E "(80|5002)"`
- [ ] 日志正常: `journalctl -u ai-trade-game.service -n 20`

### 日常维护检查项
- [ ] 应用正常运行
- [ ] 内存占用合理
- [ ] 磁盘空间充足
- [ ] 无错误日志

---

## 🆘 需要帮助？

### 问题：不知道从哪里开始
→ 阅读 README_DEPLOY.md 和 DEPLOY.md 的"快速部署"部分

### 问题：忘记了某个命令
→ 查看 QUICK_START.md 的"常用命令"表

### 问题：遇到错误或故障
→ 查看 DEPLOY.md 的"故障排查"章节

### 问题：想要HTTPS
→ 查看 DEPLOY.md 的"HTTPS/SSL配置"章节

---

## 📊 部署信息速览

```
服务架构图：
┌─────────────┐
│   客户端    │
└──────┬──────┘
       │ HTTP:80
       ↓
┌─────────────┐
│   Nginx     │ (反向代理)
└──────┬──────┘
       │ 转发 :5002
       ↓
┌─────────────┐
│   Flask     │ (应用服务)
└──────┬──────┘
       │
       ↓
┌─────────────┐
│  数据库/API │
└─────────────┘
```

**部署日期**: 2025-10-30  
**部署方式**: 无Docker本地部署  
**系统**: Ubuntu/Debian  
**状态**: ✅ 已部署并正常运行

---

## 📞 快速链接

| 需求 | 查看 |
|------|------|
| 快速开始 | QUICK_START.md |
| 完整指南 | DEPLOY.md |
| 自动部署 | deploy.sh |
| 文档说明 | README_DEPLOY.md |
| 部署总结 | DEPLOYMENT_SUMMARY.txt |
| 查看本页 | INDEX.md |

---

**提示**: 建议将 QUICK_START.md 保存到浏览器书签或本地便签，以便快速查询常用命令。

