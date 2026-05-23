import streamlit as st
import math
import plotly.graph_objects as go
import numpy as np

st.set_page_config(
    page_title="SafeVault · Password Auditor",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&family=Rajdhani:wght@500;600;700&display=swap');

:root {
    --bg:        #07090f;
    --surface:   #0c1018;
    --card:      #111520;
    --border:    #1c2438;
    --border2:   #243048;
    --cyan:      #22d3ee;
    --cyan-dim:  #0891b2;
    --violet:    #a78bfa;
    --green:     #4ade80;
    --red:       #f87171;
    --amber:     #fbbf24;
    --text:      #e2e8f0;
    --text-sub:  #07090f;
    --text-muted:#e2e8f0;
    --font-ui:   'Space Grotesk', sans-serif;
    --font-mono: 'JetBrains Mono', monospace;
    --font-head: 'Rajdhani', sans-serif;
}

html, body, [class*="css"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: var(--font-ui) !important;
}

.stApp {
    background:
        radial-gradient(ellipse 80% 40% at 50% -10%, rgba(34,211,238,.07) 0%, transparent 70%),
        var(--bg) !important;
}

/* subtle dot grid */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: radial-gradient(rgba(34,211,238,.09) 1px, transparent 1px);
    background-size: 28px 28px;
    pointer-events: none;
    z-index: 0;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] * { color: var(--text) !important; }
section[data-testid="stSidebar"] label {
    color: var(--text-sub) !important;
    font-size: .78rem !important;
    font-weight: 600 !important;
    letter-spacing: .06em !important;
    text-transform: uppercase !important;
}
section[data-testid="stSidebar"] input {
    background: #0f1622 !important;
    border: 1px solid var(--border2) !important;
    color: var(--cyan) !important;
    font-family: var(--font-mono) !important;
    border-radius: 8px !important;
    font-size: .95rem !important;
}

.block-container { padding-top: 1.8rem !important; max-width: 1120px !important; }

/* Metric cards */
[data-testid="metric-container"] {
    background: var(--card) !important;
    border: 1px solid var(--border2) !important;
    border-radius: 12px !important;
    padding: 1rem 1.2rem !important;
    box-shadow: 0 0 0 0px transparent !important;
    position: relative !important;
    overflow: hidden !important;
}
[data-testid="metric-container"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--cyan), var(--violet));
}
[data-testid="metric-container"] label {
    color: #22d3ee !important;
    font-size: .72rem !important;
    font-weight: 600 !important;
    letter-spacing: .08em !important;
    text-transform: uppercase !important;
}
[data-testid="stMetricValue"] {
    color: var(--text) !important;
    font-family: var(--font-mono) !important;
    font-size: 1.55rem !important;
    font-weight: 600 !important;
}
[data-testid="stMetricDelta"] { font-size: .75rem !important; }
[data-testid="stMetricDeltaIcon"] { display: none !important; }

/* Expander */
details {
    background: var(--card) !important;
    border: 1px solid var(--border2) !important;
    border-radius: 10px !important;
}
summary { color: var(--cyan) !important; font-weight: 600 !important; }

hr { border-color: var(--border) !important; margin: 1.4rem 0 !important; }

h1, h2, h3 { font-family: var(--font-head) !important; letter-spacing: .03em !important; }

/* ── custom classes ── */

.sv-title {
    font-family: var(--font-head);
    font-size: 2.6rem;
    font-weight: 700;
    letter-spacing: .08em;
    color: var(--text);
    line-height: 1;
}
.sv-title span { color: var(--cyan); }
.sv-subtitle {
    font-size: .9rem;
    color: var(--text-sub);
    margin-top: .4rem;
    font-family: var(--font-ui);
}

.section-tag {
    display: inline-flex;
    align-items: center;
    gap: .4rem;
    font-family: var(--font-mono);
    font-size: .68rem;
    font-weight: 600;
    letter-spacing: .12em;
    text-transform: uppercase;
    color: var(--cyan);
    border: 1px solid rgba(34,211,238,.25);
    background: rgba(34,211,238,.06);
    border-radius: 4px;
    padding: 3px 10px;
    margin-bottom: .9rem;
}

/* formula card */
.fcard {
    background: var(--card);
    border: 1px solid var(--border2);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-bottom: .8rem;
    position: relative;
    overflow: hidden;
}
.fcard::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border2), transparent);
}
.fcard-num {
    font-family: var(--font-mono);
    font-size: .62rem;
    color: var(--violet);
    letter-spacing: .1em;
    text-transform: uppercase;
    margin-bottom: .2rem;
}
.fcard-title {
    font-family: var(--font-head);
    font-size: 1rem;
    font-weight: 600;
    color: var(--text);
    margin-bottom: .5rem;
}
.fcard-result {
    font-family: var(--font-mono);
    font-size: .88rem;
    color: var(--cyan);
    background: rgba(34,211,238,.06);
    border: 1px solid rgba(34,211,238,.15);
    border-radius: 6px;
    padding: .35rem .7rem;
    margin-top: .5rem;
    display: inline-block;
}

/* status */
.status-box {
    border-radius: 12px;
    padding: 1rem 1.4rem;
    margin-bottom: 1.4rem;
    display: flex;
    align-items: center;
    gap: .9rem;
    font-family: var(--font-head);
    font-size: 1.1rem;
    font-weight: 600;
    letter-spacing: .04em;
}
.status-strong { background: rgba(74,222,128,.08); border: 1px solid rgba(74,222,128,.35); color: #86efac; }
.status-mid    { background: rgba(251,191,36,.08);  border: 1px solid rgba(251,191,36,.35);  color: #fde68a; }
.status-weak   { background: rgba(248,113,113,.08); border: 1px solid rgba(248,113,113,.35); color: #fca5a5; }
.status-sub    { font-family: var(--font-ui); font-size: .82rem; opacity: .8; font-weight: 400; }

/* boolean pills */
.pill {
    display: inline-flex; align-items: center; gap: 5px;
    font-family: var(--font-mono); font-size: .78rem; font-weight: 600;
    border-radius: 6px; padding: 4px 12px; margin: 3px 4px 3px 0;
}
.pill-t { background: rgba(74,222,128,.1);  border: 1px solid rgba(74,222,128,.4); color: #86efac; }
.pill-f { background: rgba(248,113,113,.1); border: 1px solid rgba(248,113,113,.4); color: #fca5a5; }

/* tip */
.tip-row {
    background: rgba(251,191,36,.06);
    border: 1px solid rgba(251,191,36,.2);
    border-left: 3px solid var(--amber);
    border-radius: 0 8px 8px 0;
    padding: .65rem 1rem;
    margin-bottom: .5rem;
    color: #fde68a;
    font-size: .87rem;
    font-family: var(--font-ui);
}
.tip-ok {
    background: rgba(74,222,128,.06);
    border: 1px solid rgba(74,222,128,.2);
    border-left: 3px solid var(--green);
    border-radius: 0 8px 8px 0;
    padding: .65rem 1rem;
    color: #86efac;
    font-size: .87rem;
    font-family: var(--font-ui);
}

/* decorative math symbols background */
.math-deco {
    font-family: var(--font-mono);
    font-size: .72rem;
    color: var(--text-muted);
    line-height: 1.9;
    letter-spacing: .05em;
    opacity: .6;
    margin-bottom: 1.2rem;
}
</style>
""", unsafe_allow_html=True)

# ── SIDEBAR ──
st.sidebar.markdown("""
<div style='font-family:"Rajdhani",sans-serif; font-size:1.3rem; font-weight:700; color:#22d3ee; letter-spacing:.08em; margin-bottom:.2rem;'>
🛡️ SAFEVAULT
</div>
<div style='font-family:"Space Grotesk",sans-serif; font-size:.78rem; color:#475569; margin-bottom:1.4rem;'>
Password Security Auditor
</div>
""", unsafe_allow_html=True)

user_pw = st.sidebar.text_input("PASSWORD INPUT", type="password", placeholder="masukkan password...")

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='font-family:"JetBrains Mono",monospace; font-size:.68rem; color:#334155; line-height:2;'>
TOPIK &nbsp;· Keamanan Login<br>
MK &nbsp;&nbsp;&nbsp;&nbsp;· Matematika Terapan<br>
TAHUN · 2026
</div>
""", unsafe_allow_html=True)

# ── HEADER ──
st.markdown("""
<div class='math-deco'>∑ ∧ ∨ ∩ ∪ ∈ ∉ ⊂ ⊃ log₂ N^L ‖v‖ √ ∫ ∂ ∇ ∀ ∃ ≡ ≠ ≤ ≥ → ↔ ⊕ ⊗</div>
<div class='sv-title'>SAFE<span>VAULT</span></div>
<div class='sv-subtitle'>Implementasi Matematika Terapan — Sistem Keamanan Login</div>
""", unsafe_allow_html=True)
st.markdown("<hr style='margin-top:1.2rem;'>", unsafe_allow_html=True)

if user_pw:
    L = len(user_pw)

    # ── 1. HIMPUNAN ──
    s_lower  = set("abcdefghijklmnopqrstuvwxyz")
    s_upper  = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    s_digit  = set("0123456789")
    s_symbol = set("!@#$%^&*()-_=+[{]}\\|;:'\",.<>/?`~")
    pw_set   = set(user_pw)

    used_lower  = pw_set & s_lower
    used_upper  = pw_set & s_upper
    used_digit  = pw_set & s_digit
    used_symbol = pw_set & s_symbol

    # ── 2. KOMBINATORIKA ──
    N = 0
    if used_lower:  N += 26
    if used_upper:  N += 26
    if used_digit:  N += 10
    if used_symbol: N += 32
    total_kombinasi = N ** L if N > 0 else 0

    # ── 3. LOGARITMA — Bit Entropy ──
    entropy = math.log2(total_kombinasi) if total_kombinasi > 0 else 0

    # ── 4. LOGIKA BOOLEAN ──
    x = L >= 12
    y = len(used_digit) > 0
    z = len(used_symbol) > 0
    bool_result = x and y and z

    # ── 5. VEKTOR & MAGNITUDE ──
    v = np.array([L, len(pw_set), N / 10])
    magnitude = np.linalg.norm(v)

    # Tier
    if bool_result and entropy >= 60:
        tier, css, icon = "SANGAT KUAT", "status-strong", "✦"
        note = "Semua kondisi Boolean terpenuhi · Entropy ≥ 60 bit"
    elif entropy >= 40 or sum([x,y,z]) >= 2:
        tier, css, icon = "CUKUP KUAT", "status-mid", "◈"
        note = "Sebagian syarat terpenuhi · Perlu diperkuat"
    else:
        tier, css, icon = "LEMAH", "status-weak", "✗"
        note = "Entropy terlalu rendah · Rentan brute-force"

    # ── STATUS ──
    st.markdown(f"""
    <div class='status-box {css}'>
        <span style='font-size:1.4rem;'>{icon}</span>
        <div>
            <div>STATUS KEAMANAN: {tier}</div>
            <div class='status-sub'>{note}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── METRICS ──
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Panjang (L)", f"{L} char", "≥ 12 ✓" if x else "< 12 ✗")
    m2.metric("Entropy (H)", f"{entropy:.1f} bit", "≥ 60 ✓" if entropy >= 60 else "kurang")
    m3.metric("Ruang Karakter (N)", str(N))
    m4.metric("Magnitude ‖v‖", f"{magnitude:.2f}")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── KOLOM KIRI (formula) + KANAN (chart) ──
    cl, cr = st.columns([1, 1], gap="large")

    with cl:
        st.markdown("<div class='section-tag'>⟨ /⟩ &nbsp; Model Matematis</div>", unsafe_allow_html=True)

        # Card 1 — Himpunan
        st.markdown(f"""
        <div class='fcard'>
            <div class='fcard-num'>01 · Himpunan</div>
            <div class='fcard-title'>Ruang Karakter N</div>
        </div>
        """, unsafe_allow_html=True)
        st.latex(r"N = |\Sigma_l \cup \Sigma_u \cup \Sigma_d \cup \Sigma_s|")
        st.markdown(f"<div class='fcard-result'>N = {N} karakter</div><br>", unsafe_allow_html=True)

        # Card 2 — Kombinatorika
        st.markdown(f"""
        <div class='fcard'>
            <div class='fcard-num'>02 · Kombinatorika</div>
            <div class='fcard-title'>Total Kemungkinan Password</div>
        </div>
        """, unsafe_allow_html=True)
        st.latex(r"\text{Kombinasi} = N^L")
        st.markdown(f"<div class='fcard-result'>{N}^{L} = {total_kombinasi:,.0f}</div><br>", unsafe_allow_html=True)

        # Card 3 — Logaritma
        st.markdown(f"""
        <div class='fcard'>
            <div class='fcard-num'>03 · Logaritma</div>
            <div class='fcard-title'>Bit Entropy</div>
        </div>
        """, unsafe_allow_html=True)
        st.latex(r"H = \log_2(N^L) = L \cdot \log_2 N")
        st.markdown(f"<div class='fcard-result'>H = {entropy:.2f} bit</div><br>", unsafe_allow_html=True)

        # Card 4 — Boolean
        st.markdown(f"""
        <div class='fcard'>
            <div class='fcard-num'>04 · Logika Boolean</div>
            <div class='fcard-title'>Fungsi Keputusan F(x,y,z)</div>
        </div>
        """, unsafe_allow_html=True)
        st.latex(r"F(x,y,z) = x \wedge y \wedge z")
        pc = lambda cond, label: f"<span class='pill pill-{'t' if cond else 'f'}'>{label} = {'T' if cond else 'F'}</span>"
        st.markdown(f"""
        <div style='margin:.5rem 0;'>
            {pc(x,'x: len≥12')}{pc(y,'y: angka')}{pc(z,'z: simbol')}
            <span class='pill pill-{'t' if bool_result else 'f'}'>F = {'TRUE' if bool_result else 'FALSE'}</span>
        </div><br>
        """, unsafe_allow_html=True)

        # Card 5 — Vektor
        st.markdown(f"""
        <div class='fcard'>
            <div class='fcard-num'>05 · Ruang Vektor</div>
            <div class='fcard-title'>Magnitude Keamanan</div>
        </div>
        """, unsafe_allow_html=True)
        st.latex(r"\mathbf{v} = [L,\;|\text{pw\_set}|,\;N/10], \quad \|\mathbf{v}\| = \sqrt{v_1^2+v_2^2+v_3^2}")
        st.markdown(f"<div class='fcard-result'>v = [{L}, {len(pw_set)}, {N/10:.1f}] → ‖v‖ = {magnitude:.2f}</div>", unsafe_allow_html=True)

    with cr:
        st.markdown("<div class='section-tag'>◈ &nbsp; Visualisasi</div>", unsafe_allow_html=True)

        # Bar chart
        cats   = ["Huruf Kecil", "Huruf Besar", "Angka", "Simbol"]
        counts = [len(used_lower), len(used_upper), len(used_digit), len(used_symbol)]

        fig_bar = go.Figure(go.Bar(
            x=cats, y=counts,
            marker=dict(
                color=["rgba(34,211,238,.75)", "rgba(167,139,250,.75)",
                       "rgba(251,191,36,.75)",  "rgba(248,113,113,.75)"],
                line=dict(width=0),
            ),
            text=counts,
            textposition="outside",
            textfont=dict(size=13, color="#e2e8f0", family="JetBrains Mono"),
        ))
        fig_bar.update_layout(
            title=dict(text="Distribusi Himpunan Karakter", font=dict(size=12, color="#94a3b8", family="Space Grotesk"), x=0),
            paper_bgcolor="rgba(17,21,32,1)",
            plot_bgcolor="rgba(17,21,32,1)",
            font=dict(family="Space Grotesk", color="#64748b", size=11),
            xaxis=dict(showgrid=False, color="#64748b", linecolor="#1c2438", tickfont=dict(color="#94a3b8")),
            yaxis=dict(showgrid=True, gridcolor="#1c2438", color="#64748b", zeroline=False, tickfont=dict(color="#64748b")),
            margin=dict(t=36, b=6, l=6, r=6),
            height=245,
            showlegend=False,
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        # Radar chart
        dims = ["Panjang", "Entropy", "Boolean", "Magnitude", "Keunikan"]
        rv = [
            min(L / 20, 1),
            min(entropy / 80, 1),
            1.0 if bool_result else sum([x,y,z]) / 3,
            min(magnitude / 30, 1),
            min(len(pw_set) / 20, 1),
        ]
        rv += [rv[0]]

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=rv, theta=dims + [dims[0]],
            fill="toself",
            fillcolor="rgba(34,211,238,.07)",
            line=dict(color="#22d3ee", width=2),
            marker=dict(color="#22d3ee", size=7),
        ))
        fig_radar.update_layout(
            title=dict(text="Profil Keamanan Password", font=dict(size=12, color="#94a3b8", family="Space Grotesk"), x=0),
            polar=dict(
                bgcolor="rgba(17,21,32,1)",
                radialaxis=dict(visible=True, range=[0,1], showticklabels=False,
                                gridcolor="#1c2438", linecolor="#1c2438"),
                angularaxis=dict(color="#64748b", gridcolor="#1c2438",
                                 tickfont=dict(color="#94a3b8", size=11)),
            ),
            paper_bgcolor="rgba(17,21,32,1)",
            font=dict(family="Space Grotesk", color="#64748b", size=11),
            margin=dict(t=36, b=6, l=30, r=30),
            height=300,
            showlegend=False,
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    # ── REKOMENDASI ──
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='section-tag'>⚡ &nbsp; Rekomendasi</div>", unsafe_allow_html=True)

    tips = []
    if not x: tips.append("Panjang &lt; 12 karakter — tambah panjang agar kondisi <b>x = TRUE</b>")
    if not y: tips.append("Tidak ada angka — tambahkan minimal 1 angka agar <b>y = TRUE</b>")
    if not z: tips.append("Tidak ada simbol — tambahkan karakter seperti <b>!@#$</b> agar <b>z = TRUE</b>")
    if entropy < 60: tips.append(f"Entropy {entropy:.1f} bit di bawah standar — targetkan <b>≥ 60 bit</b>")

    if tips:
        for t in tips:
            st.markdown(f"<div class='tip-row'>⚡ &nbsp; {t}</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='tip-ok'>✦ &nbsp; Password memenuhi semua kriteria keamanan matematis!</div>", unsafe_allow_html=True)

else:
    st.markdown("""
    <div style="text-align:center; padding:4.5rem 0;">
        <div style="font-family:'JetBrains Mono',monospace; font-size:2.5rem; color:#1c2438; margin-bottom:1rem;">
            ∑ ∧ log₂ ‖v‖
        </div>
        <div style="font-size:1rem; color:#334155; font-family:'Space Grotesk',sans-serif; font-weight:500;">
            Masukkan password di sidebar untuk memulai audit
        </div>
        <div style="font-size:.82rem; color:#1e293b; margin-top:.4rem; font-family:'Space Grotesk',sans-serif;">
            5 konsep matematika terapan akan dianalisis secara real-time
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center; font-family:"JetBrains Mono",monospace; font-size:.68rem; color:#1e293b;'>
SAFEVAULT · Tugas Proyek Matematika Terapan 2026 · Topik: Keamanan Login
</div>
""", unsafe_allow_html=True)
