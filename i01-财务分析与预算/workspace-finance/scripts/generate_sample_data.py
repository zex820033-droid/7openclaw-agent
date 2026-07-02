#!/usr/bin/env python3
"""
蓝鲸科技有限公司 — 仿真财务数据生成器
生成 2025-01 至 2026-05 共 17 个月的完整财务数据
包括：收入、成本、费用、资产、负债、现金流、预算、应收应付
"""

import json
import random
import os
from datetime import datetime, timedelta
from collections import OrderedDict

random.seed(42)

# ============================================================
# 公司配置
# ============================================================
COMPANY = "蓝鲸科技有限公司"
INDUSTRY = "SaaS + 跨境电商"
CURRENCY = "CNY"

DEPARTMENTS = ["销售部", "研发部", "运营部", "采购部", "行政部", "市场部"]
PRODUCTS = ["SaaS平台", "电商平台", "咨询服务"]
COST_CATEGORIES = ["人力成本", "服务器/云服务", "营销推广", "物流仓储", "办公租金", "差旅招待", "软件许可", "外包服务", "其他"]

# 月度基线 (2025-01)
BASE_MONTHLY_REVENUE = 3_200_000  # 320万/月
BASE_MONTHLY_COST = 2_100_000
BASE_MONTHLY_OPEX = 800_000

# 月度增长率 (小幅波动 + 趋势)
MONTHLY_GROWTH_TREND = 0.012  # 月均1.2%增长趋势

# 资产基线
BASE_CASH = 8_500_000
BASE_AR = 4_200_000
BASE_INVENTORY = 1_800_000
BASE_PP_E = 12_000_000
BASE_AP = 2_800_000
BASE_DEBT = 5_000_000
BASE_EQUITY = 18_700_000

# 部门成本占比
DEPT_COST_RATIO = {
    "研发部": 0.35,
    "销售部": 0.22,
    "运营部": 0.18,
    "采购部": 0.10,
    "市场部": 0.10,
    "行政部": 0.05,
}

# ============================================================
# 辅助函数
# ============================================================
def seasonal_adjust(month):
    """季节性调整系数"""
    # Q1: 淡季, Q2: 增长, Q3: 平稳, Q4: 旺季
    seasonal = {
        1: 0.88, 2: 0.82, 3: 0.95,
        4: 1.02, 5: 1.05, 6: 1.10,
        7: 1.05, 8: 1.02, 9: 1.00,
        10: 1.08, 11: 1.15, 12: 1.22,
    }
    return seasonal.get(month, 1.0)

def noise(pct=0.03):
    """随机噪声"""
    return 1.0 + random.uniform(-pct, pct)

def trend_growth(month_index):
    """趋势增长因子"""
    return (1 + MONTHLY_GROWTH_TREND) ** month_index

# ============================================================
# 生成月度数据
# ============================================================
months = []
start_date = datetime(2025, 1, 1)

for i in range(17):  # 2025-01 to 2026-05
    dt = start_date + timedelta(days=32 * i)
    dt = dt.replace(day=1)
    month_key = dt.strftime("%Y-%m")
    m = dt.month
    trend = trend_growth(i)
    season = seasonal_adjust(m)
    
    # === 收入 ===
    total_revenue = round(BASE_MONTHLY_REVENUE * trend * season * noise(0.04))
    product_revenue = round(total_revenue * 0.55 * noise(0.03))  # SaaS平台 55%
    ecom_revenue = round(total_revenue * 0.30 * noise(0.03))     # 电商平台 30%
    consulting_revenue = total_revenue - product_revenue - ecom_revenue  # 咨询 15%
    
    # === 成本 ===
    total_cogs = round(BASE_MONTHLY_COST * trend * season * noise(0.03))
    # 成本按品类拆分
    cogs_product = round(total_cogs * 0.45)
    cogs_ecom = round(total_cogs * 0.35)
    cogs_consulting = total_cogs - cogs_product - cogs_ecom
    
    gross_profit = total_revenue - total_cogs
    gross_margin = round(gross_profit / total_revenue * 100, 2) if total_revenue else 0
    
    # === 运营费用（按科目） ===
    salary_expense = round(BASE_MONTHLY_OPEX * 0.40 * trend * noise(0.02))   # 人力 40%
    marketing_expense = round(BASE_MONTHLY_OPEX * 0.22 * season * noise(0.06))  # 营销 22%
    rnd_expense = round(BASE_MONTHLY_OPEX * 0.15 * trend * noise(0.03))       # 研发 15%
    admin_expense = round(BASE_MONTHLY_OPEX * 0.12 * noise(0.02))             # 行政 12%
    logistics_expense = round(BASE_MONTHLY_OPEX * 0.08 * season * noise(0.04)) # 物流 8%
    other_expense = round(BASE_MONTHLY_OPEX * 0.03 * noise(0.10))             # 其他 3%
    
    total_opex = salary_expense + marketing_expense + rnd_expense + admin_expense + logistics_expense + other_expense
    
    # 折旧摊销
    depreciation = round(BASE_PP_E * 0.02 / 12 * trend)  # 2%年折旧率
    
    # 利息支出
    interest_expense = round(BASE_DEBT * 0.05 / 12)  # 5%年利率
    
    # === 利润 ===
    operating_profit = gross_profit - total_opex - depreciation
    profit_before_tax = operating_profit - interest_expense
    income_tax = round(max(0, profit_before_tax * 0.25))  # 25%所得税
    net_profit = profit_before_tax - income_tax
    
    # === 资产负债表 ===
    # 资产
    cash = round(BASE_CASH + net_profit * (i + 1) * 0.3 * noise(0.10))
    ar = round(BASE_AR * trend * season * noise(0.05))  # 应收账款
    inventory = round(BASE_INVENTORY * trend * season * noise(0.04))
    prepaid = round(total_opex * 0.15 * noise(0.08))  # 预付费用
    total_current_assets = cash + ar + inventory + prepaid
    
    pp_e = round(BASE_PP_E * (1 - 0.02 * (i / 12)) + rnd_expense * 0.1)  # 固定资产+新增
    intangible = round(2_500_000 + rnd_expense * 0.05 * (i / 12))  # 无形资产
    total_non_current_assets = pp_e + intangible
    total_assets = total_current_assets + total_non_current_assets
    
    # 负债
    ap = round(BASE_AP * trend * season * noise(0.04))  # 应付账款
    accrued_expenses = round(total_opex * 0.12 * noise(0.05))  # 应计费用
    tax_payable = income_tax if dt.month in [3, 6, 9, 12] else round(income_tax * 0.3)
    short_term_debt = round(BASE_DEBT * 0.3 * noise(0.05))
    total_current_liabilities = ap + accrued_expenses + tax_payable + short_term_debt
    
    long_term_debt = round(BASE_DEBT * 0.7)
    total_liabilities = total_current_liabilities + long_term_debt
    
    # 权益
    equity = total_assets - total_liabilities
    retained_earnings = equity - BASE_EQUITY
    
    # === 现金流量表 ===
    operating_cf = round(net_profit + depreciation - (ar - BASE_AR) * 0.1 + (ap - BASE_AP) * 0.1)
    investing_cf = round(-rnd_expense * 0.05 - depreciation * 0.3)  # 投资现金流（资本支出）
    financing_cf = round(-interest_expense + (short_term_debt - BASE_DEBT * 0.3) * 0.1)  # 融资现金流
    net_cf = operating_cf + investing_cf + financing_cf
    
    # === 成本按部门拆分 ===
    dept_costs = {}
    for dept, ratio in DEPT_COST_RATIO.items():
        dept_costs[dept] = round((total_cogs + total_opex) * ratio * noise(0.05))
    
    # === 成本按品类拆分 ===
    category_costs = {}
    cat_ratios = {
        "人力成本": 0.38, "服务器/云服务": 0.18, "营销推广": 0.16,
        "物流仓储": 0.08, "办公租金": 0.06, "差旅招待": 0.04,
        "软件许可": 0.05, "外包服务": 0.03, "其他": 0.02,
    }
    for cat, ratio in cat_ratios.items():
        base = (total_cogs + total_opex) * ratio
        category_costs[cat] = round(base * noise(0.06))
    
    # === 关键指标 ===
    key_metrics = {
        "毛利率": gross_margin,
        "净利率": round(net_profit / total_revenue * 100, 2) if total_revenue else 0,
        "营业利润率": round(operating_profit / total_revenue * 100, 2) if total_revenue else 0,
        "费用率": round(total_opex / total_revenue * 100, 2) if total_revenue else 0,
        "流动比率": round(total_current_assets / total_current_liabilities, 2) if total_current_liabilities else 0,
        "资产负债率": round(total_liabilities / total_assets * 100, 2) if total_assets else 0,
        "应收账款周转天数": round(ar / total_revenue * 30, 1),
        "应付账款周转天数": round(ap / total_cogs * 30, 1),
    }
    
    months.append({
        "period": month_key,
        "month_num": m,
        "income_statement": {
            "revenue": {
                "total": total_revenue,
                "SaaS平台": product_revenue,
                "电商平台": ecom_revenue,
                "咨询服务": consulting_revenue,
            },
            "cogs": {
                "total": total_cogs,
                "SaaS平台成本": cogs_product,
                "电商平台成本": cogs_ecom,
                "咨询服务成本": cogs_consulting,
            },
            "gross_profit": gross_profit,
            "gross_margin": gross_margin,
            "operating_expenses": {
                "人力成本": salary_expense,
                "营销推广": marketing_expense,
                "研发费用": rnd_expense,
                "行政管理": admin_expense,
                "物流仓储": logistics_expense,
                "其他费用": other_expense,
                "total": total_opex,
            },
            "depreciation": depreciation,
            "operating_profit": operating_profit,
            "interest_expense": interest_expense,
            "profit_before_tax": profit_before_tax,
            "income_tax": income_tax,
            "net_profit": net_profit,
        },
        "balance_sheet": {
            "assets": {
                "current": {
                    "cash": cash,
                    "accounts_receivable": ar,
                    "inventory": inventory,
                    "prepaid_expenses": prepaid,
                    "total": total_current_assets,
                },
                "non_current": {
                    "pp_e": pp_e,
                    "intangible": intangible,
                    "total": total_non_current_assets,
                },
                "total": total_assets,
            },
            "liabilities": {
                "current": {
                    "accounts_payable": ap,
                    "accrued_expenses": accrued_expenses,
                    "tax_payable": tax_payable,
                    "short_term_debt": short_term_debt,
                    "total": total_current_liabilities,
                },
                "non_current": {
                    "long_term_debt": long_term_debt,
                },
                "total": total_liabilities,
            },
            "equity": {
                "paid_in_capital": BASE_EQUITY,
                "retained_earnings": retained_earnings,
                "total": equity,
            },
            "total_liabilities_equity": total_assets,
        },
        "cash_flow": {
            "operating": operating_cf,
            "investing": investing_cf,
            "financing": financing_cf,
            "net_change": net_cf,
            "beginning_cash": round(cash - net_cf),
            "ending_cash": cash,
        },
        "cost_by_dept": dept_costs,
        "cost_by_category": category_costs,
        "key_metrics": key_metrics,
    })

# ============================================================
# 生成 2026 年度预算
# ============================================================
# 基于 2025 年实际数据 + 15% 增长目标
budget_2025_total_revenue = sum(m["income_statement"]["revenue"]["total"] for m in months if m["period"].startswith("2025"))
budget_2026_target = round(budget_2025_total_revenue * 1.15)  # 15%增长

budget_monthly = []
for i in range(12):
    m = i + 1
    season = seasonal_adjust(m)
    trend = trend_growth(12 + i)  # 延续趋势
    
    budget_revenue = round(budget_2026_target / 12 * season / sum(seasonal_adjust(j) for j in range(1, 13)) * 12)
    budget_cogs = round(budget_revenue * 0.62)  # 目标毛利率38%
    budget_opex = round(budget_revenue * 0.25)  # 目标费用率25%
    
    # 部门预算
    dept_budgets = {}
    for dept, ratio in DEPT_COST_RATIO.items():
        dept_budgets[dept] = round((budget_cogs + budget_opex) * ratio)
    
    # 费用科目预算
    cat_budgets = {
        "人力成本": round((budget_cogs + budget_opex) * 0.36),
        "服务器/云服务": round((budget_cogs + budget_opex) * 0.17),
        "营销推广": round((budget_cogs + budget_opex) * 0.17),
        "物流仓储": round((budget_cogs + budget_opex) * 0.08),
        "办公租金": round((budget_cogs + budget_opex) * 0.06),
        "差旅招待": round((budget_cogs + budget_opex) * 0.04),
        "软件许可": round((budget_cogs + budget_opex) * 0.05),
        "外包服务": round((budget_cogs + budget_opex) * 0.04),
        "其他": round((budget_cogs + budget_opex) * 0.03),
    }
    
    budget_monthly.append({
        "period": f"2026-{m:02d}",
        "revenue": budget_revenue,
        "cogs": budget_cogs,
        "opex": budget_opex,
        "gross_profit": budget_revenue - budget_cogs,
        "net_profit_target": round((budget_revenue - budget_cogs - budget_opex) * 0.75),
        "dept_budgets": dept_budgets,
        "category_budgets": cat_budgets,
    })

# ============================================================
# 生成应收应付明细（用于现金流预测）
# ============================================================
# 应收账款账龄
ar_aging = []
for i in range(30):
    days_aging = random.randint(1, 120)
    amount = round(random.uniform(50000, 500000))
    ar_aging.append({
        "customer": f"客户-{i+1:03d}",
        "amount": amount,
        "days_outstanding": days_aging,
        "aging_bucket": "0-30天" if days_aging <= 30 else ("31-60天" if days_aging <= 60 else ("61-90天" if days_aging <= 90 else "90天以上")),
        "expected_collection_week": random.randint(1, 8),
    })

# 应付账款明细
ap_schedule = []
for i in range(20):
    amount = round(random.uniform(20000, 300000))
    ap_schedule.append({
        "supplier": f"供应商-{i+1:03d}",
        "amount": amount,
        "due_week": random.randint(1, 12),
        "category": random.choice(["服务器", "营销服务", "物流", "办公", "软件许可", "外包"]),
    })

# 未来12周订单预测（用于现金流预测）
weekly_order_forecast = []
current_revenue = months[-1]["income_statement"]["revenue"]["total"]
for w in range(1, 13):
    week_revenue = round(current_revenue / 4.33 * noise(0.08))  # 月收入/4.33=周收入
    collection_rate = random.uniform(0.55, 0.75)  # 当周回款率
    weekly_order_forecast.append({
        "week": w,
        "estimated_revenue": week_revenue,
        "estimated_collection": round(week_revenue * collection_rate),
        "deferred_collection": round(week_revenue * (1 - collection_rate)),
    })

# ============================================================
# 汇总数据
# ============================================================
summary = {
    "company": COMPANY,
    "industry": INDUSTRY,
    "currency": CURRENCY,
    "generated_at": datetime.now().isoformat(),
    "data_period": "2025-01 to 2026-05",
    "total_months": len(months),
    "departments": DEPARTMENTS,
    "products": PRODUCTS,
    "cost_categories": COST_CATEGORIES,
    "quick_stats": {
        "2025_total_revenue": sum(m["income_statement"]["revenue"]["total"] for m in months if m["period"].startswith("2025")),
        "2025_total_net_profit": sum(m["income_statement"]["net_profit"] for m in months if m["period"].startswith("2025")),
        "2026_ytd_revenue": sum(m["income_statement"]["revenue"]["total"] for m in months if m["period"].startswith("2026")),
        "2026_ytd_net_profit": sum(m["income_statement"]["net_profit"] for m in months if m["period"].startswith("2026")),
        "2026_annual_budget_revenue": budget_2026_target,
        "latest_cash": months[-1]["balance_sheet"]["assets"]["current"]["cash"],
        "latest_total_assets": months[-1]["balance_sheet"]["assets"]["total"],
    },
}

# ============================================================
# 写入文件
# ============================================================
output_dir = "/home/xiaoai/.openclaw/workspace-finance/data"
os.makedirs(output_dir, exist_ok=True)

output = {
    "summary": summary,
    "monthly_data": months,
    "budget_2026": budget_monthly,
    "ar_aging": ar_aging,
    "ap_schedule": ap_schedule,
    "weekly_order_forecast": weekly_order_forecast,
}

with open(os.path.join(output_dir, "sample_financial_data.json"), "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

# 同时生成CSV方便查阅
import csv

# 月度财务摘要CSV
csv_path = os.path.join(output_dir, "monthly_summary.csv")
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["期间", "营收", "成本", "毛利", "毛利率%", "营业费用", "营业利润", "净利润", "净利率%", 
                     "期末现金", "总资产", "应收账款", "应付账款"])
    for m in months:
        ist = m["income_statement"]
        bs = m["balance_sheet"]
        writer.writerow([
            m["period"], ist["revenue"]["total"], ist["cogs"]["total"], ist["gross_profit"],
            m["key_metrics"]["毛利率"], ist["operating_expenses"]["total"], ist["operating_profit"],
            ist["net_profit"], m["key_metrics"]["净利率"],
            bs["assets"]["current"]["cash"], bs["assets"]["total"],
            bs["assets"]["current"]["accounts_receivable"],
            bs["liabilities"]["current"]["accounts_payable"],
        ])

print(f"✅ 数据生成完成！")
print(f"   JSON: {os.path.join(output_dir, 'sample_financial_data.json')}")
print(f"   CSV:  {csv_path}")
print(f"   月份数: {len(months)}")
print(f"   2025年总营收: {summary['quick_stats']['2025_total_revenue']:,.0f}")
print(f"   2025年净利润: {summary['quick_stats']['2025_total_net_profit']:,.0f}")
print(f"   2026年预算: {budget_2026_target:,.0f}")
print(f"   最新现金: {summary['quick_stats']['latest_cash']:,.0f}")
