"""
国内大厂场景化早报 v3.1
"""

import json
import concurrent.futures
import sys
import os
import argparse
from datetime import datetime

import fetch_news as fn

# ============== Profile 配置 ==============

PROFILES = {
    # 25. 综合早报：13 个热榜 + 8 个科技信源
    "general": {
        "hot_rank": {
            "sources": [(fn.fetch_hot_rank, 20, None)],
            "enrich": False
        },
        "tech_blogs": {
            "sources": [(fn.fetch_tech_blogs, 25, None)],
            "enrich": True
        }
    },

    # 26. 科技大厂早报
    "tech": {
        "tech_blogs": {
            "sources": [
                (fn.fetch_tech_blogs, 30, None),
            ],
            "enrich": True
        },
        "ai_hot": {
            "sources": [
                (fn.HOT_RANK_SOURCES['baidu_hot'], 15, "AI,大模型,芯片,云,服务器,数据库,智能体,Agent"),
                (fn.HOT_RANK_SOURCES['weibo'], 15, "AI,大模型,DeepSeek,通义,文心,豆包,混元,盘古")
            ],
            "enrich": False
        }
    },

    # 27. 社交吃瓜早报
    "social": {
        "weibo_hot": {
            "sources": [(fn.HOT_RANK_SOURCES['weibo'], 25, None)],
            "enrich": False
        },
        "zhihu_hot": {
            "sources": [(fn.HOT_RANK_SOURCES['zhihu_hot'], 20, None)],
            "enrich": True
        },
        "video_hot": {
            "sources": [
                (fn.HOT_RANK_SOURCES['douyin_hot'], 15, None),
                (fn.HOT_RANK_SOURCES['bilibili_hot'], 15, None)
            ],
            "enrich": False
        }
    },

    # 28. AI 行业早报
    "ai_focus": {
        "ai_media": {
            "sources": [
                (fn.TECH_BLOG_SOURCES['jiqizhixin'], 20, None),
                (fn.TECH_BLOG_SOURCES['qbitai'], 20, None)
            ],
            "enrich": True
        },
        "dev_community": {
            "sources": [
                (fn.HOT_RANK_SOURCES['juejin'], 15, None),
                (fn.HOT_RANK_SOURCES['csdn'], 15, None)
            ],
            "enrich": True
        },
        "ai_hot": {
            "sources": [
                (fn.HOT_RANK_SOURCES['baidu_hot'], 15, "AI,大模型,DeepSeek,通义,文心,豆包,混元,盘古,Kimi,智谱"),
                (fn.HOT_RANK_SOURCES['weibo'], 15, "AI,大模型,DeepSeek,通义,文心,豆包")
            ],
            "enrich": False
        }
    },

    # 29. 商业资讯早报
    "business": {
        "business_media": {
            "sources": [
                (fn.HOT_RANK_SOURCES['36kr'], 20, None),
                (fn.HOT_RANK_SOURCES['huxiu'], 20, None),
                (fn.HOT_RANK_SOURCES['ithome'], 20, None),
                (fn.HOT_RANK_SOURCES['thepaper'], 20, None)
            ],
            "enrich": True
        },
        "toutiao": {
            "sources": [(fn.HOT_RANK_SOURCES['toutiao_hot'], 20, None)],
            "enrich": False
        }
    },

    # 30. 8 点精简早报（30 秒看完）
    "morning": {
        "core_hot": {
            "sources": [
                (fn.HOT_RANK_SOURCES['baidu_hot'], 10, None),
                (fn.HOT_RANK_SOURCES['weibo'], 10, None)
            ],
            "enrich": False
        }
    }
}


def fetch_section(section_name, config):
    print(f"[{section_name}] 抓取中...", file=sys.stderr)
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        future_map = {}
        for func, limit, kw in config["sources"]:
            future = executor.submit(func, limit, kw)
            future_map[future] = f"{func.__name__}"
        for future in concurrent.futures.as_completed(future_map):
            fname = future_map[future]
            try:
                items = future.result()
                results.extend(items)
                print(f"  ✓ {fname} → {len(items)} 条", file=sys.stderr)
            except Exception as e:
                print(f"  ✗ {fname} 失败: {e}", file=sys.stderr)

    if config.get("enrich") and results:
        print(f"  Deep 抓取 {len(results)} 条详情...", file=sys.stderr)
        results = fn.enrich_items_with_content(results, max_workers=5)
    return results


def save_individual_sources(data, base_dir):
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    source_map = {}
    total = 0
    for section, items in data.items():
        for item in items:
            src = item.get('source', 'Unknown')
            safe = "".join([c if c.isalnum() else "_" for c in src])
            source_map.setdefault(safe, []).append(item)
            total += 1
    for src, items in source_map.items():
        fpath = os.path.join(base_dir, f"{src}.json")
        with open(fpath, 'w', encoding='utf-8') as f:
            json.dump(items, f, indent=2, ensure_ascii=False)
    return list(source_map.keys())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--profile', default='general', choices=list(PROFILES.keys()))
    parser.add_argument('--outdir', help='自定义输出目录')
    parser.add_argument('--no-save', action='store_true')
    args = parser.parse_args()

    config = PROFILES.get(args.profile, PROFILES['general'])
    final_data = {}
    for section, sec_config in config.items():
        final_data[section] = fetch_section(section, sec_config)

    if args.outdir:
        out_dir = args.outdir
    else:
        today = datetime.now().strftime('%Y-%m-%d')
        out_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports', today)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
    print(json.dumps(final_data, indent=2, ensure_ascii=False))

    if not args.no_save:
        unified = os.path.join(out_dir, f"{args.profile}_briefing_unified.json")
        with open(unified, 'w', encoding='utf-8') as f:
            json.dump(final_data, f, indent=2, ensure_ascii=False)
        sources_saved = save_individual_sources(final_data, out_dir)
        print(f"\n已保存: {unified} + {len(sources_saved)} 个独立文件 → {out_dir}", file=sys.stderr)
    else:
        print("\n(--no-save 模式，仅输出到 stdout)", file=sys.stderr)


if __name__ == "__main__":
    main()
