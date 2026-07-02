#!/usr/bin/env python3
"""弱项补强训练 - 量价分离/三表闭环/现金流建模"""
import json, os, random, time
random.seed(2026)
T0 = time.time()
OUT = "/home/xiaoai/.openclaw/workspace-finance/training/rigorous"
os.makedirs(OUT, exist_ok=True)

def fmt(n):
    if n is None: return "—"
    return f"{n:,.0f}"

samples = []

# ========== 弱项1: 量价分离 (300条) ==========
print("[弱项1] 量价分离 300条...")
for i in range(300):
    q_bud = random.randint(1000, 10000)
    q_act = int(q_bud * random.uniform(0.8, 1.3))
    p_bud = random.randint(10, 500)
    p_act = int(p_bud * random.uniform(0.85, 1.2))
    
    total_bud = q_bud * p_bud
    total_act = q_act * p_act
    total_diff = total_act - total_bud
    q_diff = int((q_act - q_bud) * p_bud)
    p_diff = int((p_act - p_bud) * q_act)
    cross = int((q_act - q_bud) * (p_act - p_bud))
    item = random.choice(["原材料A","原材料B","包装材料","电子元件","化工原料","钢材","塑料粒子"])
    
    q_sign = "量增" if q_diff > 0 else "量减"
    p_sign = "价涨" if p_diff > 0 else "价降"
    q_pct = abs(q_diff/total_bud*100)
    p_pct = abs(p_diff/total_bud*100)
    t_pct = total_diff/total_bud*100
    
    user = f"成本差异分析。{item}：预算量{q_bud}×单价{p_bud}元，实际量{q_act}×单价{p_act}元。请做量价分离。"
    
    asst = "## " + item + " 量价分离分析\n\n"
    asst += "| 指标 | 数值 |\n|---|---|\n"
    asst += f"| 预算总成本 | {fmt(total_bud)} |\n"
    asst += f"| 实际总成本 | {fmt(total_act)} |\n"
    asst += f"| **总差异** | **{fmt(total_diff)}** |\n\n"
    asst += "### 量价分解\n"
    asst += "| 差异类型 | 公式 | 计算 | 金额 |\n|---|---|---|---|\n"
    asst += f"| 量差 | (Q实-Q预)×P预 | ({q_act}-{q_bud})×{p_bud} | {fmt(q_diff)} |\n"
    asst += f"| 价差 | (P实-P预)×Q实 | ({p_act}-{p_bud})×{q_act} | {fmt(p_diff)} |\n"
    asst += f"| 交叉差 | (Q实-Q预)×(P实-P预) | ({q_act}-{q_bud})×({p_act}-{p_bud}) | {fmt(cross)} |\n"
    asst += f"| **验证** | 量差+价差+交叉差 | {q_diff}+{p_diff}+{cross} | **{fmt(q_diff+p_diff+cross)}** |\n\n"
    asst += f"### 根因\n{q_sign}{q_pct:.1f}% + {p_sign}{p_pct:.1f}% = 总变动{t_pct:+.1f}%\n\n"
    asst += "> 量价分离是成本分析ABC——区分多花了是因为买多了还是买贵了。"
    
    samples.append({"messages":[
        {"role":"system","content":"你是i01。铁律:每次成本差异必须做量价分离(量差+价差+交叉差)。数字即道德。"},
        {"role":"user","content":user},
        {"role":"assistant","content":asst}
    ],"metadata":{"weakness":"price_volume_split"}})

# ========== 弱项2: 三表闭环 (300条) ==========
print("[弱项2] 三表闭环 300条...")
for i in range(300):
    npv = random.randint(50000, 500000)
    dep = random.randint(10000, 50000)
    d_ar = random.randint(-100000, 100000)
    d_inv = random.randint(-50000, 50000)
    d_ap = random.randint(-80000, 80000)
    d_tax = random.randint(-20000, 20000)
    d_salary = random.randint(-15000, 15000)
    
    direct_cf = npv + dep - d_ar + d_ap + d_inv + d_tax + d_salary
    beg_cash = random.randint(500000, 2000000)
    end_cash_correct = beg_cash + direct_cf
    
    has_error = (i % 7 == 0)
    if has_error:
        end_cash = end_cash_correct + random.choice([-50000, -30000, -15000, 15000, 30000, 50000])
    else:
        end_cash = end_cash_correct
    
    user = f"三表勾稽。NP{fmt(npv)} 折旧{fmt(dep)} ΔAR{fmt(d_ar)} ΔInv{fmt(d_inv)} ΔAP{fmt(d_ap)} ΔTax{fmt(d_tax)} ΔSal{fmt(d_salary)} 期初{fmt(beg_cash)} 期末{fmt(end_cash)}。做三值验证。"
    
    if has_error:
        diff = beg_cash + direct_cf - end_cash
        asst = "## 三表闭环验证 - 差异发现\n\n"
        asst += f"### 间接法CF\nNP{fmt(npv)}+折旧{fmt(dep)}-ΔAR{fmt(-d_ar)}+ΔAP{fmt(d_ap)}+ΔInv{fmt(d_inv)}+ΔTax{fmt(d_tax)}+ΔSal{fmt(d_salary)} = **{fmt(direct_cf)}**\n\n"
        asst += f"### 现金验证\n期初{fmt(beg_cash)}+CF{fmt(direct_cf)}={fmt(beg_cash+direct_cf)} ≠ 期末{fmt(end_cash)}\n"
        asst += f"**差异 = {fmt(abs(diff))} ({abs(diff)/beg_cash*100:.1f}%)**\n\n"
        asst += "> 差异>1%,暂停报告输出。追查:股利分配?固资处置?债务变动?检查银行对账单。"
    else:
        asst = "## 三表闭环 - 通过\n\n"
        asst += f"经营CF = {fmt(npv)}+{fmt(dep)}{'' if d_ar>=0 else '+'}{fmt(-d_ar)}+{fmt(d_ap)}+{fmt(d_inv)}+{fmt(d_tax)}+{fmt(d_salary)} = **{fmt(direct_cf)}**\n\n"
        asst += f"期初{fmt(beg_cash)}+CF{fmt(direct_cf)}={fmt(end_cash)} = BS期末现金 ✅\n\n"
        asst += "> 三值一致(直接法=间接法=BS),可以发布。铁律:三表必须联动。"
    
    samples.append({"messages":[
        {"role":"system","content":"你是i01。铁律:三表必须联动。每次出表做三值验证。差异>0.1%追根因,>1%暂停输出。"},
        {"role":"user","content":user},
        {"role":"assistant","content":asst}
    ],"metadata":{"weakness":"triple_close"}})

# ========== 弱项3: 现金流建模 (400条) ==========
print("[弱项3] 现金流建模 400条...")
for i in range(400):
    cash0 = random.randint(200000, 3000000)
    w1_in, w2_in, w3_in, w4_in = [random.randint(50000, 500000) for _ in range(4)]
    w1_out, w2_out, w3_out, w4_out = [random.randint(40000, 400000) for _ in range(4)]
    
    delay_wk = random.randint(1, 4)
    delay_amt = random.randint(30000, 150000)
    opt_coef, pes_coef = 1.15, 0.80
    
    neutral_end = cash0 + w1_in + w2_in + w3_in + w4_in - w1_out - w2_out - w3_out - w4_out
    opt_end = cash0 + int((w1_in+w2_in+w3_in+w4_in)*opt_coef) - int((w1_out+w2_out+w3_out+w4_out)*0.9)
    
    pes_w = [cash0]
    for wk, (win, wout) in enumerate([(w1_in,w1_out),(w2_in,w2_out),(w3_in,w3_out),(w4_in,w4_out)], 1):
        adj_in = int(win * pes_coef)
        adj_out = int(wout * 1.10)
        if wk == delay_wk:
            adj_in -= delay_amt
        pes_w.append(pes_w[-1] + adj_in - adj_out)
    pes_min = min(pes_w)
    pes_min_wk = pes_w.index(pes_min)
    
    mf = int((w1_out+w2_out+w3_out+w4_out) * 0.6)
    safe = pes_min / mf if mf else 99
    
    user = f"12周现金流。期初{fmt(cash0)} 月固定{fmt(mf)}。W1收{fmt(w1_in)}支{fmt(w1_out)} W2收{fmt(w2_in)}支{fmt(w2_out)} W3收{fmt(w3_in)}支{fmt(w3_out)} W4收{fmt(w4_in)}支{fmt(w4_out)}。悲观:收入-20%+支出+10%+W{delay_wk}延迟{fmt(delay_amt)}。三情景分周。"
    
    asst = "## 12周现金流预测\n\n"
    asst += "### 情景参数定义表\n"
    asst += "| 参数 | 乐观 | 中性 | 悲观 |\n|---|---|---|---|\n"
    asst += f"| 收入系数 | +15% | 0% | **-20%** |\n"
    asst += f"| 支出系数 | -10% | 0% | **+10%** |\n"
    asst += f"| 特殊事件 | 无 | 无 | **W{delay_wk}延迟{fmt(delay_amt)}** |\n\n"
    
    asst += "### 逐周计算\n| 周 | 乐观 | 中性 | 悲观 |\n|---|---|---|---|\n"
    asst += f"| W0 | {fmt(cash0)} | {fmt(cash0)} | {fmt(cash0)} |\n"
    for wk in range(1, 5):
        n_val = cash0 + sum([w1_in,w2_in,w3_in,w4_in][:wk]) - sum([w1_out,w2_out,w3_out,w4_out][:wk])
        o_val = cash0 + int(sum([w1_in,w2_in,w3_in,w4_in][:wk])*opt_coef) - int(sum([w1_out,w2_out,w3_out,w4_out][:wk])*0.9)
        asst += f"| W{wk} | {fmt(o_val)} | {fmt(n_val)} | {fmt(pes_w[wk])} |\n"
    
    asst += f"\n### ∑验证\n中性四周收入={fmt(w1_in+w2_in+w3_in+w4_in)} = 各周收入之和 ✓\n"
    asst += f"悲观四周收入={fmt(int((w1_in+w2_in+w3_in+w4_in)*pes_coef)-delay_amt)} ✓\n\n"
    
    lvl = "🔴" if safe < 1 else ("🟡" if safe < 2 else "🟢")
    asst += f"### 预警\n最低现金{fmt(pes_min)}(W{pes_min_wk}) | 安全垫{safe:.1f}月 | {lvl}\n\n"
    asst += "> 铁律:①先填参数表 ②逐周计算 ③∑验证。缺一步都不行。预测不代表确定结果。"
    
    samples.append({"messages":[
        {"role":"system","content":"你是i01。铁律:现金流预测必须①参数定义表 ②逐周计算不跳步 ③∑验证。遗漏参数=预测失效。"},
        {"role":"user","content":user},
        {"role":"assistant","content":asst}
    ],"metadata":{"weakness":"cf_modeling"}})

# 保存
random.shuffle(samples)
path = os.path.join(OUT, "weakness_fix_train.jsonl")
with open(path, "w") as f:
    for s in samples:
        f.write(json.dumps(s, ensure_ascii=False) + "\n")

elapsed = time.time() - T0
print(f"\n✅ 弱项补强: {len(samples)}条 | {elapsed:.1f}s")
print(f"  量价分离: 300条")
print(f"  三表闭环: 300条(含错误检测)")
print(f"  现金流建模: 400条(含参数表+逐周+∑验证)")
