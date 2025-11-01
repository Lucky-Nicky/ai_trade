# 操作密码保护功能说明

## 功能介绍

为了防止应用部署到公网后被恶意操作，AITradeGame添加了操作密码保护功能。

### 受保护的操作

设置密码后，以下操作需要输入正确的密码才能执行：

- 🗑️ **删除模型** - 防止他人删除你的交易模型
- ➕ **添加模型** - 防止他人添加恶意模型
- 🗑️ **删除API提供方** - 保护你的API配置
- ➕ **添加API提供方** - 防止他人添加未授权的API
- ⚙️ **修改系统设置** - 保护系统配置参数

### 不受影响的功能

- ✅ 查看交易数据、图表、持仓等信息
- ✅ 查看AI对话记录
- ✅ 查看市场行情
- ✅ 自动交易功能正常运行
- ✅ 测试模型连接

## 使用方法

### 首次设置密码

1. 访问应用页面
2. 点击右上角的 **"设置"** 按钮
3. 滚动到底部的 **"操作密码保护"** 区域
4. 在 **"新密码"** 框中输入密码（至少4位）
5. 在 **"确认新密码"** 框中再次输入相同密码
6. 点击 **"保存设置"** 按钮

💡 **注意**: 首次设置时不需要填写"原密码"

### 修改密码

1. 进入 **"设置"** 界面
2. 在 **"原密码"** 框中输入当前密码
3. 在 **"新密码"** 和 **"确认新密码"** 中输入新密码
4. 点击 **"保存设置"**

### 使用密码保护的操作

当密码保护启用后，执行受保护操作时会自动弹出密码输入框：

1. 系统检测到操作需要验证
2. 弹出密码输入框
3. 输入操作密码
4. 点击"确认"按钮
5. 密码正确则执行操作，错误则提示重新输入

## 安全特性

### 密码存储安全

- 🔐 **哈希存储**: 密码使用SHA256哈希后存储，不保存明文
- 🔐 **后端验证**: 所有操作都在后端验证密码，前端无法绕过
- 🔐 **独立存储**: 密码存储在数据库settings表中

### 可选保护

- ⚙️ 不设置密码时，系统照常工作（适合本地开发）
- ⚙️ 设置密码后才启用保护（适合公网部署）
- ⚙️ 可随时在设置中添加或修改密码

## 技术实现

### 数据库层面 (database.py)

```python
# 密码字段
settings.operation_password  # SHA256哈希

# 核心方法
db.set_operation_password(password)      # 设置密码
db.verify_operation_password(password)   # 验证密码
db.has_operation_password()              # 检查是否设置
```

### API端点 (app.py)

```python
POST /api/password/verify    # 验证密码
POST /api/password/set       # 设置/修改密码
GET  /api/password/has       # 检查是否设置密码
```

### 受保护的API

```python
POST   /api/models                  # 添加模型（需密码）
DELETE /api/models/<id>            # 删除模型（需密码）
POST   /api/providers              # 添加API提供方（需密码）
DELETE /api/providers/<id>         # 删除API提供方（需密码）
PUT    /api/settings               # 修改设置（需密码）
```

## 常见问题

### Q: 忘记密码怎么办？

如果忘记密码，可以通过以下方式重置：

**方法1：清除数据库中的密码**

```bash
cd /root/AITradeGame/AITradeGame
sqlite3 AITradeGame.db "UPDATE settings SET operation_password = NULL;"
```

**方法2：删除数据库并重新初始化**

```bash
cd /root/AITradeGame/AITradeGame
rm AITradeGame.db
source venv/bin/activate
python init_db.py
```

⚠️ **警告**: 方法2会删除所有交易数据！

### Q: 密码必须多少位？

- 最少4位
- 建议使用8位以上的强密码
- 支持字母、数字、特殊字符

### Q: 密码安全吗？

- ✅ 使用SHA256哈希存储，不可逆
- ✅ 前后端双重验证
- ✅ 建议部署到公网时务必设置密码
- ⚠️ 密码通过HTTPS传输（生产环境建议配置SSL）

### Q: 可以禁用密码保护吗？

可以！只需清除数据库中的密码：

```bash
sqlite3 /root/AITradeGame/AITradeGame/AITradeGame.db "UPDATE settings SET operation_password = NULL;"
```

然后重启应用。

### Q: 密码会过期吗？

不会。密码永久有效，除非主动修改或清除。

## 建议

### 本地开发环境

- 💡 可以不设置密码，方便开发测试
- 💡 只有你自己能访问，风险较低

### 公网部署环境

- ⚠️ **强烈建议**设置操作密码
- ⚠️ 使用强密码（8位以上，包含大小写字母、数字）
- ⚠️ 定期更换密码
- ⚠️ 配置HTTPS加密传输
- ⚠️ 使用防火墙限制访问IP（可选）

## 更新日志

- **2025-11-02**: 添加操作密码保护功能
  - 新增密码设置和验证
  - 保护敏感操作
  - 支持密码修改
  - 添加密码输入弹窗

## 相关文件

- `/root/AITradeGame/AITradeGame/database.py` - 数据库密码管理
- `/root/AITradeGame/AITradeGame/app.py` - 后端API密码验证
- `/root/AITradeGame/AITradeGame/templates/index.html` - 密码输入界面
- `/root/AITradeGame/AITradeGame/static/app.js` - 前端密码逻辑
