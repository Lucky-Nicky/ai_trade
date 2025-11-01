# AITradeGame 快速参考

## 快速部署

```bash
cd /root/AITradeGame/AITradeGame
sudo bash deploy.sh
```

## 访问应用

- **域名**: http://ai_trade.nicky.org.cn/
- **本地**: http://localhost/
- **后端**: http://127.0.0.1:5002/ (调试)

## 常用命令

### 生产环境（Systemd服务）

| 命令 | 说明 |
|------|------|
| `systemctl status ai-trade-game.service` | 查看Flask应用状态 |
| `systemctl restart ai-trade-game.service` | 重启Flask应用 |
| `systemctl start ai-trade-game.service` | 启动Flask应用 |
| `systemctl stop ai-trade-game.service` | 停止Flask应用 |
| `journalctl -u ai-trade-game.service -f` | 查看Flask实时日志 |
| `systemctl restart nginx` | 重启Nginx |
| `nginx -t` | 测试Nginx配置 |
| `tail -f /var/log/nginx/error.log` | 查看Nginx错误日志 |

### 开发环境（直接运行）

```bash
# 停止应用
pkill -f "python.*app\.py"

# 启动应用
cd /root/AITradeGame/AITradeGame
source venv/bin/activate
nohup python app.py > app.log 2>&1 &

# 查看日志
tail -f /root/AITradeGame/AITradeGame/app.log

# 重启应用（一条命令）
pkill -f "python.*app\.py" && sleep 1 && cd /root/AITradeGame/AITradeGame && source venv/bin/activate && nohup python app.py > app.log 2>&1 &
```

### 数据库操作

```bash
# 初始化/迁移数据库（添加新字段等）
cd /root/AITradeGame/AITradeGame
source venv/bin/activate
python init_db.py
```

## 查看日志

```bash
# Flask应用日志（最新50行）
journalctl -u ai-trade-game.service -n 50

# Flask应用日志（实时）
journalctl -u ai-trade-game.service -f

# Nginx错误日志
tail -f /var/log/nginx/error.log

# Nginx访问日志
tail -f /var/log/nginx/access.log
```

## 监控资源

```bash
# 内存使用
free -h

# 磁盘使用
df -h

# 系统负载
uptime

# 进程详情
ps aux | grep "python app.py"

# 端口占用
netstat -tulpn | grep -E "(80|5002)"
```

## 检查部署状态

```bash
# 检查所有组件
echo "Flask应用:"
systemctl status ai-trade-game.service --no-pager | head -5

echo "Nginx:"
systemctl status nginx --no-pager | head -5

echo "端口:"
netstat -tulpn | grep -E "(80|5002)"

echo "测试连接:"
curl -I http://localhost/
```

## 更新代码

1. 修改 `/root/AITradeGame/AITradeGame/app.py` 或其他源文件
2. 重启应用：`systemctl restart ai-trade-game.service`
3. 查看日志确认更新：`journalctl -u ai-trade-game.service -f`

## 常见问题

### 502 Bad Gateway

```bash
# 检查Flask是否运行
ps aux | grep "python app.py"

# 检查5002端口
netstat -tulpn | grep 5002

# 查看Flask日志
journalctl -u ai-trade-game.service -n 50
```

### 无法访问应用

```bash
# 检查Nginx
systemctl status nginx

# 测试本地访问
curl http://localhost/

# 查看80端口
netstat -tulpn | grep :80
```

### 应用启动缓慢

```bash
# 查看详细日志
journalctl -u ai-trade-game.service -f

# 检查资源使用
ps aux | grep python
free -h
```

## 文件位置

- 项目: `/root/AITradeGame/AITradeGame/`
- 虚拟环境: `/root/AITradeGame/AITradeGame/venv/`
- 部署脚本: `/root/AITradeGame/AITradeGame/deploy.sh`
- 部署文档: `/root/AITradeGame/DEPLOY.md`
- Nginx配置: `/etc/nginx/sites-available/ai_trade`
- Systemd服务: `/etc/systemd/system/ai-trade-game.service`

## 完整部署指南

详见 `/root/AITradeGame/DEPLOY.md`

