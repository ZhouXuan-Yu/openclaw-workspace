---
name: "test-and-validate"
description: "AI能力边界测试+生产级验收：自动测试所有工具/Skill/集成，生成验收报告，自举优化"
---

# 测试验收 Skill — test-and-validate

## 触发条件
- 用户说"测试验收"、"跑测试"、"验收报告"、"检查系统状态"
- 用户说"测试XXX"（某个具体组件）
- 定期自动触发（cron）

## 核心职责

### 1. 系统健康检查

```yaml
health_check:
  - name: "基础环境"
    checks:
      - cmd: "node --version"
        expect: "v*"
      - cmd: "python --version"  
        expect: "Python 3.*"
      - cmd: "uv --version"
        expect: "uv *"
  
  - name: "social-auto-upload"
    checks:
      - cmd: "sau --help"
        expect: "usage: sau"
      - cmd: "python tests/test_verify.py"
        expect: "全部通过"
  
  - name: "Wechatsync"
    checks:
      - cmd: "wechatsync --help"
        expect: "Usage: wechatsync"
  
  - name: "截图工具"
    checks:
      - cmd: "powershell -ExecutionPolicy Bypass -File tools/screenshot.ps1"
        expect: "screenshot_*.png"
```

### 2. SkillSpector 安全扫描

集成 NVIDIA SkillSpector 对所有 Skill 进行安全扫描：

```yaml
security_scan:
  tool: "skillspector"
  location: "tools/SkillSpector/.venv/Scripts/skillspector"
  
  scan_targets:
    - "skills/"  # 扫描所有 workspace skills
    - "tools/*/skills/"  # 扫描工具附带的 skills
  
  severity_thresholds:
    CRITICAL: "立即报告，阻断使用"
    HIGH: "标记警告，建议修复"
    MEDIUM: "记录，可接受"
    LOW: "忽略"
  
  false_positive_rules:
    - pattern: "RA1 (Self-Modification)"
      exception: "evolution-engine, self-improving-agent 的设计目的"
    - pattern: "RA2 (Session Persistence)"
      exception: "memory/ 相关操作是正常功能"
    - pattern: "P3 (Exfiltration Commands)"
      exception: "OpenClaw sessions_send 是正常跨会话通信"
  
  output: "memory/evolution/security-scan-report.json"
```

### 3. 平台登录状态检查

```yaml
platform_check:
  - platform: xiaohongshu
    cmd: "sau xiaohongshu check --account creator"
    expect: "valid"
  - platform: kuaishou
    cmd: "sau kuaishou check --account creator"
    expect: "valid"
  - platform: douyin
    cmd: "sau douyin check --account creator"
    expect: "valid"
  - platform: bilibili
    cmd: "sau bilibili check --account creator"
    expect: "valid"
```

### 4. 端到端集成测试

```yaml
integration_test:
  - name: "内容生成→发布链路"
    steps:
      1. 调用 multi-platform-content 生成测试内容
      2. 验证内容文件完整性
      3. dry-run 发布到已登录平台
      4. 检查发布报告格式
    
  - name: "截图→发送链路"
    steps:
      1. 运行 screenshot.ps1
      2. 验证文件存在且大小 > 0
      3. 通过 MEDIA: 指令发送
    
  - name: "进化引擎链路"
    steps:
      1. 读取 run-log.json
      2. 验证 JSON 完整性
      3. 检查 test-history.json 趋势
```

### 5. 性能基准测试

```yaml
benchmark:
  - name: "内容生成速度"
    metric: "从主题到6平台内容的耗时"
    baseline: 180
    target: 120
    
  - name: "Token消耗"
    metric: "单次内容生成的token数"
    baseline: 6500
    target: 4000
    
  - name: "CLI响应时间"
    metric: "sau --help 的响应时间"
    baseline: 5
    target: 2
```

---

## 输出格式

### 验收报告

```
📋 验收报告 — YYYY-MM-DD HH:MM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🟢 基础环境 (N/N)
  ✅/❌ 检查项

🔒 安全扫描 (SkillSpector)
  ✅ skill-name: 0/100 (SAFE)
  ⚠️ skill-name: 50/100 (CAUTION) — 2 issues
  🔴 skill-name: 100/100 (CRITICAL) — 6 issues

🟡 平台登录 (N/N)
  ✅/⏳ 平台名

🟢 工具链 (N/N)
  ✅/❌ 工具名

🟡 端到端测试 (N/N)
  ✅/⚠️ 测试名

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
总分: N/M (XX%)
状态: 🟢/🟡/🔴 描述
```

### 问题清单

按严重程度分类列出所有发现的问题。

---

## 自举机制

### 测试历史

存储在 `memory/evolution/test-history.json`：
- 每次测试的分数趋势
- 问题修复率
- 回归检测（之前通过的测试突然失败）
- 安全扫描结果历史

### 自动优化规则

| 条件 | 动作 |
|------|------|
| 同一检查连续3次失败 | 标记为已知问题，跳过等待修复 |
| 测试耗时增加 > 50% | 分析瓶颈，优化测试顺序 |
| 新增工具/Skill | 自动加入测试套件 |
| 安全扫描发现 CRITICAL | 立即通知用户，阻断使用 |
| 修复后测试通过 | 更新基线数据 |
| 分数 > 90% | 触发更严格的性能基准测试 |

### 进度提醒

长任务（>30秒）自动发送进度：

```
⏳ [1/5] 正在检查基础环境...
⏳ [2/5] 正在安全扫描...
⏳ [3/5] 正在检查平台登录...
⏳ [4/5] 正在运行端到端测试...
✅ [5/5] 验收完成！总分: N/M
```

---

## 依赖

- exec（执行CLI命令）
- read/write（文件检查和报告生成）
- cron（定时触发）
- SkillSpector（安全扫描）
- memory/evolution/（性能数据存储）
