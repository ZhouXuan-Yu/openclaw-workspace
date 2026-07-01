#!/usr/bin/env python3
"""OpenClaw 记忆架构可视化"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

def create_memory_architecture(output_path):
    """创建记忆架构图"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    
    # 定义层级
    layers = [
        ('L1 索引 (MEMORY.md)', '#FF6B6B', 0.9, '每次启动必读\n<200行'),
        ('L2 主题 (topics/)', '#4ECDC4', 0.7, '偏好/项目/学习\n决策/人物/工具'),
        ('L3 日志 (daily/)', '#45B7D1', 0.5, '每日对话记录\n时间线追踪'),
        ('L4 会话 (sessions/)', '#96CEB4', 0.3, '完整会话历史\n最后手段'),
    ]
    
    # 绘制层级
    y_positions = [0.8, 0.6, 0.4, 0.2]
    for i, (name, color, alpha, desc) in enumerate(layers):
        # 主层
        rect = mpatches.FancyBboxPatch((0.1, y_positions[i]-0.08), 0.8, 0.15, 
                                        boxstyle="round,pad=0.02", 
                                        facecolor=color, alpha=alpha, 
                                        edgecolor='black', linewidth=2)
        ax.add_patch(rect)
        
        # 层名
        ax.text(0.5, y_positions[i]+0.02, name, ha='center', va='center', 
                fontsize=14, fontweight='bold', color='white')
        
        # 描述
        ax.text(0.5, y_positions[i]-0.04, desc, ha='center', va='center', 
                fontsize=10, color='white', alpha=0.9)
    
    # 标题
    ax.text(0.5, 0.95, 'OpenClaw 4层记忆架构', ha='center', va='center', 
            fontsize=20, fontweight='bold', color='#2C3E50')
    
    # 副标题
    ax.text(0.5, 0.9, '从索引到会话的完整记忆体系', ha='center', va='center', 
            fontsize=14, color='#7F8C8D')
    
    # 访问箭头
    ax.annotate('', xy=(0.95, 0.8), xytext=(0.95, 0.2),
                arrowprops=dict(arrowstyle='->', color='#E74C3C', lw=3))
    ax.text(0.97, 0.5, '按需\n检索', ha='center', va='center', 
            fontsize=12, color='#E74C3C', fontweight='bold')
    
    # 写入箭头
    ax.annotate('', xy=(0.05, 0.2), xytext=(0.05, 0.8),
                arrowprops=dict(arrowstyle='->', color='#27AE60', lw=3))
    ax.text(0.03, 0.5, '写入\n整合', ha='center', va='center', 
            fontsize=12, color='#27AE60', fontweight='bold')
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.close()
    return output_path

def create_evolution_loop(output_path):
    """创建进化循环图"""
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    
    # 定义循环节点
    nodes = [
        ('观察', '#FF6B6B', 0.5, 0.9),
        ('分析', '#4ECDC4', 0.9, 0.5),
        ('提炼', '#45B7D1', 0.5, 0.1),
        ('验证', '#96CEB4', 0.1, 0.5),
    ]
    
    # 绘制节点
    for name, color, x, y in nodes:
        circle = plt.Circle((x, y), 0.08, color=color, alpha=0.8, ec='black', lw=2)
        ax.add_patch(circle)
        ax.text(x, y, name, ha='center', va='center', 
                fontsize=16, fontweight='bold', color='white')
    
    # 绘制箭头
    arrows = [
        ((0.5, 0.9), (0.9, 0.5)),  # 观察 → 分析
        ((0.9, 0.5), (0.5, 0.1)),  # 分析 → 提炼
        ((0.5, 0.1), (0.1, 0.5)),  # 提炼 → 验证
        ((0.1, 0.5), (0.5, 0.9)),  # 验证 → 观察
    ]
    
    for start, end in arrows:
        ax.annotate('', xy=end, xytext=start,
                    arrowprops=dict(arrowstyle='->', color='#2C3E50', lw=2.5))
    
    # 标题
    ax.text(0.5, 0.5, '自进化\n循环', ha='center', va='center', 
            fontsize=24, fontweight='bold', color='#2C3E50', alpha=0.3)
    
    ax.text(0.5, 1.0, 'OpenClaw 自进化循环', ha='center', va='center', 
            fontsize=20, fontweight='bold', color='#2C3E50')
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.close()
    return output_path

def create_tool_chain(output_path):
    """创建工具链图"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 6))
    
    # 定义工具
    tools = [
        ('social-auto-upload', '#FF6B6B', '多平台发布'),
        ('Wechatsync', '#4ECDC4', '文章同步'),
        ('EasyOCR', '#45B7D1', '本地识别'),
        ('SkillSpector', '#96CEB4', '安全扫描'),
        ('cover-gen.py', '#FFEAA7', '配图生成'),
        ('tracker.py', '#DDA0DD', '数据追踪'),
    ]
    
    # 绘制工具
    x_positions = np.linspace(0.1, 0.9, len(tools))
    for i, (name, color, desc) in enumerate(tools):
        rect = mpatches.FancyBboxPatch((x_positions[i]-0.08, 0.3), 0.16, 0.4, 
                                        boxstyle="round,pad=0.02", 
                                        facecolor=color, alpha=0.8, 
                                        edgecolor='black', linewidth=2)
        ax.add_patch(rect)
        ax.text(x_positions[i], 0.55, name, ha='center', va='center', 
                fontsize=10, fontweight='bold', color='white', wrap=True)
        ax.text(x_positions[i], 0.35, desc, ha='center', va='center', 
                fontsize=9, color='white', alpha=0.9)
    
    # 连接线
    for i in range(len(tools)-1):
        ax.annotate('', xy=(x_positions[i+1]-0.08, 0.5), 
                    xytext=(x_positions[i]+0.08, 0.5),
                    arrowprops=dict(arrowstyle='->', color='#2C3E50', lw=2))
    
    # 标题
    ax.text(0.5, 0.85, 'OpenClaw 工具链', ha='center', va='center', 
            fontsize=20, fontweight='bold', color='#2C3E50')
    ax.text(0.5, 0.78, '从内容生成到发布的完整自动化流程', ha='center', va='center', 
            fontsize=14, color='#7F8C8D')
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.close()
    return output_path

if __name__ == "__main__":
    output_dir = os.path.expanduser("~/.openclaw/workspace/memory/content/images")
    os.makedirs(output_dir, exist_ok=True)
    
    # 生成三张图
    create_memory_architecture(os.path.join(output_dir, "memory-architecture.png"))
    create_evolution_loop(os.path.join(output_dir, "evolution-loop.png"))
    create_tool_chain(os.path.join(output_dir, "tool-chain.png"))
    
    print("✅ 架构图生成完成！")
    print(f"📁 输出目录: {output_dir}")
