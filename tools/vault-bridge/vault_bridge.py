#!/usr/bin/env python3
"""
vault-bridge.py — Obsidian vault → book-to-skill → OpenClaw Skill 桥接层

职责:
  1. 从 vault 发现源文件 (书籍/PDF/EPUB 或 主题目录)
  2. 调用 book-to-skill 提取文本
  3. 生成分析报告 + 技能骨架目录
  4. 记录到 vault 索引笔记

用法:
  python vault-bridge.py extract <path> [--slug <slug>] [--mode text|technical]
  python vault-bridge.py list                              # 列出 vault 内可转换的源
  python vault-bridge.py status [--slug <slug>]            # 查看已生成技能的状态
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ── 路径常量 ──────────────────────────────────────────────────────────────────

_ws = os.environ.get("OPENCLAW_WORKSPACE", "")
WORKSPACE = Path(_ws).resolve() if _ws else Path(__file__).resolve().parent.parent.parent
VAULT = Path(r"E:\Obsidian仓库\ZhouXuan私人领域")
SKILLS_HOME = WORKSPACE.resolve() / "skills"
BRIDGE_DIR = Path(__file__).resolve().parent
INDEX_FILE = BRIDGE_DIR / "skill-index.json"

# 可生成技能的主题目录（默认候选）
TOPIC_CANDIDATES = [
    ("顶级UI设计", "UI 设计原则与组件模式"),
    ("Agent学习", "Agent 架构与技能模式"),
    ("开发项目", "项目知识库与架构决策"),
    ("prompt学习提示词", "Prompt 工程模式库"),
    ("计算机视觉", "CV 算法与最佳实践"),
    ("学习笔记", "综合学习知识"),
    ("自动化内容", "内容生产自动化"),
]

# 书籍优先搜索目录
BOOK_DIRS = ["学习项目", "开发项目", "每日更新", "自动化内容"]

SUPPORTED_EXTS = {
    ".pdf", ".epub", ".docx", ".txt", ".text",
    ".md", ".markdown", ".rst", ".adoc", ".asciidoc",
    ".html", ".htm", ".rtf", ".mobi", ".azw", ".azw3",
}


# ── 核心函数 ──────────────────────────────────────────────────────────────────


def slugify(name: str) -> str:
    """生成技能 slug: 小写 + 连字符"""
    name = name.lower().strip()
    name = re.sub(r"[^\w\s-]", "", name)
    name = re.sub(r"[\s_]+", "-", name)
    return name.strip("-")


def find_sources() -> list[dict[str, Any]]:
    """扫描 vault 发现所有可转换源：书籍 + 主题目录"""
    sources: list[dict[str, Any]] = []

    # --- 书籍扫描 ---
    for dirname in BOOK_DIRS:
        d = VAULT / dirname
        if not d.exists():
            continue
        for f in sorted(d.rglob("*")):
            if f.suffix.lower() in {".pdf", ".epub", ".docx"}:
                sources.append({
                    "type": "book",
                    "path": str(f.resolve()),
                    "name": f.stem,
                    "category": dirname,
                    "ext": f.suffix.lower(),
                    "size_mb": round(f.stat().st_size / (1024 * 1024), 2),
                })

    # --- 主题目录扫描 ---
    for dirname, desc in TOPIC_CANDIDATES:
        d = VAULT / dirname
        if not d.exists():
            continue
        md_files = list(d.rglob("*.md"))
        if md_files:
            total_size = sum(f.stat().st_size for f in md_files)
            sources.append({
                "type": "topic",
                "path": str(d.resolve()),
                "name": dirname,
                "description": desc,
                "file_count": len(md_files),
                "size_mb": round(total_size / (1024 * 1024), 2),
            })

    return sources


def extract(source_path: str, slug: str, mode: str = "text") -> dict[str, Any]:
    """调用 book-to-skill 提取文本，返回分析结果"""
    from book_to_skill.config import (
        OUTPUT_DIR, OUTPUT_TEXT, OUTPUT_META,
    )
    from book_to_skill.utils import (
        parse_arguments, resolve_input_files, extract_single_file,
        estimate_tokens, detect_structure,
    )

    # 重置输出目录
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR, ignore_errors=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 准备参数
    paths, extraction_mode, install_mode = parse_arguments(
        ["vault-bridge", source_path, "--mode", mode]
    )
    input_files = resolve_input_files(paths)

    if not input_files:
        raise RuntimeError(f"未找到支持的源文件: {source_path}")

    # 提取
    extracted_sources: list[dict] = []
    combined_texts: list[str] = []
    errors: list[tuple[Path, str]] = []

    for file_path in input_files:
        try:
            res = extract_single_file(file_path, extraction_mode, install_mode)
        except Exception as e:
            errors.append((file_path, str(e)))
            continue

        extracted_sources.append(res)
        separator = (
            f"\n\n{'=' * 80}\n"
            f"SOURCE: {res['filename']} (Path: {res['source_file']})\n"
            f"{'=' * 80}\n\n"
        )
        combined_texts.append(separator + res["text"])

    if not extracted_sources:
        raise RuntimeError(
            f"所有源文件提取失败 ({len(errors)} 个错误)"
        )

    consolidated_text = "".join(combined_texts).strip()
    OUTPUT_TEXT.write_text(consolidated_text, encoding="utf-8")

    # 聚合元数据
    total_mb = sum(s["file_size_mb"] for s in extracted_sources)
    total_pages = sum(s["pages"] for s in extracted_sources)
    total_words = len(consolidated_text.split())
    total_tokens = estimate_tokens(consolidated_text)
    structure = detect_structure(consolidated_text)

    metadata = {
        "slug": slug,
        "source_path": source_path,
        "extraction_mode": mode,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_sources": len(extracted_sources),
        "file_size_mb": round(total_mb, 2),
        "pages": total_pages,
        "words": total_words,
        "estimated_tokens": total_tokens,
        "estimated_tokens_human": f"~{total_tokens // 1000}K",
        "chapters_detected": structure["chapters_detected"],
        "has_toc": structure["has_toc"],
        "sources": [{
            "filename": s["filename"],
            "format": s["format"],
            "pages": s["pages"],
            "words": s["words"],
            "estimated_tokens": s["estimated_tokens"],
            "chapters_detected": s.get("chapters_detected", 0),
        } for s in extracted_sources],
        "errors": [str(e) for _, e in errors],
        "output_text": str(OUTPUT_TEXT),
        "output_meta": str(OUTPUT_META),
    }

    OUTPUT_META.write_text(json.dumps(metadata, indent=2, ensure_ascii=False))

    return metadata


def create_skill_skeleton(slug: str, metadata: dict[str, Any]) -> Path:
    """在 skills/ 下创建技能骨架目录 + analysis.json"""
    skill_dir = SKILLS_HOME / slug
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "chapters").mkdir(exist_ok=True)

    # 写入分析报告（供 Agent 生成 skill 时使用）
    analysis = {
        "slug": slug,
        "title": metadata.get("slug", slug),
        "source_path": metadata.get("source_path", ""),
        "sources": metadata.get("sources", []),
        "total_tokens": metadata.get("estimated_tokens", 0),
        "chapters_count": metadata.get("chapters_detected", 0),
        "words": metadata.get("words", 0),
        "extraction_mode": metadata.get("extraction_mode", "text"),
        "generated_at": metadata.get("generated_at", ""),
        "full_text_path": metadata.get("output_text", ""),
    }
    analysis_path = skill_dir / "_analysis.json"
    analysis_path.write_text(
        json.dumps(analysis, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # 写入 vault 索引笔记
    write_vault_index(slug, metadata)

    return skill_dir


def write_vault_index(slug: str, metadata: dict[str, Any]) -> None:
    """在 vault 内写入 Skill 索引笔记"""
    vault_skills_dir = VAULT / "_skills"
    vault_skills_dir.mkdir(exist_ok=True)
    note_path = vault_skills_dir / f"{slug}.md"

    lines = [
        f"---",
        f"skill: {slug}",
        f"generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"tokens: {metadata.get('estimated_tokens', 0)}",
        f"chapters: {metadata.get('chapters_detected', 0)}",
        f"type: {'topic' if Path(metadata.get('source_path', '')).is_dir() else 'book'}",
        f"---",
        f"",
        f"# Skill: `{slug}`",
        f"",
        f"📦 **状态**: 🟡 待生成 (extracted, 等待 Agent 生成技能文件)",
        f"",
    ]

    # 源文件信息
    source_path = metadata.get("source_path", "")
    p = Path(source_path)
    lines.append("## 源文件")
    if p.is_dir():
        lines.append(f"- 📁 目录: `{source_path}`")
        for s in metadata.get("sources", []):
            lines.append(f"  - `{s['filename']}` ({s['format']})")
    else:
        lines.append(f"- 📄 文件: `{source_path}`")
    lines.append("")

    # 统计信息
    lines.extend([
        "## 统计",
        f"| 项 | 值 |",
        f"|----|-----|",
        f"| 字数 | {metadata.get('words', 0):,} |",
        f"| Token 估算 | {metadata.get('estimated_tokens_human', '?')} |",
        f"| 章节 (检测) | {metadata.get('chapters_detected', 0)} |",
        f"| 源文件数 | {metadata.get('total_sources', 0)} |",
        f"| 提取模式 | {metadata.get('extraction_mode', 'text')} |",
        f"",
    ])

    # 使用指引
    lines.extend([
        "## 使用",
        "",
        "```",
        f"ask {slug}                              # 加载核心框架",
        f"ask {slug} about <topic>                # 查找并解释主题",
        f"ask {slug} for ch01                     # 深入特定章节",
        f"ask {slug} what chapters do you have?   # 浏览所有章节",
        "```",
        "",
    ])

    note_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  📝 索引笔记: {note_path}")


def list_sources() -> None:
    """打印 vault 内所有可转换源"""
    sources = find_sources()

    print(f"\n📚 书籍 ({sum(1 for s in sources if s['type'] == 'book')})")
    for s in sources:
        if s["type"] == "book":
            slug = slugify(s["name"])
            print(f"  [{slug:30s}] {s['name']:30s}  ({s['size_mb']:.1f}MB, {s['ext']})")

    print(f"\n📁 主题目录 ({sum(1 for s in sources if s['type'] == 'topic')})")
    for s in sources:
        if s["type"] == "topic":
            slug = slugify(s["name"])
            status = "✅" if (SKILLS_HOME / slug / "_analysis.json").exists() else "🟡"
            print(f"  [{slug:30s}] {s['name']:20s}  {s['file_count']} files, {s['size_mb']:.1f}MB  {status}")


def show_status(slug: str | None = None) -> None:
    """显示已生成技能的状态"""
    if slug:
        targets = [SKILLS_HOME / slug]
    else:
        targets = sorted(SKILLS_HOME.iterdir()) if SKILLS_HOME.exists() else []

    found = False
    for d in targets:
        if not d.is_dir() or d.name.startswith("."):
            continue
        analysis_file = d / "_analysis.json"
        skill_md = d / "SKILL.md"
        if not analysis_file.exists():
            continue
        found = True
        analysis = json.loads(analysis_file.read_text(encoding="utf-8"))
        has_skill = skill_md.exists()
        status = "✅" if has_skill else "🟡"
        print(f"\n{status} [{d.name}]")
        print(f"   源:       {analysis.get('source_path', '?')}")
        print(f"   字数:     {analysis.get('words', 0):,}")
        print(f"   Tokens:   {analysis.get('total_tokens', 0):,}")
        print(f"   章节:     {analysis.get('chapters_count', 0)}")
        print(f"   提取于:   {analysis.get('generated_at', '?')[:10]}")
        if has_skill:
            print(f"   Skill 文件: {skill_md}")
        else:
            print(f"   ⚠️  待 Agent 生成技能文件")

    if not found:
        print("  暂无已分析的技能")


# ── CLI ───────────────────────────────────────────────────────────────────────


def main() -> None:
    parser = argparse.ArgumentParser(
        description="vault-bridge: Obsidian vault → OpenClaw Skill 桥接",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # extract
    ext = sub.add_parser("extract", help="提取 vault 内容生成技能骨架")
    ext.add_argument("source", nargs="?", help="源文件/目录路径")
    ext.add_argument("--slug", help="技能 slug (默认自动生成)")
    ext.add_argument("--mode", choices=["text", "technical"], default="text",
                     help="提取模式: text=纯文本, technical=保留表格/代码")
    ext.add_argument("--vault", help="从 vault 自动发现: book|topic|all")

    # list
    sub.add_parser("list", help="列出 vault 可转换源")

    # status
    st = sub.add_parser("status", help="查看已提取技能状态")
    st.add_argument("--slug", help="技能 slug (留空列出全部)")

    args = parser.parse_args()

    if args.command == "list":
        list_sources()
        return

    if args.command == "status":
        show_status(args.slug)
        return

    if args.command == "extract":
        if args.vault:
            # 从 vault 自动发现
            sources = find_sources()
            candidates = []
            if args.vault == "book":
                candidates = [s for s in sources if s["type"] == "book"]
            elif args.vault == "topic":
                candidates = [s for s in sources if s["type"] == "topic"]
            else:
                candidates = sources

            if not candidates:
                print("未找到匹配的源")
                return

            print(f"发现 {len(candidates)} 个候选源:\n")
            for i, s in enumerate(candidates, 1):
                slug = slugify(s["name"])
                status = "✅" if (SKILLS_HOME / slug / "SKILL.md").exists() else "🟡"
                print(f"  {i}. [{slug}] {s['name']}  ({s['size_mb']}MB)  {status}")
            print()
            return

        if not args.source:
            print("错误: 需要指定源路径或 --vault 参数")
            sys.exit(1)

        slug = args.slug or slugify(Path(args.source).stem)
        print(f"\n🔧 提取: {args.source}")
        print(f"  Slug: {slug}")
        print(f"  模式: {args.mode}")

        try:
            metadata = extract(args.source, slug, args.mode)
        except Exception as e:
            print(f"\n❌ 提取失败: {e}")
            sys.exit(1)

        skill_dir = create_skill_skeleton(slug, metadata)

        print(f"\n✅ 提取完成")
        print(f"  Token 估算: {metadata['estimated_tokens_human']}")
        print(f"  章节检测:   {metadata['chapters_detected']}")
        print(f"  技能骨架:   {skill_dir}")
        print(f"  分析报告:   {skill_dir / '_analysis.json'}")
        print(f"\n➡  下一步: 告诉我「生成 Skill: {slug}」, 我来完成技能文件")

        # 更新索引
        update_skill_index(slug, metadata)


def update_skill_index(slug: str, metadata: dict[str, Any]) -> None:
    """更新技能索引文件"""
    index: dict[str, Any] = {"skills": []}
    if INDEX_FILE.exists():
        try:
            index = json.loads(INDEX_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass

    entry = {
        "slug": slug,
        "source": metadata.get("source_path", ""),
        "generated_at": metadata.get("generated_at", ""),
        "tokens": metadata.get("estimated_tokens", 0),
        "chapters": metadata.get("chapters_detected", 0),
        "status": "extracted",
        "vault_note": str(VAULT / "_skills" / f"{slug}.md"),
    }

    # 更新或追加
    existing = [i for i in index["skills"] if i["slug"] == slug]
    if existing:
        existing[0].update(entry)
    else:
        index["skills"].append(entry)

    INDEX_FILE.write_text(
        json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
