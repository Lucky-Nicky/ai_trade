# AITradeGame 功能更新总结

## 新增功能：百分比/金额切换显示

### 更新时间
2025-10-29 20:15

### 功能描述
在原有的金额显示基础上，新增了百分比显示模式，用户可以在金额和百分比之间自由切换。

### 具体实现

#### 1. 前端界面更新
- **文件**: `templates/index.html`
- **新增元素**: 在stats section添加切换按钮
```html
<div class="stats-toggle">
    <button class="toggle-btn active" id="amountToggle" data-mode="amount">
        <i class="bi bi-currency-dollar"></i>
        金额
    </button>
    <button class="toggle-btn" id="percentToggle" data-mode="percent">
        <i class="bi bi-percent"></i>
        百分比
    </button>
</div>
```

#### 2. 样式更新
- **文件**: `static/style.css`
- **新增样式**:
  - `.stats-toggle`: 切换按钮容器
  - `.toggle-btn`: 切换按钮样式
  - 支持active状态和hover效果

#### 3. JavaScript 逻辑实现
- **文件**: `static/app.js`
- **新增功能**:
  - `currentDisplayMode`: 当前显示模式状态
  - `portfolioData`: 存储组合数据用于切换
  - `formatStatValue()`: 格式化统计值显示
  - `switchDisplayMode()`: 切换显示模式

#### 4. 后端API修复
- **文件**: `database.py`
- **修复**: `get_portfolio()` 方法现在返回 `initial_capital` 字段

- **文件**: `app.py`
- **修复**: 聚合API正确计算总初始资金

### 百分比计算逻辑

#### 账户总值百分比
```javascript
const totalPercent = ((total_value - initial_capital) / initial_capital) * 100;
// 显示: +0.09% (如果盈利) 或 -1.25% (如果亏损)
```

#### 可用现金百分比
```javascript
const cashPercent = (cash / initial_capital) * 100;
// 显示: 65.23% (现金占初始资金比例)
```

#### 盈亏百分比
```javascript
const pnlPercent = (pnl / initial_capital) * 100;
// 显示: +0.05% (盈利) 或 -0.15% (亏损)
```

### 功能特点

1. **实时切换**: 点击按钮即可在金额和百分比之间切换
2. **状态保持**: 切换后状态被保存，刷新数据时保持选择的显示模式
3. **中文习惯**: 按照中国投资者习惯，盈利显示红色(positive)，亏损显示绿色(negative)
4. **聚合支持**: 同时支持单个模型和聚合视图的百分比显示
5. **精确计算**: 基于实际初始资金计算，确保百分比准确性

### 测试验证

- ✅ 单个模型百分比显示正常
- ✅ 聚合视图百分比显示正常
- ✅ 切换按钮交互正常
- ✅ 百分比计算准确
- ✅ 实时数据更新正常

### API测试示例

```bash
# 测试单个模型
curl -s http://localhost:5002/api/models/1/portfolio

# 测试聚合数据
curl -s http://localhost:5002/api/aggregated/portfolio

# 验证 initial_capital 字段存在且正确
```

### 文件清单

主要修改的文件：
- `templates/index.html` - 添加切换按钮
- `static/style.css` - 添加按钮样式
- `static/app.js` - 实现切换逻辑
- `database.py` - 修复portfolio返回值
- `app.py` - 修复聚合API计算

### 部署说明

1. 所有代码已经更新完成
2. 数据库结构无需修改
3. 现有数据完全兼容
4. 服务器重启后生效

这个功能提升了用户体验，让交易者能够更直观地了解投资回报率，符合专业投资软件的标准。