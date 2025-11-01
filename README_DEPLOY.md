# 部署文档说明

本目录包含AITradeGame本地部署的完整文档和脚本。

## 📄 文件清单

### 1. **DEPLOY.md** - 完整部署指南（重要）
包含详细的部署步骤和故障排查方法：
- 快速部署脚本使用
- 手动部署步骤
- Nginx配置
- Systemd服务配置
- 常见问题解决

**第一次部署时阅读这个文件**

### 2. **QUICK_START.md** - 快速参考卡
包含常用命令和快速操作：
- 快速部署命令
- 访问地址
- 常用命令表
- 日志查看
- 资源监控
- 文件位置

**日常使用时参考这个文件**

### 3. **deploy.sh** - 自动化部署脚本
一键自动完成所有部署步骤：
```bash
sudo bash deploy.sh
```

**推荐使用这个脚本进行部署**

## 🚀 快速开始

### 首次部署

1. 阅读 `DEPLOY.md` 了解完整流程
2. 运行部署脚本：
   ```bash
   cd /root/AITradeGame/AITradeGame
   sudo bash deploy.sh
   ```
3. 访问 http://ai_trade.nicky.org.cn/

### 日常使用

参考 `QUICK_START.md`：
- 重启应用：`systemctl restart ai-trade-game.service`
- 查看日志：`journalctl -u ai-trade-game.service -f`
- 查看状态：`systemctl status ai-trade-game.service`

## 📋 部署架构

```
请求流程：
客户端 
  ↓
Nginx (端口 80)
  ↓
Flask 应用 (端口 5002)
  ↓
数据库 / API
```

## 🔧 关键配置

| 项目 | 值 |
|------|-----|
| 域名 | ai_trade.nicky.org.cn |
| 协议 | HTTP |
| Nginx端口 | 80 |
| Flask端口 | 5002 |
| 项目目录 | /root/AITradeGame/AITradeGame |
| 虚拟环境 | /root/AITradeGame/AITradeGame/venv |

## 📖 文档使用建议

### 第一次部署
1. `DEPLOY.md` → 了解完整流程
2. `deploy.sh` → 自动部署
3. `QUICK_START.md` → 保存快速命令

### 故障排查
- 查看 `DEPLOY.md` 中的"故障排查"章节
- 运行 `QUICK_START.md` 中的诊断命令

### 后续维护
- 日常使用 `QUICK_START.md` 作为参考
- 定期检查日志和资源使用
- 更新代码后记得重启应用

## ⚡ 常见操作速查

```bash
# 部署/更新
sudo bash deploy.sh

# 查看状态
systemctl status ai-trade-game.service

# 查看日志
journalctl -u ai-trade-game.service -f

# 重启应用
systemctl restart ai-trade-game.service

# 重启Nginx
systemctl restart nginx

# 监控资源
ps aux | grep python
free -h
df -h
```

## 📞 需要帮助？

1. **部署问题** → 查看 `DEPLOY.md` 的"故障排查"
2. **命令查询** → 查看 `QUICK_START.md`
3. **查看日志** → `journalctl -u ai-trade-game.service -n 100`

## ✅ 部署清单

部署完成后验证以下内容：

- [ ] Flask应用运行 (`systemctl status ai-trade-game.service`)
- [ ] Nginx运行 (`systemctl status nginx`)
- [ ] 端口正确绑定 (`netstat -tulpn | grep -E "(80|5002)"`)
- [ ] 可访问应用 (`curl http://localhost/`)
- [ ] 日志无错误 (`journalctl -u ai-trade-game.service -n 50`)

---

**部署时间**: 2025-10-30  
**部署方式**: 无Docker本地部署  
**操作系统**: Ubuntu/Debian  
**Python版本**: 3.8+

