#!/bin/bash

#############################################
# AITradeGame 自动部署脚本
# 用于Linux系统的本地部署
# 使用: bash deploy.sh
#############################################

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查权限
if [[ $EUID -ne 0 ]]; then
   log_error "此脚本必须以root身份运行"
   exit 1
fi

# 获取项目目录
PROJECT_DIR="/root/AITradeGame/AITradeGame"
DOMAIN="ai_trade.nicky.org.cn"
FLASK_PORT="5002"

log_info "=========================================="
log_info "AITradeGame 本地部署脚本"
log_info "=========================================="

# 第1步：创建虚拟环境
log_info "第1步：创建Python虚拟环境..."
cd "$PROJECT_DIR"

if [ ! -d "venv" ]; then
    python3 -m venv venv
    log_success "虚拟环境创建完成"
else
    log_warn "虚拟环境已存在，跳过创建"
fi

# 第2步：安装依赖
log_info "第2步：安装Python依赖..."
source venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt -q
log_success "依赖安装完成"

# 第3步：安装系统软件包
log_info "第3步：安装系统软件包（Nginx, Certbot）..."
apt-get update -qq
apt-get install -y -qq nginx certbot python3-certbot-nginx >/dev/null 2>&1
log_success "系统软件包安装完成"

# 第4步：配置Nginx
log_info "第4步：配置Nginx反向代理..."
cat > /etc/nginx/sites-available/ai_trade << EOF
upstream flask_app {
    server 127.0.0.1:${FLASK_PORT};
}

server {
    listen 80;
    listen [::]:80;
    server_name ${DOMAIN};

    client_max_body_size 20M;

    location / {
        proxy_pass http://flask_app;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_buffering off;
        proxy_request_buffering off;
    }

    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
        proxy_pass http://flask_app;
    }
}
EOF

ln -sf /etc/nginx/sites-available/ai_trade /etc/nginx/sites-enabled/ai_trade
rm -f /etc/nginx/sites-enabled/default

# 测试Nginx配置
if nginx -t 2>&1 | grep -q "successful"; then
    log_success "Nginx配置验证通过"
else
    log_error "Nginx配置验证失败"
    exit 1
fi

# 第5步：创建systemd服务
log_info "第5步：创建systemd服务..."
cat > /etc/systemd/system/ai-trade-game.service << EOF
[Unit]
Description=AI Trade Game Flask Application
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=${PROJECT_DIR}
Environment="PATH=${PROJECT_DIR}/venv/bin"
ExecStart=${PROJECT_DIR}/venv/bin/python app.py
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
EOF

log_success "systemd服务创建完成"

# 第6步：启动服务
log_info "第6步：启动服务..."

systemctl daemon-reload
systemctl enable ai-trade-game.service >/dev/null 2>&1
systemctl enable nginx >/dev/null 2>&1

systemctl restart nginx
sleep 2

systemctl stop ai-trade-game.service 2>/dev/null || true
sleep 1
systemctl start ai-trade-game.service

sleep 3

# 验证服务状态
if systemctl is-active --quiet ai-trade-game.service; then
    log_success "Flask应用服务启动成功"
else
    log_error "Flask应用服务启动失败"
    log_info "查看日志: journalctl -u ai-trade-game.service -n 50"
    exit 1
fi

if systemctl is-active --quiet nginx; then
    log_success "Nginx服务启动成功"
else
    log_error "Nginx服务启动失败"
    exit 1
fi

# 第7步：显示部署结果
log_info "=========================================="
log_success "部署完成！"
log_info "=========================================="
echo ""
echo "访问地址:"
echo "  - 域名: http://${DOMAIN}/"
echo "  - 本地: http://localhost/"
echo "  - 后端: http://127.0.0.1:${FLASK_PORT}/"
echo ""
echo "常用命令:"
echo "  - 查看状态: systemctl status ai-trade-game.service"
echo "  - 查看日志: journalctl -u ai-trade-game.service -f"
echo "  - 重启应用: systemctl restart ai-trade-game.service"
echo "  - 重启Nginx: systemctl restart nginx"
echo ""
echo "详细文档: $PROJECT_DIR/../DEPLOY.md"
echo ""
