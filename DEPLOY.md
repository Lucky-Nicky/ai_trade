# AITradeGame 本地部署指南

本指南用于在Linux服务器上本地部署AITradeGame，无需Docker。

## 前置要求

- Linux系统（Ubuntu/Debian）
- Python 3.8+
- root或sudo权限

## 快速部署（一键脚本）

### 方法1：使用自动化脚本（推荐）

```bash
cd /root/AITradeGame/AITradeGame
bash deploy.sh
```

脚本会自动完成以下步骤：
1. 创建Python虚拟环境
2. 安装依赖包
3. 安装Nginx和Certbot
4. 配置Nginx反向代理
5. 创建systemd服务
6. 启动所有服务

### 方法2：手动部署

如果脚本无法使用，按以下步骤手动部署：

#### 1. 创建虚拟环境并安装依赖

```bash
cd /root/AITradeGame/AITradeGame

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 升级pip
pip install --upgrade pip

# 安装依赖
pip install -r requirements.txt
```

#### 2. 安装Nginx和Certbot

```bash
sudo apt-get update
sudo apt-get install -y nginx certbot python3-certbot-nginx
```

#### 3. 配置Nginx

创建文件 `/etc/nginx/sites-available/ai_trade`：

```bash
sudo nano /etc/nginx/sites-available/ai_trade
```

粘贴以下内容：

```nginx
upstream flask_app {
    server 127.0.0.1:5002;
}

server {
    listen 80;
    listen [::]:80;
    server_name ai_trade.nicky.org.cn;

    client_max_body_size 20M;

    location / {
        proxy_pass http://flask_app;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_buffering off;
        proxy_request_buffering off;
    }

    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
        proxy_pass http://flask_app;
    }
}
```

启用配置：

```bash
sudo ln -sf /etc/nginx/sites-available/ai_trade /etc/nginx/sites-enabled/ai_trade
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
```

#### 4. 创建systemd服务

创建文件 `/etc/systemd/system/ai-trade-game.service`：

```bash
sudo nano /etc/systemd/system/ai-trade-game.service
```

粘贴以下内容：

```ini
[Unit]
Description=AI Trade Game Flask Application
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/AITradeGame/AITradeGame
Environment="PATH=/root/AITradeGame/AITradeGame/venv/bin"
ExecStart=/root/AITradeGame/AITradeGame/venv/bin/python app.py
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
```

#### 5. 启动服务

```bash
sudo systemctl daemon-reload
sudo systemctl enable ai-trade-game.service
sudo systemctl enable nginx
sudo systemctl restart nginx
sudo systemctl start ai-trade-game.service
```

## 验证部署

检查服务状态：

```bash
# 查看Flask应用
systemctl status ai-trade-game.service

# 查看Nginx
systemctl status nginx

# 查看端口
netstat -tulpn | grep -E "(80|5002)"

# 测试访问
curl http://localhost/
```

## 访问应用

- **域名访问**: http://ai_trade.nicky.org.cn/
- **本地访问**: http://localhost/ 或 http://127.0.0.1/
- **后端直接**: http://127.0.0.1:5002/ (调试用)

## 常见操作

### 查看实时日志

```bash
# Flask应用日志
journalctl -u ai-trade-game.service -f

# Nginx错误日志
tail -f /var/log/nginx/error.log

# Nginx访问日志
tail -f /var/log/nginx/access.log
```

### 管理服务

```bash
# 启动Flask应用
sudo systemctl start ai-trade-game.service

# 停止Flask应用
sudo systemctl stop ai-trade-game.service

# 重启Flask应用
sudo systemctl restart ai-trade-game.service

# 重启Nginx
sudo systemctl restart nginx
```

### 更新应用代码

修改app.py等文件后，只需重启Flask应用：

```bash
sudo systemctl restart ai-trade-game.service
```

### 查看资源使用

```bash
# 内存使用
free -h

# 磁盘使用
df -h

# 系统负载
uptime

# 进程资源
ps aux | grep "python app.py"
```

## HTTPS/SSL配置（可选）

如果需要HTTPS，可以配置Let's Encrypt证书：

```bash
# 申请证书（需要DNS正确解析该域名）
sudo certbot certonly --webroot -w /var/www/html -d ai_trade.nicky.org.cn

# Certbot可以自动配置Nginx
sudo certbot --nginx -d ai_trade.nicky.org.cn

# 自动续期（已默认启用）
sudo systemctl enable certbot.timer
```

## 故障排查

### Flask服务无法启动

```bash
# 查看详细日志
journalctl -u ai-trade-game.service -n 50

# 手动运行应用查看错误
cd /root/AITradeGame/AITradeGame
source venv/bin/activate
python app.py
```

### Nginx返回502错误

```bash
# 检查Flask是否运行
ps aux | grep "python app.py"

# 检查端口绑定
netstat -tulpn | grep 5002

# 检查Nginx配置
sudo nginx -t

# 查看Nginx错误日志
tail -f /var/log/nginx/error.log
```

### 无法访问应用

```bash
# 检查Nginx是否运行
systemctl status nginx

# 检查端口80是否被占用
netstat -tulpn | grep 80

# 测试本地连接
curl http://localhost/

# 查看防火墙规则
sudo ufw status
```

## 文件位置

| 文件 | 位置 |
|------|------|
| 项目目录 | `/root/AITradeGame/AITradeGame` |
| 虚拟环境 | `/root/AITradeGame/AITradeGame/venv` |
| Flask应用 | `/root/AITradeGame/AITradeGame/app.py` |
| 数据库 | `/root/AITradeGame/AITradeGame/AITradeGame.db` |
| Nginx配置 | `/etc/nginx/sites-available/ai_trade` |
| Systemd服务 | `/etc/systemd/system/ai-trade-game.service` |
| Nginx日志 | `/var/log/nginx/` |
| 系统日志 | `journalctl` |

## 性能调优

### 增加Flask工作进程（生产环境）

若使用Gunicorn替代Flask开发服务器：

```bash
pip install gunicorn

# 修改systemd服务ExecStart行为：
ExecStart=/root/AITradeGame/AITradeGame/venv/bin/gunicorn -w 4 -b 127.0.0.1:5002 app:app
```

### Nginx优化

编辑 `/etc/nginx/sites-available/ai_trade`，在server块添加：

```nginx
# 启用gzip压缩
gzip on;
gzip_min_length 1000;
gzip_types text/plain text/css application/json application/javascript;

# 连接池
keepalive_timeout 65;
```

## 卸载部署

若要移除部署：

```bash
# 停止服务
sudo systemctl stop ai-trade-game.service
sudo systemctl stop nginx

# 禁用开机自启
sudo systemctl disable ai-trade-game.service
sudo systemctl disable nginx

# 删除systemd服务
sudo rm /etc/systemd/system/ai-trade-game.service

# 删除Nginx配置
sudo rm /etc/nginx/sites-available/ai_trade
sudo rm /etc/nginx/sites-enabled/ai_trade

# 重新加载systemd
sudo systemctl daemon-reload

# 删除虚拟环境（可选）
rm -rf /root/AITradeGame/AITradeGame/venv
```

## 备注

- 部署日期：2025-10-30
- 部署方式：无Docker本地部署
- 服务器系统：Ubuntu/Debian
- Python版本：3.8+
- 域名：ai_trade.nicky.org.cn
- 协议：HTTP（可选HTTPS）

---

如有问题，查看日志获取详细错误信息。
