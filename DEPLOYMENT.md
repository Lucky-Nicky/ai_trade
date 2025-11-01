# AITradeGame 本地部署指南

## 部署完成信息

### 基本配置
- **域名**: ai_trade.nicky.org.cn
- **协议**: HTTP
- **Flask后端端口**: 5002
- **Nginx反向代理端口**: 80
- **项目目录**: /root/AITradeGame/AITradeGame
- **虚拟环境**: /root/AITradeGame/AITradeGame/venv

### 系统服务

#### Flask应用服务
```bash
# 查看服务状态
systemctl status ai-trade-game.service

# 启动服务
systemctl start ai-trade-game.service

# 停止服务
systemctl stop ai-trade-game.service

# 重启服务
systemctl restart ai-trade-game.service

# 查看日志
journalctl -u ai-trade-game.service -f
```

#### Nginx反向代理
```bash
# 查看状态
systemctl status nginx

# 重启
systemctl restart nginx

# 测试配置
nginx -t

# 查看配置
cat /etc/nginx/sites-available/ai_trade
```

### 访问应用
- 本地访问: http://localhost/
- 域名访问: http://ai_trade.nicky.org.cn/
- 后端直接访问: http://127.0.0.1:5002/ (用于调试)

### 重要文件位置
- **Nginx配置**: /etc/nginx/sites-available/ai_trade
- **Systemd服务**: /etc/systemd/system/ai-trade-game.service
- **应用文件**: /root/AITradeGame/AITradeGame/app.py
- **数据库**: /root/AITradeGame/AITradeGame/AITradeGame.db

### 依赖包
所有依赖已安装在虚拟环境中:
- Flask 3.0.0
- Flask-CORS 4.0.0
- requests 2.31.0
- openai >=1.0.0
- pyinstaller >=5.13.0

### SSL/HTTPS
当前使用HTTP协议。如需HTTPS:
1. 确保域名DNS已解析
2. 运行: `certbot certonly --webroot -w /var/www/html -d ai_trade.nicky.org.cn`
3. 更新Nginx配置使用SSL证书

### 服务开机自启
两个服务都已配置为开机自启:
- ai-trade-game.service
- nginx.service

### 故障排查

#### Flask服务无法启动
```bash
# 检查日志
journalctl -u ai-trade-game.service -n 100

# 手动运行应用查看错误
cd /root/AITradeGame/AITradeGame
source venv/bin/activate
python app.py
```

#### Nginx返回502错误
```bash
# 检查Flask后端是否运行
ps aux | grep "python app.py"

# 检查端口是否正确绑定
netstat -tulpn | grep 5002

# 检查Nginx日志
tail -f /var/log/nginx/error.log
```

#### 修改应用配置
编辑 `/root/AITradeGame/AITradeGame/app.py` 后需要重启服务:
```bash
systemctl restart ai-trade-game.service
```

### 监控资源使用
```bash
# 查看Flask进程资源使用
ps aux | grep "python app.py"

# 查看服务内存使用
systemctl status ai-trade-game.service

# 查看详细资源统计
free -h  # 内存
df -h    # 磁盘
uptime   # 系统负载
```

---
部署日期: 2025-10-30
部署方式: 无Docker本地部署
