#!/usr/bin/env python3
"""
依赖检查脚本
ai-coding-daily skill 只使用 Python 标准库，无需额外安装
"""

import sys
import subprocess

def check():
    print("=== ai-coding-daily 依赖检查 ===\n")

    # Python 版本
    v = sys.version_info
    if v.major < 3 or (v.major == 3 and v.minor < 8):
        print(f"❌ Python 版本过低：{sys.version}，需要 3.8+")
        sys.exit(1)
    print(f"✅ Python {v.major}.{v.minor}.{v.micro}")

    # 标准库模块检查
    required_modules = [
        "json", "sys", "re", "time", "datetime",
        "urllib.request", "urllib.error", "xml.etree.ElementTree",
        "html.parser", "concurrent.futures"
    ]
    for mod in required_modules:
        try:
            __import__(mod)
            print(f"✅ {mod}")
        except ImportError:
            print(f"❌ {mod} 不可用（这不应该发生，请检查 Python 安装）")
            sys.exit(1)

    # 检查 oa-skills（citadel 发布用）
    print("\n--- 可选依赖 ---")
    try:
        result = subprocess.run(["oa-skills", "--version"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"✅ oa-skills（citadel 发布功能可用）")
        else:
            print(f"⚠️  oa-skills 不可用，日报将只生成到本地文件，不自动发布到学城")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print(f"⚠️  oa-skills 未安装，日报将只生成到本地文件，不自动发布到学城")
        print(f"   安装命令：npm install -g @it/oa-skills --registry=http://r.npm.sankuai.com")

    print("\n✅ 所有必要依赖就绪，可以运行日报生成脚本")
    print("\n使用方法：")
    print("  python3 ~/.catpaw/skills/ai-coding-daily/scripts/fetch_all.py")


if __name__ == "__main__":
    check()
