#!/usr/bin/env python3
"""
一键采集所有信息源
并行运行 GitHub Trending、HN、RSS 三个采集脚本
将结果合并输出到 /tmp/ai-daily-data.json
"""

import json
import sys
import os
import subprocess
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = "/tmp/ai-daily-data.json"


def run_script(script_name):
    """运行采集脚本，返回 (script_name, result_dict, error)"""
    script_path = os.path.join(SKILL_DIR, script_name)
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode != 0:
            return script_name, None, f"exit code {result.returncode}: {result.stderr[:200]}"

        # 解析 JSON 输出（stdout）
        data = json.loads(result.stdout)
        return script_name, data, None

    except subprocess.TimeoutExpired:
        return script_name, None, "超时（60s）"
    except json.JSONDecodeError as e:
        return script_name, None, f"JSON 解析失败: {e}"
    except Exception as e:
        return script_name, None, str(e)


def main():
    print("=== AI Coding & Agent 情报日报 - 数据采集 ===\n", file=sys.stderr)
    print(f"开始时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n", file=sys.stderr)

    scripts = [
        "fetch_github_trending.py",
        "fetch_hn.py",
        "fetch_rss.py",
    ]

    results = {}
    errors = {}

    # 并行执行三个采集脚本
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(run_script, s): s for s in scripts}
        for future in as_completed(futures):
            script_name, data, error = future.result()
            if error:
                print(f"❌ {script_name}: {error}", file=sys.stderr)
                errors[script_name] = error
            else:
                source = data.get("source", script_name)
                print(f"✅ {script_name} 完成", file=sys.stderr)
                results[source] = data

    # 汇总
    summary = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "errors": errors,
        "github_trending": results.get("github_trending", {}),
        "hacker_news": results.get("hacker_news", {}),
        "rss_and_arxiv": results.get("rss_and_arxiv", {}),
    }

    # 统计
    github_count = len(summary["github_trending"].get("repos", []))
    hn_count = len(summary["hacker_news"].get("items", []))
    rss_count = len(summary["rss_and_arxiv"].get("articles", []))
    arxiv_count = len(summary["rss_and_arxiv"].get("papers", []))

    print(f"\n📊 采集结果汇总：", file=sys.stderr)
    print(f"  GitHub Trending AI 相关项目：{github_count} 个", file=sys.stderr)
    print(f"  HN 高分 AI 相关帖子：{hn_count} 条", file=sys.stderr)
    print(f"  RSS 博客文章：{rss_count} 篇", file=sys.stderr)
    print(f"  ArXiv 论文：{arxiv_count} 篇", file=sys.stderr)

    if errors:
        print(f"\n⚠️  以下信息源采集失败（日报将跳过）：", file=sys.stderr)
        for s, e in errors.items():
            print(f"  - {s}: {e}", file=sys.stderr)

    # 写入文件
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 数据已保存到 {OUTPUT_FILE}", file=sys.stderr)
    print(f"\n下一步：AI 将读取此文件，生成日报正文并发布到学城。", file=sys.stderr)

    # 同时输出到 stdout（供 AI 直接读取）
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
