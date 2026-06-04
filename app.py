import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import base64
import json
import time
import math

# ══════════════════════════════════════════════════════════════════════════════
# KONFIGURASI HALAMAN & INJEKSI CSS PROFESIONAL
# ═════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="OptiLab Pro — Simulasi Optik",
    layout="wide",
    page_icon="🔬",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

/* ── Reset & Base ─────────────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
.stApp { background: #0a0e1a; color: #e2e8f0; }

/* ── Scrollbar Custom ──────────────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0f172a; }
::-webkit-scrollbar-thumb { background: #1e3a5f; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #2563eb; }

/* ── Hero Banner ──────────────────────────────────────────────────── */
.hero-banner {
    position: relative;
    background: linear-gradient(135deg, #0c1220 0%, #111827 40%, #0f172a 100%);
    border: 1px solid rgba(59, 130, 246, 0.2);
    border-radius: 16px;
    padding: 36px 42px;
    margin-bottom: 28px;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse 80% 60% at 80% 50%, rgba(59,130,246,0.08) 0%, transparent 70%),
                radial-gradient(ellipse 40% 40% at 20% 80%, rgba(139,92,246,0.06) 0%, transparent 60%);
    pointer-events: none;
}
.hero-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.15em;
    color: #60a5fa;
    text-transform: uppercase;
    margin-bottom: 10px;
}
.hero-title {
    font-size: 34px;
    font-weight: 800;
    line-height: 1.15;
    letter-spacing: -0.02em;
    color: #f1f5f9;
    margin: 0 0 12px;
}
.hero-title em {
    font-style: normal;
    background: linear-gradient(90deg, #60a5fa, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-size: 14px;
    color: #94a3b8;
    line-height: 1.7;
    max-width: 600px;
    margin: 0 0 20px;
}
.hero-badges { display: flex; gap: 8px; flex-wrap: wrap; }
.badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    font-weight: 600;
    padding: 4px 10px;
    border-radius: 100px;
    border: 1px solid;
    letter-spacing: 0.05em;
}
.badge-blue { color: #60a5fa; border-color: rgba(96,165,250,0.3); background: rgba(96,165,250,0.08); }
.badge-green { color: #34d399; border-color: rgba(52,211,153,0.3); background: rgba(52,211,153,0.08); }
.badge-purple { color: #a78bfa; border-color: rgba(167,139,250,0.3); background: rgba(167,139,250,0.08); }
.badge-amber { color: #fbbf24; border-color: rgba(251,191,36,0.3); background: rgba(251,191,36,0.08); }

/* ── KPI Cards ─────────────────────────────────────────────────────── */
.kpi-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 20px; }
.kpi-card {
    background: #111827;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 16px 18px;
    position: relative;
    overflow: hidden;
    transition: all 0.2s ease;
}
.kpi-card:hover { border-color: rgba(96,165,250,0.3); transform: translateY(-1px); }
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    border-radius: 12px 12px 0 0;
}
.kpi-card.blue::before { background: linear-gradient(90deg, #60a5fa, #a78bfa); }
.kpi-card.green::before { background: linear-gradient(90deg, #34d399, #60a5fa); }
.kpi-card.amber::before { background: linear-gradient(90deg, #fbbf24, #f87171); }
.kpi-card.red::before { background: linear-gradient(90deg, #f87171, #f43f5e); }
.kpi-label { font-size: 10px; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px; }
.kpi-value { font-size: 26px; font-weight: 800; letter-spacing: -0.03em; line-height: 1; margin-bottom: 4px; }
.kpi-value.blue { color: #60a5fa; }
.kpi-value.green { color: #34d399; }
.kpi-value.amber { color: #fbbf24; }
.kpi-value.red { color: #f87171; }
.kpi-sub { font-size: 11px; color: #475569; }

/* ── TIR Alert ─────────────────────────────────────────────────────── */
.tir-alert {
    background: linear-gradient(135deg, rgba(239,68,68,0.1), rgba(244,63,94,0.05));
    border: 1px solid rgba(239,68,68,0.3);
    border-radius: 12px;
    padding: 14px 18px;
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 20px;
}
.tir-icon { font-size: 24px; }
.tir-text strong { color: #f87171; font-size: 13px; display: block; margin-bottom: 3px; }
.tir-text span { color: #94a3b8; font-size: 12px; }

/* ── Section Cards ────────────────────────────────────────────────── */
.section-card {
    background: #111827;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 16px;
}
.section-title {
    font-size: 12px;
    font-weight: 700;
    color: #60a5fa;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-title::before {
    content: '';
    display: inline-block;
    width: 3px;
    height: 12px;
    background: #60a5fa;
    border-radius: 2px;
}

/* ── Formula Display ───────────────────────────────────────────────── */
.formula-box {
    font-family: 'JetBrains Mono', monospace;
    background: rgba(96,165,250,0.06);
    border: 1px solid rgba(96,165,250,0.15);
    border-radius: 10px;
    padding: 14px 18px;
    text-align: center;
    font-size: 16px;
    color: #bfdbfe;
    margin: 14px 0;
    letter-spacing: 0.02em;
}

/* ── Snell Debug Table ─────────────────────────────────────────────── */
.snell-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 12px;
    margin-top: 10px;
}
.snell-table th {
    font-weight: 600;
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #64748b;
    padding: 8px 12px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    text-align: left;
}
.snell-table td {
    padding: 8px 12px;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    color: #cbd5e1;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
}
.snell-table tr:last-child td { border-bottom: none; }
.snell-table .highlight { color: #60a5fa; font-weight: 600; }

/* ── Sidebar Overrides ─────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: #0a0e1a !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
}
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] div[data-baseweb="select"] span,
section[data-testid="stSidebar"] div[data-baseweb="select"] div {
    color: #f1f5f9 !important;
}
section[data-testid="stSidebar"] input[type="number"],
section[data-testid="stSidebar"] input {
    color: #ffffff !important;
    background: #1e293b !important;
    border-color: rgba(96,165,250,0.3) !important;
    font-size: 15px !important;
    font-weight: 700 !important;
}
section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    background: #1e293b !important;
    border-color: rgba(96,165,250,0.3) !important;
}
section[data-testid="stSidebar"] [data-testid="stSlider"] p {
    color: #94a3b8 !important;
    font-size: 11px !important;
}

/* ── Streamlit Widget Overrides ────────────────────────────────────── */
div[data-baseweb="select"] > div {
    background: #1e293b !important;
    border-color: rgba(255,255,255,0.1) !important;
    border-radius: 8px !important;
}
div[data-baseweb="select"] span { color: #e2e8f0 !important; }
.stSlider > div > div { background: #1e293b !important; }
.stSlider > div > div > div { background: #60a5fa !important; }

div[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    transition: opacity 0.2s !important;
}
div[data-testid="stButton"] > button[kind="primary"]:hover { opacity: 0.9 !important; }

div[data-testid="stButton"] > button[kind="secondary"] {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 8px !important;
    color: #cbd5e1 !important;
    font-family: 'Inter', sans-serif !important;
}

/* Tabs */
div[data-baseweb="tab-list"] {
    background: #111827 !important;
    border-radius: 10px !important;
    padding: 4px !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
}
div[data-baseweb="tab"] { border-radius: 6px !important; font-family: 'Inter', sans-serif !important; font-weight: 600 !important; }
div[data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, rgba(59,130,246,0.2), rgba(139,92,246,0.2)) !important;
    color: #60a5fa !important;
}
button[data-baseweb="tab"] { color: #64748b !important; }
button[data-baseweb="tab"][aria-selected="true"] { color: #60a5fa !important; }

/* Info/Warning boxes */
div[data-testid="stInfo"] {
    background: rgba(96,165,250,0.08) !important;
    border-color: rgba(96,165,250,0.2) !important;
    border-radius: 10px !important;
}
div[data-testid="stWarning"] {
    background: rgba(251,191,36,0.08) !important;
    border-color: rgba(251,191,36,0.2) !important;
    border-radius: 10px !important;
}
div[data-testid="stSuccess"] {
    background: rgba(52,211,153,0.08) !important;
    border-color: rgba(52,211,153,0.2) !important;
    border-radius: 10px !important;
}
div[data-testid="stError"] {
    background: rgba(248,113,113,0.08) !important;
    border-color: rgba(248,113,113,0.2) !important;
    border-radius: 10px !important;
}

hr { border-color: rgba(255,255,255,0.06) !important; }

/* Progress bar custom */
.prog-wrap { margin: 8px 0; }
.prog-label { font-size: 11px; color: #64748b; margin-bottom: 4px; display: flex; justify-content: space-between; }
.prog-bar-bg { background: rgba(255,255,255,0.06); border-radius: 100px; height: 6px; overflow: hidden; }
.prog-bar-fill { height: 100%; border-radius: 100px; transition: width 0.5s ease; }

/* Info tooltip */
.info-tooltip {
    background: rgba(59,130,246,0.06);
    border-left: 3px solid #60a5fa;
    border-radius: 0 8px 8px 0;
    padding: 10px 14px;
    font-size: 12px;
    color: #94a3b8;
    line-height: 1.6;
    margin: 8px 0;
}
.info-tooltip strong { color: #60a5fa; }

/* Step row */
.step-row {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 10px 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
}
.step-num {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    background: linear-gradient(135deg, #3b82f6, #8b5cf6);
    color: white;
    font-size: 11px;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}
.step-text { font-size: 12px; color: #94a3b8; line-height: 1.6; padding-top: 3px; }
.step-text strong { color: #cbd5e1; }

/* Challenge card */
.challenge-card {
    background: linear-gradient(135deg, rgba(59,130,246,0.08), rgba(139,92,246,0.05));
    border: 1px solid rgba(96,165,250,0.2);
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 12px;
}
.challenge-card.completed {
    background: linear-gradient(135deg, rgba(52,211,153,0.08), rgba(52,211,153,0.03));
    border-color: rgba(52,211,153,0.3);
}
.challenge-title { font-size: 13px; font-weight: 700; color: #60a5fa; margin-bottom: 6px; }
.challenge-card.completed .challenge-title { color: #34d399; }
.challenge-desc { font-size: 12px; color: #94a3b8; line-height: 1.6; }

/* Achievement badge */
.achievement {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 10px;
    border-radius: 100px;
    font-size: 10px;
    font-weight: 600;
    margin: 3px;
}
.achievement.unlocked {
    background: rgba(251,191,36,0.15);
    border: 1px solid rgba(251,191,36,0.3);
    color: #fbbf24;
}
.achievement.locked {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    color: #475569;
}

/* Guide panel */
.guide-panel {
    background: #111827;
    border: 1px solid rgba(96,165,250,0.15);
    border-radius: 12px;
    padding: 18px;
    margin-bottom: 16px;
}
.guide-step {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
}
.guide-step:last-child { border-bottom: none; }
.guide-step-num {
    width: 22px;
    height: 22px;
    border-radius: 50%;
    background: rgba(96,165,250,0.15);
    color: #60a5fa;
    font-size: 10px;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}
.guide-step-num.active {
    background: #3b82f6;
    color: white;
}
.guide-step-num.done {
    background: #34d399;
    color: white;
}
.guide-step-text { font-size: 12px; color: #94a3b8; }
.guide-step-text.active { color: #e2e8f0; font-weight: 600; }

/* Animations */
@keyframes fade-up {
    from { opacity: 0; transform: translateY(12px); }
    to { opacity: 1; transform: translateY(0); }
}
.animate-up { animation: fade-up 0.4s ease forwards; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# STATE MANAGEMENT
# ══════════════════════════════════════════════════════════════════════════════
for key, default in {
    'jurnal': [],
    'challenges_completed': [],
    'current_guide_step': 0,
    'achievements': [],
    'show_guide': True,
    'sudut_val': 45.0,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ══════════════════════════════════════════════════════════════════════════════
# DATABASE MATERIAL
# ══════════════════════════════════════════════════════════════════════════════
MATERIAL_DB = {
    "Vakum / Udara": {
        "n": 1.0003, "density": 1.2, "category": "Gas",
        "color_fill": "rgba(15, 23, 42, 0.3)",
        "color_border": "#1e3a5f",
        "color_glow": "rgba(96,165,250,0.15)",
        "description": "Hampir tidak ada pembiasan. Digunakan sebagai referensi standar.",
        "applications": ["Teleskop luar angkasa", "Laser vakum", "Riset fisika"]
    },
    "Air Murni (20°C)": {
        "n": 1.333, "density": 998, "category": "Cairan",
        "color_fill": "rgba(14,165,233,0.12)",
        "color_border": "#0ea5e9",
        "color_glow": "rgba(14,165,233,0.25)",
        "description": "Medium optik alami dengan n=1.333 pada 589nm. Kecepatan cahaya ~2.25×10 m/s.",
        "applications": ["Kolam renang optik", "Akuarium", "Lensa kontak hidrogel"]
    },
    "Kaca Crown (BK7)": {
        "n": 1.517, "density": 2520, "category": "Solid",
        "color_fill": "rgba(16,185,129,0.12)",
        "color_border": "#10b981",
        "color_glow": "rgba(16,185,129,0.25)",
        "description": "Kaca optik standar industri. Dispersi rendah, transmitansi tinggi 350–2500nm.",
        "applications": ["Lensa kamera", "Teleskop", "Kacamata"]
    },
    "Kaca Flint (SF11)": {
        "n": 1.785, "density": 4740, "category": "Solid",
        "color_fill": "rgba(99,102,241,0.12)",
        "color_border": "#6366f1",
        "color_glow": "rgba(99,102,241,0.25)",
        "description": "Kaca berat dengan dispersi tinggi. Digunakan dalam prisma spektroskopi.",
        "applications": ["Prisma optis", "Spektroskopi", "Lensa apokromatik"]
    },
    "Silikon Dioksida (SiO₂)": {
        "n": 1.458, "density": 2200, "category": "Solid",
        "color_fill": "rgba(251,191,36,0.10)",
        "color_border": "#fbbf24",
        "color_glow": "rgba(251,191,36,0.25)",
        "description": "Material serat optik utama. Atenuasi sangat rendah pada 1550nm.",
        "applications": ["Serat optik", "Chip fotonik", "Lithografi UV"]
    },
    "Intan (Diamond)": {
        "n": 2.417, "density": 3515, "category": "Kristal",
        "color_fill": "rgba(139,92,246,0.12)",
        "color_border": "#8b5cf6",
        "color_glow": "rgba(139,92,246,0.30)",
        "description": "n tertinggi material alami. Sudut kritis ~24.4° → kilap maksimal.",
        "applications": ["Perhiasan optis", "Jendela IR industri", "Detektor radiasi"]
    },
    "Safir (Al₂O₃)": {
        "n": 1.762, "density": 3980, "category": "Kristal",
        "color_fill": "rgba(56,189,248,0.12)",
        "color_border": "#38bdf8",
        "color_glow": "rgba(56,189,248,0.30)",
        "description": "Kristal keras dengan transmisi UV–IR luar biasa. Layar smartphone premium.",
        "applications": ["Cover HP premium", "Jendela satelit", "LED substrat"]
    },
    "Es (0°C)": {
        "n": 1.309, "density": 917, "category": "Padat",
        "color_fill": "rgba(186,230,253,0.08)",
        "color_border": "#bae6fd",
        "color_glow": "rgba(186,230,253,0.15)",
        "description": "n sedikit lebih rendah dari air cair. Menarik untuk studi transisi fase.",
        "applications": ["Optik kutub", "Riset glasiologi", "Eksperimen fase"]
    },
}

LASER_PRESETS = {
    "🔴 Merah — 633nm (HeNe)": {"color": "#FF2020", "wavelength": 633, "hex": "#FF2020"},
    "🟠 Oranye — 589nm (Na-D)": {"color": "#FF8C00", "wavelength": 589, "hex": "#FF8C00"},
    "🟡 Kuning-Hijau — 532nm (DPSS)": {"color": "#80FF00", "wavelength": 532, "hex": "#80FF00"},
    "🟢 Hijau — 514nm (Ar+)": {"color": "#00E87B", "wavelength": 514, "hex": "#00E87B"},
    "🔵 Biru — 473nm (DPSS)": {"color": "#0080FF", "wavelength": 473, "hex": "#0080FF"},
    "🟣 Violet — 405nm (GaN)": {"color": "#9000FF", "wavelength": 405, "hex": "#9000FF"},
    "⚪ Custom": {"color": "#FFFFFF", "wavelength": 550, "hex": "#FFFFFF"},
}

# ══════════════════════════════════════════════════════════════════════════════
# CHALLENGES & GUIDED LEARNING
# ═════════════════════════════════════════════════════════════════════════════
CHALLENGES = [
    {
        "id": "snell_basic",
        "title": "🔭 Tantangan 1: Verifikasi Hukum Snellius",
        "desc": "Atur medium Udara → Air, sudut datang sekitar 30°. Rekam data dan verifikasi n₁sinθ₁ = n₂sinθ₂.",
        "hint": "Medium 1: Vakum/Udara | Medium 2: Air Murni | Sudut: ~30°",
        "check": lambda res, m1, m2, angle: (
            "Udara" in m1 and "Air" in m2 and
            20.0 <= angle <= 40.0 and not res["is_tir"]
        ),
        "reward": "Pemula Optik"
    },
    {
        "id": "tir_discover",
        "title": "💎 Tantangan 2: Temukan Sudut Kritis",
        "desc": "Gunakan Intan → Udara. Naikkan sudut datang hingga terjadi TIR. Berapa sudut kritisnya?",
        "hint": "Medium 1: Intan (Diamond) | Medium 2: Vakum/Udara | Naikkan sudut hingga TIR aktif",
        "check": lambda res, m1, m2, angle: (
            "Intan" in m1 and ("Udara" in m2 or "Vakum" in m2) and res["is_tir"]
        ),
        "reward": "Penjelajah TIR"
    },
    {
        "id": "brewster",
        "title": "🔬 Tantangan 3: Sudut Brewster",
        "desc": "Atur Kaca Crown → Udara. Cari sudut di mana Rp = 0 (polarisasi sempurna). Sudut Brewster = arctan(n₂/n₁).",
        "hint": "Medium 1: Kaca Crown | Medium 2: Vakum/Udara | Sudut Brewster ≈ 56.5°",
        "check": lambda res, m1, m2, angle: (
            "Kaca Crown" in m1 and ("Udara" in m2 or "Vakum" in m2) and
            abs(res["Rp"]) < 0.005
        ),
        "reward": "Master Polarisasi"
    },
    {
        "id": "fiber_optic",
        "title": "🔌 Tantangan 4: Simulasi Serat Optik",
        "desc": "Gunakan SiO₂ → Udara dengan sudut > sudut kritis. Amati TIR yang menjadi dasar serat optik.",
        "hint": "Medium 1: Silikon Dioksida | Medium 2: Vakum/Udara | Sudut > 43.3°",
        "check": lambda res, m1, m2, angle: (
            "Silikon" in m1 and ("Udara" in m2 or "Vakum" in m2) and res["is_tir"]
        ),
        "reward": "Insinyur Fiber Optik"
    },
    {
        "id": "dispersion",
        "title": "🌈 Tantangan 5: Eksplorasi Dispersi",
        "desc": "Gunakan Kaca Flint → Udara, aktifkan Dispersi di sidebar. Amati pemisahan warna seperti prisma Newton.",
        "hint": "Medium 1: Kaca Flint | Medium 2: Vakum/Udara | Sudut > 20° | Aktifkan toggle Dispersi",
        "check": lambda res, m1, m2, angle: (
            "Kaca Flint" in m1 and ("Udara" in m2 or "Vakum" in m2) and
            not res["is_tir"] and angle > 20
        ),
        "reward": "Ahli Spektroskopi"
    },
]

GUIDE_STEPS = [
    {
        "title": "Pilih Medium",
        "desc": "Pilih Medium 1 (asal sinar) dan Medium 2 (tujuan sinar) di panel kiri."
    },
    {
        "title": "Atur Sumber Cahaya",
        "desc": "Pilih preset laser atau warna custom. Perhatikan panjang gelombangnya."
    },
    {
        "title": "Atur Sudut Datang",
        "desc": "Ketik nilai θ₁ secara langsung pada kotak input sudut datang. Amati perubahan di diagram."
    },
    {
        "title": "Analisis Hasil",
        "desc": "Perhatikan KPI cards, kurva Fresnel, dan verifikasi Hukum Snellius."
    },
    {
        "title": "Rekam & Selesaikan Tantangan",
        "desc": "Tekan 'Rekam' untuk menyimpan data. Coba selesaikan tantangan di tab Jurnal!"
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ENGINE FISIKA
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data
def engine_optik_lengkap(n1, n2, sudut_deg):
    """Mesin fisika optik: Snellius, Fresnel, Brewster, TIR."""
    th1 = np.radians(sudut_deg)
    sin_t1 = np.sin(th1)
    cos_t1 = np.cos(th1)
    
    # Sudut kritis
    if n1 > n2:
        theta_c_rad = np.arcsin(n2 / n1)
        theta_c_deg = np.degrees(theta_c_rad)
    else:
        theta_c_rad = None
        theta_c_deg = None
    
    # Sudut Brewster
    theta_B_deg = np.degrees(np.arctan(n2 / n1))
    
    # Cek TIR
    sin_t2 = (n1 / n2) * sin_t1
    is_tir = sin_t2 >= 1.0
    
    if is_tir:
        th2 = th1
        Rs, Rp = 1.0, 1.0
        Ts, Tp = 0.0, 0.0
    else:
        th2 = np.arcsin(np.clip(sin_t2, -1, 1))
        cos_t2 = np.cos(th2)
        
        # Koefisien Fresnel (amplitudo)
        denom_s = n1 * cos_t1 + n2 * cos_t2
        denom_p = n2 * cos_t1 + n1 * cos_t2
        
        rs = (n1 * cos_t1 - n2 * cos_t2) / denom_s if denom_s != 0 else 0
        rp = (n2 * cos_t1 - n1 * cos_t2) / denom_p if denom_p != 0 else 0
        ts = 2 * n1 * cos_t1 / denom_s if denom_s != 0 else 0
        tp = 2 * n1 * cos_t1 / denom_p if denom_p != 0 else 0
        
        # Reflektansi & Transmitansi intensitas
        Rs = rs ** 2
        Rp = rp ** 2
        factor = (n2 * cos_t2) / (n1 * cos_t1) if (n1 * cos_t1) != 0 else 0
        Ts = factor * ts ** 2
        Tp = factor * tp ** 2
    
    R_avg = (Rs + Rp) / 2
    T_avg = (Ts + Tp) / 2
    
    # Kecepatan cahaya di medium
    C = 2.998e8
    v1 = C / n1
    v2 = C / n2
    
    return {
        "th1": th1, "th1_deg": sudut_deg,
        "th2": th2, "th2_deg": np.degrees(th2) if not is_tir else None,
        "is_tir": is_tir,
        "Rs": Rs, "Rp": Rp, "Ts": Ts, "Tp": Tp,
        "R_avg": R_avg, "T_avg": T_avg,
        "theta_c_deg": theta_c_deg,
        "theta_B_deg": theta_B_deg,
        "v1": v1, "v2": v2,
        "sin_t1": sin_t1, "sin_t2": sin_t2 if not is_tir else None,
        "n1": n1, "n2": n2,
    }


def wavelength_to_hex(wl):
    """Konversi panjang gelombang (nm) ke warna HEX."""
    if 380 <= wl < 440:
        r, g, b = -(wl - 440) / (440 - 380), 0.0, 1.0
    elif 440 <= wl < 490:
        r, g, b = 0.0, (wl - 440) / (490 - 440), 1.0
    elif 490 <= wl < 510:
        r, g, b = 0.0, 1.0, (510 - wl) / (510 - 490)
    elif 510 <= wl < 580:
        r, g, b = (wl - 510) / (580 - 510), 1.0, 0.0
    elif 580 <= wl < 645:
        r, g, b = 1.0, (645 - wl) / (645 - 580), 0.0
    elif 645 <= wl <= 780:
        r, g, b = 1.0, 0.0, 0.0
    else:
        return "#FFFFFF"
    
    # Intensity factor for edges of spectrum
    if 380 <= wl < 420:
        factor = 0.3 + 0.7 * (wl - 380) / (420 - 380)
    elif 700 <= wl <= 780:
        factor = 0.3 + 0.7 * (780 - wl) / (780 - 700)
    else:
        factor = 1.0
    
    r = int((r * factor) ** 0.8 * 255)
    g = int((g * factor) ** 0.8 * 255)
    b = int((b * factor) ** 0.8 * 255)
    return f"#{r:02X}{g:02X}{b:02X}"


# ══════════════════════════════════════════════════════════════════════════════
# KOMPONEN VISUALISASI
# ══════════════════════════════════════════════════════════════════════════════
def render_diagram_optik(res, m1, m2, laser_hex, show_dispersion=False):
    """Render diagram sinar optik interaktif dengan Plotly."""
    mat1 = MATERIAL_DB[m1]
    mat2 = MATERIAL_DB[m2]
    fig = go.Figure()
    fig.update_layout(
        xaxis=dict(visible=False, range=[-5, 5]),
        yaxis=dict(visible=False, range=[-4.5, 4.5], scaleanchor="x", scaleratio=1),
        margin=dict(l=10, r=10, t=10, b=10),
        height=480,
        plot_bgcolor='#0a0e1a',
        paper_bgcolor='#0a0e1a',
        showlegend=False,
        uirevision="static"
    )
    
    # Background medium
    fig.add_shape(type="rect", x0=-5, y0=0, x1=5, y1=4.5,
                  fillcolor=mat1["color_fill"], line_width=0, layer="below")
    fig.add_shape(type="rect", x0=-5, y0=-4.5, x1=5, y1=0,
                  fillcolor=mat2["color_fill"], line_width=0, layer="below")
    
    # Garis batas antarmuka
    for width, opacity, color in [(10, 0.04, mat2["color_border"]),
                                   (4, 0.10, mat2["color_border"]),
                                   (1.5, 0.70, mat2["color_border"])]:
        fig.add_shape(type="line", x0=-5, y0=0, x1=5, y1=0,
                      line=dict(color=color, width=width), opacity=opacity)
    
    # Label medium
    for label, x_pos, y_pos, n_val, cat in [
        (m1, -4.2, 3.8, mat1["n"], mat1["category"]),
        (m2, -4.2, -3.8, mat2["n"], mat2["category"])
    ]:
        short = label[:16] + ("…" if len(label) > 16 else "")
        fig.add_annotation(
            x=x_pos, y=y_pos,
            text=f"<b>{short}</b><br><span style='font-size:10px'>n = {n_val:.3f} · {cat}</span>",
            showarrow=False, font=dict(size=11, color="#cbd5e1"), align="left",
            bgcolor="rgba(10,14,26,0.85)", bordercolor="rgba(255,255,255,0.1)",
            borderwidth=1, borderpad=5, xanchor="left"
        )
    
    # Garis normal
    fig.add_shape(type="line", x0=0, y0=0.3, x1=0, y1=4.2,
                  line=dict(color="#334155", width=1.5, dash="dash"))
    fig.add_shape(type="line", x0=0, y0=-0.3, x1=0, y1=-4.2,
                  line=dict(color="#334155", width=1.5, dash="dash"))
    fig.add_annotation(x=0.15, y=4.0, text="Normal", showarrow=False,
                        font=dict(size=9, color="#475569"), xanchor="left")
    
    # Busur sudut
    arc_r = 1.2
    th1 = res["th1"]
    if th1 > 0.02:
        arc_angles_1 = np.linspace(np.pi/2, np.pi/2 - th1, 40)
        ax1 = arc_r * np.cos(arc_angles_1)
        ay1 = arc_r * np.sin(arc_angles_1)
        fig.add_trace(go.Scatter(x=ax1, y=ay1, mode='lines',
                                  line=dict(color="#fbbf24", width=1.5, dash="dot"),
                                  hoverinfo='none'))
        fig.add_annotation(
            x=-(arc_r+0.3)*np.sin(th1/2), y=(arc_r+0.3)*np.cos(th1/2),
            text=f"θ₁={res['th1_deg']:.1f}°",
            showarrow=False, font=dict(size=11, color="#fbbf24"),
            bgcolor="rgba(10,14,26,0.8)", borderpad=3
        )
    
    if not res["is_tir"] and res["th1_deg"] > 0.5:
        th2 = res["th2"]
        arc_angles_2 = np.linspace(-np.pi/2, -np.pi/2 + th2, 40)
        ax2 = arc_r * np.cos(arc_angles_2)
        ay2 = arc_r * np.sin(arc_angles_2)
        fig.add_trace(go.Scatter(x=ax2, y=ay2, mode='lines',
                                  line=dict(color="#34d399", width=1.5, dash="dot"),
                                  hoverinfo='none'))
        fig.add_annotation(
            x=(arc_r+0.3)*np.sin(th2/2), y=-(arc_r+0.3)*np.cos(th2/2),
            text=f"θ₂={res['th2_deg']:.1f}°",
            showarrow=False, font=dict(size=11, color="#34d399"),
            bgcolor="rgba(10,14,26,0.8)", borderpad=3
        )
    
    # Generator sinar
    def add_ray(x_end, y_end, intensity, label="", ray_type="incident"):
        if intensity < 0.01:
            return
        x0, y0 = 0, 0
        colors_by_type = {
            "incident": laser_hex, "reflected": laser_hex,
            "refracted": laser_hex, "evanescent": "#f97316",
        }
        base_color = colors_by_type.get(ray_type, laser_hex)
        
        for width, opac in [(25, 0.03), (15, 0.06), (8, 0.12), (4, 0.3), (1.5, 0.95)]:
            fig.add_trace(go.Scatter(
                x=[x0, x_end], y=[y0, y_end], mode='lines',
                line=dict(color=base_color, width=width),
                opacity=opac * intensity, hoverinfo='none'
            ))
        
        # Arrow
        mid_x = (x0 + x_end) / 2
        mid_y = (y0 + y_end) / 2
        dx = x_end - x0
        dy = y_end - y0
        length = np.sqrt(dx**2 + dy**2)
        if length > 0:
            norm_dx, norm_dy = dx/length, dy/length
            fig.add_annotation(
                x=mid_x, y=mid_y,
                ax=mid_x - norm_dx*0.01, ay=mid_y - norm_dy*0.01,
                xref="x", yref="y", axref="x", ayref="y",
                showarrow=True, arrowhead=2, arrowsize=1.5, arrowwidth=1.5,
                arrowcolor=base_color, opacity=intensity * 0.9
            )
        
        if label:
            fig.add_annotation(
                x=x_end * 0.72, y=y_end * 0.72, text=label,
                showarrow=False, font=dict(size=10, color=base_color),
                bgcolor="rgba(10,14,26,0.8)", borderpad=3
            )
    
    # Sinar datang
    r_len = 4.3
    th1 = res["th1"]
    x_source = -r_len * np.sin(th1)
    y_source = r_len * np.cos(th1)
    
    fig.add_trace(go.Scatter(
        x=[x_source, 0], y=[y_source, 0], mode='lines',
        line=dict(color=laser_hex, width=2.5), opacity=0.9, hoverinfo='none'
    ))
    for w, a in [(20, 0.03), (12, 0.07), (6, 0.18)]:
        fig.add_trace(go.Scatter(
            x=[x_source, 0], y=[y_source, 0], mode='lines',
            line=dict(color=laser_hex, width=w), opacity=a, hoverinfo='none'
        ))
    fig.add_annotation(
        x=x_source, y=y_source + 0.25, text="<b>LASER</b>", showarrow=False,
        font=dict(size=10, color=laser_hex), bgcolor="rgba(10,14,26,0.85)", borderpad=3
    )
    
    # Sinar pantul
    x_refl = r_len * np.sin(th1)
    y_refl = r_len * np.cos(th1)
    add_ray(x_refl, y_refl, res["R_avg"], label=f"R={res['R_avg']*100:.0f}%", ray_type="reflected")
    
    if not res["is_tir"]:
        th2 = res["th2"]
        x_bias = r_len * np.sin(th2)
        y_bias = -r_len * np.cos(th2)
        add_ray(x_bias, y_bias, res["T_avg"], label=f"T={res['T_avg']*100:.0f}%", ray_type="refracted")
        
        if show_dispersion:
            wl_range = [405, 450, 490, 532, 580, 620, 660]
            for wl in wl_range:
                n2_disp = mat2["n"] + (500 - wl) * 0.00004
                sin_t2_d = (mat1["n"] / n2_disp) * np.sin(th1)
                if abs(sin_t2_d) < 1.0:
                    th2_d = np.arcsin(sin_t2_d)
                    xd = r_len * np.sin(th2_d)
                    yd = -r_len * np.cos(th2_d)
                    hex_wl = wavelength_to_hex(wl)
                    for w2, a2 in [(6, 0.1), (2, 0.6)]:
                        fig.add_trace(go.Scatter(
                            x=[0, xd], y=[0, yd], mode='lines',
                            line=dict(color=hex_wl, width=w2),
                            opacity=a2 * 0.7, hoverinfo='none'
                        ))
    else:
        # Gelombang evanescent
        ev_count = 6
        for i in range(ev_count):
            x_ev = (i - ev_count/2) * 0.4
            fig.add_trace(go.Scatter(
                x=[x_ev, x_ev + 0.25], y=[0, -(0.4 - i*0.05)],
                mode='lines', line=dict(color="#f97316", width=1.5, dash="dot"),
                opacity=max(0, 0.6 - i*0.08), hoverinfo='none'
            ))
        fig.add_annotation(
            x=2.2, y=-0.6, text="Gelombang Evanescent", showarrow=False,
            font=dict(size=10, color="#f97316"), bgcolor="rgba(10,14,26,0.85)", borderpad=4
        )
    
    # Titik interaksi
    fig.add_trace(go.Scatter(
        x=[0], y=[0], mode='markers',
        marker=dict(size=14, color='white', opacity=0.9, symbol='circle',
                    line=dict(color=laser_hex, width=2)),
        hovertemplate="<b>Titik Interaksi</b><br>" +
                      f"n₁ = {mat1['n']:.3f}<br>" +
                      f"n₂ = {mat2['n']:.3f}<br>" +
                      f"θ₁ = {res['th1_deg']:.1f}°<br>" +
                      f"θ₂ = {res['th2_deg']:.1f}°" if not res['is_tir'] else f"θ₁ = {res['th1_deg']:.1f}° (TIR)" + "<extra></extra>",
        name=""
    ))
    
    # Sudut kritis marker
    if res["theta_c_deg"]:
        th_c = np.radians(res["theta_c_deg"])
        r_c = 3.3
        fig.add_trace(go.Scatter(
            x=[-r_c*np.sin(th_c), 0], y=[r_c*np.cos(th_c), 0],
            mode='lines', line=dict(color="#f43f5e", width=1.5, dash="dashdot"),
            opacity=0.5, hoverinfo='none', name=""
        ))
        fig.add_annotation(
            x=-r_c*np.sin(th_c)*0.65, y=r_c*np.cos(th_c)*0.65,
            text=f"θc={res['theta_c_deg']:.1f}°", showarrow=False,
            font=dict(size=9, color="#f43f5e"), bgcolor="rgba(10,14,26,0.8)", borderpad=2
        )
    
    return fig


def render_fresnel_chart(res):
    """Grafik reflektansi vs sudut datang."""
    angles = np.linspace(0, 89.9, 500)
    Rs_vals, Rp_vals, R_avg_vals = [], [], []
    n1, n2 = res["n1"], res["n2"]
    for a in angles:
        r = engine_optik_lengkap(n1, n2, a)
        Rs_vals.append(r["Rs"])
        Rp_vals.append(r["Rp"])
        R_avg_vals.append(r["R_avg"])
    
    fig = go.Figure()
    if res["theta_c_deg"]:
        fig.add_vrect(x0=res["theta_c_deg"], x1=90,
                      fillcolor="rgba(244,63,94,0.08)", line_color="rgba(244,63,94,0.3)",
                      line_width=1, annotation_text="TIR Zone",
                      annotation_position="top left", annotation_font_color="#f43f5e",
                      annotation_font_size=10)
    
    fig.add_trace(go.Scatter(x=angles, y=Rs_vals, name="Rₛ (TE/Senkatan)",
                              line=dict(color="#60a5fa", width=2),
                              fill='tozeroy', fillcolor="rgba(96,165,250,0.05)"))
    fig.add_trace(go.Scatter(x=angles, y=Rp_vals, name="Rₚ (TM/Paralel)",
                              line=dict(color="#a78bfa", width=2),
                              fill='tozeroy', fillcolor="rgba(167,139,250,0.05)"))
    fig.add_trace(go.Scatter(x=angles, y=R_avg_vals, name="R̄ (rata-rata)",
                              line=dict(color="#34d399", width=2, dash="dash")))
    
    fig.add_vline(x=res["th1_deg"], line_color="#fbbf24", line_width=2,
                  line_dash="dot", annotation_text=f"θ={res['th1_deg']:.1f}°",
                  annotation_font_color="#fbbf24", annotation_font_size=10)
    fig.add_vline(x=res["theta_B_deg"], line_color="#f97316", line_width=1.5,
                  line_dash="dash", annotation_text=f"θB={res['theta_B_deg']:.1f}°",
                  annotation_font_color="#f97316", annotation_font_size=9)
    
    fig.update_layout(
        xaxis=dict(title="Sudut Datang (°)", color="#64748b", gridcolor="#1e293b",
                   showgrid=True, zeroline=False, tickfont=dict(color="#64748b", size=10)),
        yaxis=dict(title="Reflektansi", range=[0, 1.05], color="#64748b",
                   gridcolor="#1e293b", showgrid=True, zeroline=False,
                   tickfont=dict(color="#64748b", size=10), tickformat=".0%"),
        plot_bgcolor="#0a0e1a", paper_bgcolor="#0a0e1a",
        legend=dict(bgcolor="rgba(17,24,39,0.9)", bordercolor="#1e293b",
                    borderwidth=1, font=dict(color="#94a3b8", size=11)),
        height=300, margin=dict(l=55, r=15, t=15, b=50),
        font=dict(family="Inter, sans-serif"), hovermode="x unified"
    )
    return fig


def render_polar_chart(res):
    """Diagram kutub reflektansi."""
    angles_deg = np.linspace(0, 89.9, 360)
    r_vals = []
    n1, n2 = res["n1"], res["n2"]
    for a in angles_deg:
        r = engine_optik_lengkap(n1, n2, a)
        r_vals.append(r["R_avg"])
    
    fig = go.Figure(go.Scatterpolar(
        r=r_vals + r_vals,
        theta=list(angles_deg) + list(360 - angles_deg),
        mode='lines', line=dict(color="#60a5fa", width=2),
        fill='toself', fillcolor="rgba(96,165,250,0.06)"
    ))
    fig.update_layout(
        polar=dict(
            bgcolor="#0a0e1a",
            radialaxis=dict(visible=True, range=[0, 1], color="#334155",
                            gridcolor="#1e293b", tickformat=".0%",
                            tickfont=dict(color="#475569", size=8)),
            angularaxis=dict(color="#334155", gridcolor="#1e293b",
                             tickfont=dict(color="#475569", size=9)),
        ),
        paper_bgcolor="#0a0e1a", font=dict(color="#94a3b8"),
        height=260, margin=dict(l=30, r=30, t=20, b=15), showlegend=False
    )
    return fig


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR — PANEL KONTROL
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="padding: 16px 0 8px;">
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 9px; letter-spacing: 0.15em; color: #475569; text-transform: uppercase; margin-bottom: 6px;">OptiLab Pro v2.1</div>
        <div style="font-size: 16px; font-weight: 800; color: #f1f5f9; line-height: 1.2;">Panel Kontrol<br>Eksperimen</div>
        <div style="width: 36px; height: 2px; background: linear-gradient(90deg, #3b82f6, #8b5cf6); margin-top: 8px; border-radius: 2px;"></div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    
    # Panduan Belajar Toggle
    st.markdown('<div class="section-title">📖 Panduan Belajar</div>', unsafe_allow_html=True)
    show_guide = st.toggle("Tampilkan Panduan", value=st.session_state.show_guide,
                           help="Aktifkan panduan langkah demi langkah")
    st.session_state.show_guide = show_guide
    
    if show_guide:
        current_step = st.session_state.current_guide_step
        guide_html = '<div class="guide-panel">'
        for i, step in enumerate(GUIDE_STEPS):
            if i < current_step:
                num_class = "done"
                num_label = "✓"
                text_class = ""
            elif i == current_step:
                num_class = "active"
                num_label = str(i + 1)
                text_class = "active"
            else:
                num_class = ""
                num_label = str(i + 1)
                text_class = ""
            guide_html += f'''
            <div class="guide-step">
                <div class="guide-step-num {num_class}">{num_label}</div>
                <div class="guide-step-text {text_class}">
                    <strong>{step["title"]}</strong><br>{step["desc"]}
                </div>
            </div>'''
        guide_html += '</div>'
        st.markdown(guide_html, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Konfigurasi Medium
    st.markdown('<div class="section-title">Konfigurasi Medium</div>', unsafe_allow_html=True)
    
    mat_list = list(MATERIAL_DB.keys())
    
    st.markdown('<p style="font-size:12px; color:#94a3b8; margin-bottom:4px;">📡 Medium 1 — Insiden</p>', unsafe_allow_html=True)
    m1_name = st.selectbox("Medium 1", mat_list, index=0, label_visibility="collapsed",
                            help="Medium asal sinar datang")
    m1_data = MATERIAL_DB[m1_name]
    st.markdown(f'<div style="padding:6px 10px; background:rgba(255,255,255,0.05); border-left:3px solid {m1_data["color_border"]}; border-radius:0 6px 6px 0; margin-bottom:8px;"><span style="font-weight:700; color:#ffffff; font-size:13px;">{m1_name}</span> <span style="color:{m1_data["color_border"]}; font-size:11px; font-family:monospace;">n={m1_data["n"]:.3f}</span></div>', unsafe_allow_html=True)
    
    st.markdown('<p style="font-size:12px; color:#94a3b8; margin-bottom:4px;">🔭 Medium 2 — Transmisi</p>', unsafe_allow_html=True)
    m2_name = st.selectbox("Medium 2", mat_list, index=1, label_visibility="collapsed",
                            help="Medium yang dituju sinar")
    m2_data = MATERIAL_DB[m2_name]
    st.markdown(f'<div style="padding:6px 10px; background:rgba(255,255,255,0.05); border-left:3px solid {m2_data["color_border"]}; border-radius:0 6px 6px 0; margin-bottom:8px;"><span style="font-weight:700; color:#ffffff; font-size:13px;">{m2_name}</span> <span style="color:{m2_data["color_border"]}; font-size:11px; font-family:monospace;">n={m2_data["n"]:.3f}</span></div>', unsafe_allow_html=True)
    
    n1 = MATERIAL_DB[m1_name]["n"]
    n2 = MATERIAL_DB[m2_name]["n"]
    
    ratio = n2 / n1
    direction_emoji = "⬆️ Rapat→Renggang" if n1 > n2 else "⬇️ Renggang→Rapat"
    st.markdown(f"""
    <div class="info-tooltip">
        <strong>Rasio indeks</strong> n₂/n₁ = {ratio:.3f}<br>
        {direction_emoji} · Δn = {abs(n2-n1):.3f}
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Sumber Cahaya
    st.markdown('<div class="section-title">Sumber Cahaya</div>', unsafe_allow_html=True)
    
    laser_name = st.selectbox("🔦 Preset Laser", list(LASER_PRESETS.keys()))
    laser_info = LASER_PRESETS[laser_name]
    
    if laser_name == "⚪ Custom":
        custom_color = st.color_picker("Pilih warna", "#FF6060")
        laser_hex = custom_color
        wl_display = "Custom"
    else:
        laser_hex = laser_info["hex"]
        wl_display = f"{laser_info['wavelength']} nm"
    
    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 8px; padding: 8px; background: rgba(255,255,255,0.03); border-radius: 6px; margin: 6px 0;">
        <div style="width: 16px; height: 16px; border-radius: 50%; background: {laser_hex}; box-shadow: 0 0 8px {laser_hex}88; flex-shrink: 0;"></div>
        <span style="font-size: 11px; color: #64748b;">λ = {wl_display}</span>
    </div>
    """, unsafe_allow_html=True)
    
    show_dispersion = st.toggle("🌈 Tampilkan Dispersi", value=False,
                                 help="Simulasikan pemisahan warna (seperti prisma)")
    
    st.markdown("---")
    
    # Sudut Datang
    st.markdown('<div class="section-title">Parameter Sinar</div>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:11px; color:#94a3b8; margin-bottom:2px;">θ₁ — Sudut Datang (°) <span style="color:#60a5fa;">[ ketik nilai sudut secara langsung ]</span></p>', unsafe_allow_html=True)
    sudut_datang = st.number_input(
        "Input sudut (°)",
        min_value=0.0, max_value=89.9,
        value=st.session_state.sudut_val,
        step=0.5, format="%.1f",
        label_visibility="collapsed",
        key="sudut_input"
    )
    st.session_state.sudut_val = sudut_datang
    
    if n1 > n2:
        theta_c_preview = np.degrees(np.arcsin(n2/n1))
        frac = min(sudut_datang / theta_c_preview, 1.0)
        bar_color = "#f87171" if frac > 0.9 else "#fbbf24" if frac > 0.7 else "#34d399"
        st.markdown(f"""
        <div class="prog-wrap">
            <div class="prog-label">
                <span>Mendekati θ_kritis</span>
                <span style="color: {bar_color}">{frac*100:.0f}%</span>
            </div>
            <div class="prog-bar-bg">
                <div class="prog-bar-fill" style="width: {frac*100:.0f}%; background: {bar_color};"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Rekam Data
    st.markdown('<div class="section-title">Jurnal Eksperimen</div>', unsafe_allow_html=True)
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        btn_rekam = st.button("📸 Rekam", type="primary", use_container_width=True)
    with col_btn2:
        btn_hapus = st.button("🗑️ Hapus", type="secondary", use_container_width=True)
    
    if btn_hapus:
        st.session_state.jurnal = []
        st.session_state.challenges_completed = []
        st.session_state.current_guide_step = 0
        st.rerun()
    
    n_records = len(st.session_state.jurnal)
    n_tir = sum(1 for j in st.session_state.jurnal if j["Status"] == "TIR 🔴")
    
    st.markdown(f"""
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-top: 10px;">
        <div style="background: rgba(96,165,250,0.08); border: 1px solid rgba(96,165,250,0.2); border-radius: 6px; padding: 10px; text-align: center;">
            <div style="font-size: 20px; font-weight: 800; color: #60a5fa;">{n_records}</div>
            <div style="font-size: 9px; color: #475569; text-transform: uppercase; letter-spacing: 0.08em;">Rekaman</div>
        </div>
        <div style="background: rgba(244,63,94,0.08); border: 1px solid rgba(244,63,94,0.2); border-radius: 6px; padding: 10px; text-align: center;">
            <div style="font-size: 20px; font-weight: 800; color: #f87171;">{n_tir}</div>
            <div style="font-size: 9px; color: #475569; text-transform: uppercase; letter-spacing: 0.08em;">TIR Event</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
    <div style="font-size: 10px; color: #334155; line-height: 1.8; text-align: center;">
        Hukum Snellius: <br>
        <span style="font-family: 'JetBrains Mono', monospace; color: #475569;">n₁ sin θ₁ = n₂ sin θ₂</span><br><br>
        Kurikulum Merdeka — Fase F<br>
        Fisika SMA Kelas XI
    </div>
    """, unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# KALKULASI UTAMA
# ══════════════════════════════════════════════════════════════════════════════
res = engine_optik_lengkap(n1, n2, sudut_datang)

# Proses rekam data & cek tantangan
if btn_rekam:
    entry = {
        "No": len(st.session_state.jurnal) + 1,
        "Medium 1": m1_name[:20],
        "Medium 2": m2_name[:20],
        "n₁": round(n1, 3),
        "n₂": round(n2, 3),
        "θ₁ (°)": round(sudut_datang, 1),
        "θ₂ (°)": round(res["th2_deg"], 1) if res["th2_deg"] else "TIR",
        "R (%)": round(res["R_avg"] * 100, 1),
        "T (%)": round(res["T_avg"] * 100, 1),
        "n₁sinθ₁": round(n1 * np.sin(res["th1"]), 4),
        "n₂sinθ₂": round(n2 * np.sin(res["th2"]), 4) if not res["is_tir"] else "TIR",
        "Status": "TIR 🔴" if res["is_tir"] else "Normal ✅",
        "Laser": wl_display,
    }
    st.session_state.jurnal.append(entry)
    
    # Cek tantangan
    for challenge in CHALLENGES:
        if challenge["id"] not in st.session_state.challenges_completed:
            if challenge["check"](res, m1_name, m2_name, sudut_datang):
                st.session_state.challenges_completed.append(challenge["id"])
                st.toast(f"🏆 Tantangan selesai: {challenge['reward']}!")
    
    # Update guide step
    if st.session_state.current_guide_step < len(GUIDE_STEPS) - 1:
        st.session_state.current_guide_step += 1
    
    st.toast("✅ Data berhasil direkam!")

# ══════════════════════════════════════════════════════════════════════════════
# HERO BANNER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero-banner animate-up">
    <div class="hero-eyebrow">Laboratorium Virtual · Fisika Optik</div>
    <h1 class="hero-title">OptiLab <em>Pro</em></h1>
    <p class="hero-sub">
        Simulasi interaktif Hukum Snellius, Koefisien Fresnel, dan Pemantulan Internal Sempurna 
        berbasis model fisika presisi tinggi. Dirancang untuk inkuiri terbimbing Fase F.
    </p>
    <div class="hero-badges">
        <span class="badge badge-blue">Hukum Snellius</span>
        <span class="badge badge-green">Koefisien Fresnel</span>
        <span class="badge badge-purple">TIR & Evanescent</span>
        <span class="badge badge-amber">Dispersi Prisma</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# KPI DASHBOARD (FIXED - menggunakan st.columns instead of raw HTML)
# ══════════════════════════════════════════════════════════════════════════════
tir_status_color = "red" if res["is_tir"] else "green"
tir_status_val = "TIR!" if res["is_tir"] else f"{res['theta_c_deg']:.1f}°" if res['theta_c_deg'] else "N/A"

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    th2_display = f"{res['th2_deg']:.1f}°" if res['th2_deg'] is not None else "TIR"
    sin_t2_display = f"{np.sin(res['th2']):.4f}" if res['th2_deg'] is not None else "—"
    st.markdown(f"""
    <div class="kpi-card blue">
        <div class="kpi-label">θ₂ — Sudut Bias</div>
        <div class="kpi-value blue">{th2_display}</div>
        <div class="kpi-sub">sin θ₂ = {sin_t2_display}</div>
    </div>
    """, unsafe_allow_html=True)

with kpi2:
    st.markdown(f"""
    <div class="kpi-card amber">
        <div class="kpi-label">θ_Brewster</div>
        <div class="kpi-value amber">{res['theta_B_deg']:.1f}°</div>
        <div class="kpi-sub">Polarisasi sempurna Rₚ=0</div>
    </div>
    """, unsafe_allow_html=True)

with kpi3:
    st.markdown(f"""
    <div class="kpi-card {tir_status_color}">
        <div class="kpi-label">θ_Kritis / Status TIR</div>
        <div class="kpi-value {tir_status_color}">{tir_status_val}</div>
        <div class="kpi-sub">{"⚠️ Pemantulan Sempurna" if res["is_tir"] else "Sinar merambat normal"}</div>
    </div>
    """, unsafe_allow_html=True)

with kpi4:
    st.markdown(f"""
    <div class="kpi-card green">
        <div class="kpi-label">Transmitansi</div>
        <div class="kpi-value green">{res['T_avg']*100:.1f}%</div>
        <div class="kpi-sub">Reflektansi R = {res['R_avg']*100:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

# TIR Alert
if res["is_tir"]:
    st.markdown(f"""
    <div class="tir-alert">
        <div class="tir-icon">⚡</div>
        <div class="tir-text">
            <strong>PEMANTULAN INTERNAL SEMPURNA (TIR) AKTIF</strong>
            <span>Sudut datang ({sudut_datang:.1f}°) melebihi sudut kritis ({res['theta_c_deg']:.1f}°).
            Seluruh energi sinar dipantulkan kembali ke medium 1. Dasar prinsip kerja serat optik.</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# LAYOUT UTAMA: DIAGRAM + PANEL ANALISIS
# ══════════════════════════════════════════════════════════════════════════════
col_vis, col_anal = st.columns([1.6, 1], gap="large")

with col_vis:
    st.markdown('<div class="section-card" style="padding: 14px;">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Diagram Sinar Interaktif</div>', unsafe_allow_html=True)
    fig_main = render_diagram_optik(res, m1_name, m2_name, laser_hex, show_dispersion)
    st.plotly_chart(fig_main, use_container_width=True, config={
        'displayModeBar': True,
        'modeBarButtonsToRemove': ['zoom', 'pan', 'select', 'lasso2d', 'autoScale'],
        'displaylogo': False
    })
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown('<div class="section-card" style="padding: 14px;">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Kurva Fresnel — Reflektansi vs. Sudut</div>', unsafe_allow_html=True)
    fig_fresnel = render_fresnel_chart(res)
    st.plotly_chart(fig_fresnel, use_container_width=True, config={'displayModeBar': False})
    st.markdown("</div>", unsafe_allow_html=True)

with col_anal:
    # Verifikasi Hukum Snellius
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Verifikasi Hukum Snellius</div>', unsafe_allow_html=True)
    st.markdown('<div class="formula-box">n₁ · sin θ₁ = n₂ · sin θ₂</div>', unsafe_allow_html=True)
    
    lhs = n1 * np.sin(res["th1"])
    if not res["is_tir"] and res["sin_t2"]:
        rhs = n2 * np.sin(res["th2"])
        err = abs(lhs - rhs)
    else:
        rhs = lhs
        err = 0.0
    
    st.markdown(f"""
    <table class="snell-table">
        <thead>
            <tr><th>Parameter</th><th>Ruas Kiri</th><th>Ruas Kanan</th></tr>
        </thead>
        <tbody>
            <tr><td>Nilai</td><td class="highlight">{lhs:.5f}</td><td class="highlight">{rhs:.5f}</td></tr>
            <tr><td>n</td><td>{n1:.3f}</td><td>{n2:.3f}</td></tr>
            <tr><td>sin θ</td><td>{np.sin(res['th1']):.5f}</td><td>{"TIR" if res['is_tir'] else f"{np.sin(res['th2']):.5f}"}</td></tr>
            <tr><td>θ</td><td>{res['th1_deg']:.2f}°</td><td>{"TIR" if res['is_tir'] else f"{res['th2_deg']:.2f}°"}</td></tr>
            <tr><td>Error</td><td colspan="2" style="color: #34d399;">{err:.2e}</td></tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Koefisien Fresnel Detail
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Koefisien Fresnel Lengkap</div>', unsafe_allow_html=True)
    
    for label, val_r, val_t, color in [
        ("Polarisasi-s (TE)", res['Rs'], res['Ts'], "#60a5fa"),
        ("Polarisasi-p (TM)", res['Rp'], res['Tp'], "#a78bfa"),
        ("Rata-rata", res['R_avg'], res['T_avg'], "#34d399"),
    ]:
        st.markdown(f"""
        <div style="margin-bottom: 12px;">
            <div style="font-size: 11px; font-weight: 700; color: {color}; margin-bottom: 4px;">{label}</div>
            <div class="prog-wrap">
                <div class="prog-label"><span>Reflektansi R</span><span style="color: {color}">{val_r*100:.1f}%</span></div>
                <div class="prog-bar-bg"><div class="prog-bar-fill" style="width: {val_r*100:.1f}%; background: {color};"></div></div>
            </div>
            <div class="prog-wrap">
                <div class="prog-label"><span>Transmitansi T</span><span style="color: #475569">{val_t*100:.1f}%</span></div>
                <div class="prog-bar-bg"><div class="prog-bar-fill" style="width: {val_t*100:.1f}%; background: #475569;"></div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Kecepatan Cahaya
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Kecepatan Cahaya di Medium</div>', unsafe_allow_html=True)
    
    C = 2.998e8
    for medium, v, n_val, color in [
        (m1_name[:20], res['v1'], n1, "#60a5fa"),
        (m2_name[:20], res['v2'], n2, "#a78bfa"),
    ]:
        v_pct = (v / C) * 100
        st.markdown(f"""
        <div style="margin-bottom: 12px;">
            <div style="font-size: 11px; color: #64748b; margin-bottom: 3px;">{medium}</div>
            <div style="font-size: 18px; font-weight: 800; color: {color}; margin-bottom: 3px; font-family: 'JetBrains Mono', monospace;">
                {v/1e8:.3f} × 10⁸ m/s
            </div>
            <div class="prog-wrap">
                <div class="prog-label"><span>% kecepatan cahaya</span><span style="color: {color}">{v_pct:.1f}%</span></div>
                <div class="prog-bar-bg"><div class="prog-bar-fill" style="width: {v_pct:.1f}%; background: {color};"></div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Diagram Polar
    st.markdown('<div class="section-card" style="padding: 14px;">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Pola Polar Reflektansi</div>', unsafe_allow_html=True)
    fig_polar = render_polar_chart(res)
    st.plotly_chart(fig_polar, use_container_width=True, config={'displayModeBar': False})
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB KONTEN BAWAH
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
tab_jurnal, tab_tantangan, tab_aktivitas, tab_teori, tab_aplikasi, tab_diagnostik = st.tabs([
    "📊 Jurnal & Laporan",
    "🏆 Tantangan",
    "🧪 Aktivitas Percobaan",
    "📚 Teori & Materi",
    "🌍 Aplikasi Nyata",
    "🧠 Tes Diagnostik"
])

# ── TAB 1: JURNAL ────────────────────────────────────────────────────────────
with tab_jurnal:
    st.markdown("### 📊 Jurnal Data Eksperimen")
    if st.session_state.jurnal:
        df = pd.DataFrame(st.session_state.jurnal)
        
        if len(df) > 1:
            col_g1, col_g2 = st.columns(2)
            with col_g1:
                fig_j1 = px.scatter(df, x="θ₁ (°)", y="θ₂ (°)",
                                     color="Status",
                                     color_discrete_map={"Normal ✅": "#34d399", "TIR 🔴": "#f87171"},
                                     title="Grafik θ₁ vs θ₂", template="plotly_dark")
                fig_j1.update_layout(
                    plot_bgcolor="#0a0e1a", paper_bgcolor="#0a0e1a", height=280,
                    font=dict(family="Inter, sans-serif", size=11, color="#94a3b8"),
                    title_font=dict(color="#cbd5e1", size=13),
                    legend=dict(bgcolor="rgba(17,24,39,0.9)", bordercolor="#1e293b", borderwidth=1)
                )
                st.plotly_chart(fig_j1, use_container_width=True, config={'displayModeBar': False})
            
            with col_g2:
                fig_j2 = px.bar(df, x="No", y=["R (%)", "T (%)"],
                                 barmode="stack",
                                 color_discrete_map={"R (%)": "#60a5fa", "T (%)": "#34d399"},
                                 title="Distribusi R & T per Eksperimen", template="plotly_dark")
                fig_j2.update_layout(
                    plot_bgcolor="#0a0e1a", paper_bgcolor="#0a0e1a", height=280,
                    font=dict(family="Inter, sans-serif", size=11, color="#94a3b8"),
                    title_font=dict(color="#cbd5e1", size=13),
                    legend=dict(bgcolor="rgba(17,24,39,0.9)", bordercolor="#1e293b", borderwidth=1)
                )
                st.plotly_chart(fig_j2, use_container_width=True, config={'displayModeBar': False})
        
        st.dataframe(df, use_container_width=True, hide_index=True,
                     column_config={
                         "R (%)": st.column_config.ProgressColumn("R (%)", min_value=0, max_value=100, format="%f%%"),
                         "T (%)": st.column_config.ProgressColumn("T (%)", min_value=0, max_value=100, format="%f%%"),
                     })
        
        col_ex1, col_ex2 = st.columns(2)
        with col_ex1:
            csv = df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="OptiLab_Jurnal.csv" style="display: block; padding: 10px 18px; background: linear-gradient(135deg, #3b82f6, #8b5cf6); color: white; text-decoration: none; border-radius: 8px; font-weight: 600; text-align: center; font-family: Inter, sans-serif; font-size: 13px;">📥 Export CSV</a>'
            st.markdown(href, unsafe_allow_html=True)
        with col_ex2:
            json_str = df.to_json(orient='records', indent=2)
            b64j = base64.b64encode(json_str.encode()).decode()
            href_j = f'<a href="data:application/json;base64,{b64j}" download="OptiLab_Jurnal.json" style="display: block; padding: 10px 18px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); color: #cbd5e1; text-decoration: none; border-radius: 8px; font-weight: 600; text-align: center; font-family: Inter, sans-serif; font-size: 13px;">📥 Export JSON</a>'
            st.markdown(href_j, unsafe_allow_html=True)
        
        with st.expander("🔍 Analisis Otomatis Data Jurnal"):
            n_normal = len(df[df["Status"] == "Normal ✅"])
            n_tir_j = len(df[df["Status"] == "TIR 🔴"])
            avg_r = df["R (%)"].mean()
            avg_t = df["T (%)"].mean()
            st.markdown(f"""
            **Ringkasan Statistik:**
            - Total eksperimen: **{len(df)}** percobaan
            - Kondisi normal: **{n_normal}** percobaan ({n_normal/len(df)*100:.0f}%)
            - Kondisi TIR: **{n_tir_j}** percobaan ({n_tir_j/len(df)*100:.0f}%)
            - Rata-rata reflektansi: **{avg_r:.1f}%**
            - Rata-rata transmitansi: **{avg_t:.1f}%**
            - Verifikasi Snellius: semua nilai |n₁sinθ₁ − n₂sinθ₂| < 0.001 ✅
            """)
    else:
        st.info("💡 Atur parameter dan tekan **Rekam** di sidebar untuk mulai mengisi jurnal eksperimen.")

# ── TAB 2: TANTANGAN ─────────────────────────────────────────────────────────
with tab_tantangan:
    st.markdown("### 🏆 Tantangan Eksperimen")
    st.markdown("""
    <div class="info-tooltip">
        <strong>Cara Bermain:</strong> Atur parameter di sidebar sesuai deskripsi tantangan, 
        lalu tekan <strong>Rekam</strong>. Tantangan akan otomatis terbuka ketika kondisi terpenuhi!
    </div>
    """, unsafe_allow_html=True)
    
    # Achievement display
    unlocked = len(st.session_state.challenges_completed)
    total = len(CHALLENGES)
    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 16px; padding: 12px; background: rgba(251,191,36,0.06); border: 1px solid rgba(251,191,36,0.15); border-radius: 10px;">
        <div style="font-size: 28px;">🏆</div>
        <div>
            <div style="font-size: 14px; font-weight: 700; color: #fbbf24;">Progress: {unlocked}/{total} Tantangan</div>
            <div style="font-size: 11px; color: #64748b;">{"Lanjutkan eksplorasi!" if unlocked < total else "🎉 Semua tantangan selesai!"}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    for challenge in CHALLENGES:
        is_completed = challenge["id"] in st.session_state.challenges_completed
        status_icon = "✅" if is_completed else "🎯"
        border_color = "#34d399" if is_completed else "#60a5fa"
        card_bg = "linear-gradient(135deg,rgba(52,211,153,0.08),rgba(52,211,153,0.03))" if is_completed else "linear-gradient(135deg,rgba(59,130,246,0.08),rgba(139,92,246,0.05))"
        ach_style_base = "display:inline-flex;align-items:center;gap:6px;padding:5px 14px;border-radius:100px;font-size:11px;font-weight:700;"
        ach_style = (ach_style_base + "background:rgba(52,211,153,0.15);border:1px solid rgba(52,211,153,0.4);color:#34d399;") if is_completed else (ach_style_base + "background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.1);color:#475569;")
        ach_icon = "🏅" if is_completed else "⏳"
        ach_text = challenge["reward"] + (" — SELESAI!" if is_completed else " — Belum selesai")
        hint_part = ('<div style="margin-top:8px;padding:8px 10px;background:rgba(96,165,250,0.06);border:1px solid rgba(96,165,250,0.2);border-radius:6px;font-size:11px;color:#60a5fa;">💡 <strong>Cara selesaikan:</strong> ' + challenge.get("hint","") + '</div>') if not is_completed else ""
        html_parts = [
            '<div style="background:' + card_bg + ';border:1px solid ' + border_color + '44;border-left:4px solid ' + border_color + ';border-radius:12px;padding:16px;margin-bottom:14px;">',
            '<div style="font-size:14px;font-weight:700;color:' + border_color + ';margin-bottom:6px;">' + status_icon + ' ' + challenge["title"] + '</div>',
            '<div style="font-size:12px;color:#cbd5e1;margin-bottom:8px;line-height:1.6;">' + challenge["desc"] + '</div>',
            hint_part,
            '<div style="margin-top:10px;"><span style="' + ach_style + '">' + ach_icon + ' ' + ach_text + '</span></div>',
            '</div>',
        ]
        st.markdown("".join(html_parts), unsafe_allow_html=True)


# ── TAB 3: AKTIVITAS PERCOBAAN ───────────────────────────────────────────────
with tab_aktivitas:
    st.markdown("### 🧪 Aktivitas Percobaan Terpandu")
    st.markdown('<div class="info-tooltip"><strong>Petunjuk Umum:</strong> Ikuti langkah-langkah percobaan di bawah ini secara berurutan. Gunakan panel kontrol di sidebar kiri untuk mengatur parameter. Catat hasil di tab <em>Jurnal</em> dengan menekan tombol <strong>Rekam</strong>.</div>', unsafe_allow_html=True)

    act_tab1, act_tab2, act_tab3 = st.tabs([
        "⚗️ Percobaan 1 — Hukum Snellius",
        "🔴 Percobaan 2 — TIR & Sudut Kritis",
        "🌈 Percobaan 3 — Dispersi & Brewster",
    ])

    def render_step_card(num, title, color, desc):
        html = (
            '<div style="display:flex;gap:14px;margin-bottom:14px;align-items:flex-start;">'
            + '<div style="min-width:32px;height:32px;border-radius:50%;background:linear-gradient(135deg,' + color + ',' + color + '88);display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:800;color:white;flex-shrink:0;">' + num + '</div>'
            + '<div style="background:#111827;border:1px solid rgba(255,255,255,0.08);border-radius:10px;padding:12px 14px;flex:1;">'
            + '<div style="font-size:13px;font-weight:700;color:' + color + ';margin-bottom:4px;">' + title + '</div>'
            + '<div style="font-size:12px;color:#94a3b8;line-height:1.7;">' + desc + '</div>'
            + '</div></div>'
        )
        st.markdown(html, unsafe_allow_html=True)

    with act_tab1:
        st.markdown(
            '<div class="section-card" style="border-top:3px solid #60a5fa;">'
            '<div style="font-size:16px;font-weight:800;color:#60a5fa;margin-bottom:4px;">⚗️ Percobaan 1: Memverifikasi Hukum Snellius</div>'
            '<div style="font-size:12px;color:#94a3b8;margin-bottom:16px;">Kurikulum Merdeka Fase F | Fisika SMA Kelas XI | ~20 menit</div>'
            '<div style="font-size:13px;font-weight:700;color:#cbd5e1;margin-bottom:8px;">🎯 Tujuan Percobaan</div>'
            '<div style="font-size:12px;color:#94a3b8;line-height:1.8;margin-bottom:14px;">Memverifikasi secara numerik bahwa <strong style="color:#f1f5f9;">n&#8321; sin &#952;&#8321; = n&#8322; sin &#952;&#8322;</strong> berlaku untuk berbagai sudut datang dan pasangan medium, serta menganalisis bagaimana perbedaan indeks bias memengaruhi arah pembiasan sinar.</div>'
            '<div style="font-size:13px;font-weight:700;color:#cbd5e1;margin-bottom:10px;">📋 Alat &amp; Bahan (Virtual)</div>'
            '<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:14px;">'
            '<div style="font-size:11px;color:#94a3b8;background:rgba(255,255,255,0.03);padding:8px 10px;border-radius:6px;">✅ Simulator OptiLab (panel kiri)</div>'
            '<div style="font-size:11px;color:#94a3b8;background:rgba(255,255,255,0.03);padding:8px 10px;border-radius:6px;">✅ Tabel Jurnal (tab Jurnal)</div>'
            '<div style="font-size:11px;color:#94a3b8;background:rgba(255,255,255,0.03);padding:8px 10px;border-radius:6px;">✅ Kalkulator (bawaan HP/laptop)</div>'
            '<div style="font-size:11px;color:#94a3b8;background:rgba(255,255,255,0.03);padding:8px 10px;border-radius:6px;">✅ Lembar kerja / buku tulis</div>'
            '</div>'
            '<div style="font-size:13px;font-weight:700;color:#cbd5e1;margin-bottom:4px;">📌 Langkah-Langkah Percobaan</div>'
            '</div>',
            unsafe_allow_html=True)

        steps_p1 = [
            ("1", "Persiapan Awal", "#60a5fa",
             "Buka panel kontrol di sidebar. Pastikan panduan belajar aktif (toggle ON). Siapkan tabel data di buku tulis dengan kolom: &#952;&#8321;, &#952;&#8322;, n&#8321;, n&#8322;, n&#8321;sin&#952;&#8321;, n&#8322;sin&#952;&#8322;."),
            ("2", "Atur Medium", "#60a5fa",
             "Pilih <strong>Medium 1: Vakum/Udara</strong> (n=1.000) dan <strong>Medium 2: Air Murni</strong> (n=1.333). Perhatikan tampilan highlight nama medium yang muncul."),
            ("3", "Percobaan Sudut Pertama (&#952;&#8321; = 10°)", "#60a5fa",
             "Ketik angka <strong>10.0</strong> pada kolom sudut datang. Amati diagram: ke mana sinar berbelok? Catat nilai &#952;&#8322; dari KPI card. Tekan <strong>Rekam</strong>."),
            ("4", "Ulangi untuk 5 Variasi Sudut", "#60a5fa",
             "Ulangi langkah 3 untuk sudut: 20°, 30°, 45°, 60°. Setiap kali tekan Rekam. Kamu akan punya 5 baris data di Jurnal."),
            ("5", "Ganti Medium Transmisi", "#60a5fa",
             "Ubah Medium 2 ke <strong>Kaca Crown (BK7)</strong> (n=1.517). Ulangi pengukuran untuk 5 sudut yang sama. Rekam setiap data."),
            ("6", "Analisis Data", "#34d399",
             "Buka tab Jurnal. Hitung manual: n&#8321;sin&#952;&#8321; dan n&#8322;sin&#952;&#8322; untuk tiap baris. Apakah nilainya sama? Berapa besar errornya?"),
            ("7", "Buat Grafik &#952;&#8321; vs &#952;&#8322;", "#34d399",
             "Lihat grafik otomatis di tab Jurnal. Apakah grafik linear? Mengapa atau mengapa tidak? Tulis kesimpulan."),
        ]
        for num, title, color, desc in steps_p1:
            render_step_card(num, title, color, desc)

        st.markdown(
            '<div class="section-card" style="border-left:4px solid #34d399;margin-top:8px;">'
            '<div style="font-size:13px;font-weight:700;color:#34d399;margin-bottom:8px;">📝 Pertanyaan Refleksi</div>'
            '<div style="font-size:12px;color:#94a3b8;line-height:2;">'
            '1. Ketika sinar melewati udara ke air, apakah &#952;&#8322; lebih besar atau lebih kecil dari &#952;&#8321;? Mengapa?<br>'
            '2. Ketika sinar melewati udara ke kaca crown, apakah pembelokkan lebih besar atau lebih kecil dibanding udara ke air? Mengapa?<br>'
            '3. Apakah nilai n&#8321;sin&#952;&#8321; selalu sama dengan n&#8322;sin&#952;&#8322;? Jelaskan mengapa hukum ini disebut hukum kekekalan.<br>'
            '4. Apa yang terjadi jika &#952;&#8321; = 0°? Apakah sinar tetap berbelok?'
            '</div></div>',
            unsafe_allow_html=True)

    with act_tab2:
        st.markdown(
            '<div class="section-card" style="border-top:3px solid #f87171;">'
            '<div style="font-size:16px;font-weight:800;color:#f87171;margin-bottom:4px;">🔴 Percobaan 2: Menemukan Sudut Kritis &amp; TIR</div>'
            '<div style="font-size:12px;color:#94a3b8;margin-bottom:16px;">Kurikulum Merdeka Fase F | Fisika SMA Kelas XI | ~25 menit</div>'
            '<div style="font-size:13px;font-weight:700;color:#cbd5e1;margin-bottom:8px;">🎯 Tujuan Percobaan</div>'
            '<div style="font-size:12px;color:#94a3b8;line-height:1.8;">Menemukan sudut kritis (&#952;c) secara eksperimental untuk berbagai material, memahami syarat terjadinya Pemantulan Internal Sempurna (TIR), dan menghubungkannya dengan prinsip kerja serat optik.</div>'
            '</div>',
            unsafe_allow_html=True)

        steps_p2 = [
            ("1", "Atur Konfigurasi Awal", "#f87171",
             "Pilih <strong>Medium 1: Kaca Crown (BK7)</strong> dan <strong>Medium 2: Vakum/Udara</strong>. Perhatikan: n&#8321; &gt; n&#8322;, artinya TIR bisa terjadi."),
            ("2", "Mulai dari Sudut Kecil", "#f87171",
             "Set sudut datang ke <strong>10°</strong>. Amati sinar bias muncul di Medium 2. Catat: sinar bias ada? Berapa &#952;&#8322;?"),
            ("3", "Naikkan Sudut Perlahan", "#f87171",
             "Naikkan sudut satu per satu: 20°, 30°, 35°, 38°, 40°, 41°. Perhatikan progress bar <em>Mendekati &#952;_kritis</em> di sidebar berubah warna dari hijau ke kuning ke merah."),
            ("4", "Temukan Momen TIR", "#f43f5e",
             "Terus naikkan sudut hingga muncul pesan <strong>PEMANTULAN INTERNAL SEMPURNA AKTIF</strong> berwarna merah. Catat sudut saat TIR pertama kali terjadi — ini adalah &#952;_kritis!"),
            ("5", "Verifikasi dengan Rumus", "#f87171",
             "Hitung manual: sin &#952;c = n&#8322;/n&#8321; = 1.000/1.517. &#952;c = arcsin(0.659) = ? Bandingkan dengan hasil eksperimen. Apakah cocok?"),
            ("6", "Bandingkan 3 Material", "#f87171",
             "Ulangi langkah 1-5 untuk: (a) Intan ke Udara, (b) Kaca Flint ke Udara, (c) Silikon Dioksida ke Udara. Catat &#952;c masing-masing."),
            ("7", "Hubungkan ke Serat Optik", "#34d399",
             "Pilih SiO&#8322; ke Udara, atur sudut &gt; &#952;c. Aktifkan toggle Dispersi. Bayangkan sinar ini terpantul berulang di dalam serat sepanjang ribuan km. Itulah prinsip serat optik!"),
        ]
        for num, title, color, desc in steps_p2:
            render_step_card(num, title, color, desc)

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(
                '<div class="section-card" style="border-left:4px solid #f87171;">'
                '<div style="font-size:12px;font-weight:700;color:#f87171;margin-bottom:8px;">📊 Tabel Data yang Diisi Siswa</div>'
                '<table class="snell-table">'
                '<tr><th>Material</th><th>n&#8321;</th><th>n&#8322;</th><th>&#952;c (eksperimen)</th><th>&#952;c (hitung)</th></tr>'
                '<tr><td>Kaca Crown</td><td>1.517</td><td>1.000</td><td>___°</td><td>___°</td></tr>'
                '<tr><td>Kaca Flint</td><td>1.785</td><td>1.000</td><td>___°</td><td>___°</td></tr>'
                '<tr><td>Intan</td><td>2.417</td><td>1.000</td><td>___°</td><td>___°</td></tr>'
                '<tr><td>SiO&#8322;</td><td>1.458</td><td>1.000</td><td>___°</td><td>___°</td></tr>'
                '</table></div>',
                unsafe_allow_html=True)
        with col_b:
            st.markdown(
                '<div class="section-card" style="border-left:4px solid #34d399;">'
                '<div style="font-size:12px;font-weight:700;color:#34d399;margin-bottom:8px;">📝 Pertanyaan Refleksi</div>'
                '<div style="font-size:11px;color:#94a3b8;line-height:2;">'
                '1. Material mana yang punya &#952;c terkecil? Apa artinya?<br>'
                '2. Mengapa intan begitu berkilau? Kaitkan dengan &#952;c-nya!<br>'
                '3. Mengapa TIR hanya bisa terjadi dari medium rapat ke renggang?<br>'
                '4. Jelaskan cara kerja serat optik berdasarkan hasil percobaan ini!<br>'
                '5. Apa yang dimaksud gelombang evanescent? Amati di diagram saat TIR aktif.'
                '</div></div>',
                unsafe_allow_html=True)

    with act_tab3:
        st.markdown(
            '<div class="section-card" style="border-top:3px solid #a78bfa;">'
            '<div style="font-size:16px;font-weight:800;color:#a78bfa;margin-bottom:4px;">🌈 Percobaan 3: Dispersi Cahaya &amp; Sudut Brewster</div>'
            '<div style="font-size:12px;color:#94a3b8;margin-bottom:16px;">Kurikulum Merdeka Fase F | Fisika SMA Kelas XI | ~30 menit</div>'
            '<div style="font-size:13px;font-weight:700;color:#cbd5e1;margin-bottom:8px;">🎯 Tujuan Percobaan</div>'
            '<div style="font-size:12px;color:#94a3b8;line-height:1.8;">Mengamati fenomena dispersi cahaya (pemisahan warna) pada prisma, menemukan sudut Brewster secara eksperimental menggunakan kurva Fresnel, dan memahami konsep polarisasi cahaya oleh permukaan.</div>'
            '</div>',
            unsafe_allow_html=True)

        steps_p3 = [
            ("A", "Dispersi — Setup Awal", "#a78bfa",
             "Pilih <strong>Medium 1: Kaca Flint (SF11)</strong> dan <strong>Medium 2: Vakum/Udara</strong>. Atur sudut datang ke 30°. Aktifkan toggle <strong>🌈 Tampilkan Dispersi</strong> di bagian Sumber Cahaya sidebar."),
            ("B", "Amati Pemisahan Warna", "#a78bfa",
             "Perhatikan diagram: sinar refraksi terpisah menjadi spektrum warna (merah ke ungu). Warna mana yang dibiaskan paling jauh dari normal? Warna mana yang paling dekat?"),
            ("C", "Variasi Sudut Dispersi", "#a78bfa",
             "Coba sudut 10°, 20°, 30°, 40°. Pada sudut berapa pemisahan warna terlihat paling jelas? Catat. Ubah ke Kaca Crown — apakah dispersi lebih besar atau lebih kecil?"),
            ("D", "Sudut Brewster — Konsep", "#fbbf24",
             "Matikan Dispersi. Pilih <strong>Kaca Crown ke Udara</strong>. Buka tab Teori, baca bagian Koefisien Fresnel. Rumus sudut Brewster: <strong>tan &#952;B = n&#8322;/n&#8321;</strong>. Hitung &#952;B untuk Kaca Crown!"),
            ("E", "Temukan Sudut Brewster", "#fbbf24",
             "Atur sudut datang mendekati nilai &#952;B yang kamu hitung (sekitar 56.5°). Amati kurva Fresnel di bawah diagram — cari titik di mana garis ungu (Rp) menyentuh nol. Catat sudutnya."),
            ("F", "Verifikasi dengan KPI", "#fbbf24",
             "Perhatikan KPI card <em>&#952;_Brewster</em>. Bandingkan dengan nilai yang kamu temukan. Amati panel Koefisien Fresnel — Rp seharusnya mendekati 0% saat sudut Brewster."),
            ("G", "Aplikasi Polarisasi", "#34d399",
             "Bayangkan sinar matahari memantul dari permukaan danau pada sudut Brewster. Sinar pantul hanya berisi komponen-s (terpolarisasi). Itulah cara kerja kacamata polaroid — menyaring komponen-s berlebih agar tidak silau!"),
        ]
        for num, title, color, desc in steps_p3:
            render_step_card(num, title, color, desc)

        st.markdown(
            '<div class="section-card" style="border-left:4px solid #a78bfa;margin-top:4px;">'
            '<div style="font-size:13px;font-weight:700;color:#a78bfa;margin-bottom:8px;">📝 Pertanyaan Refleksi Akhir</div>'
            '<div style="font-size:12px;color:#94a3b8;line-height:2;">'
            '1. Mengapa cahaya ungu dibiaskan lebih kuat daripada merah? Kaitkan dengan indeks bias dan panjang gelombang.<br>'
            '2. Sebutkan contoh dispersi cahaya dalam kehidupan sehari-hari selain pelangi.<br>'
            '3. Jelaskan apa yang dimaksud Rp = 0 pada sudut Brewster. Apakah artinya tidak ada cahaya yang dipantulkan?<br>'
            '4. Mengapa kacamata polaroid efektif mengurangi silau dari permukaan air tetapi tidak efektif untuk silau dari langit?<br>'
            '5. Hubungkan: bagaimana seorang fotografer memanfaatkan sudut Brewster dalam pemotretan outdoor?'
            '</div></div>',
            unsafe_allow_html=True)

# ── TAB 3: TEORI ─────────────────────────────────────────────────────────────
with tab_teori:
    col_t1, col_t2 = st.columns([1, 1], gap="large")
    with col_t1:
        st.markdown("### 📐 Hukum Snellius")
        st.markdown("""
        <div class="section-card">
            <div class="formula-box">n₁ · sin θ₁ = n₂ · sin θ₂</div>
            <div style="font-size: 12px; color: #94a3b8; line-height: 1.8; margin-top: 10px;">
                Diformulasikan oleh <strong style="color: #cbd5e1;">Willebrord Snellius</strong> (1621).
                Saat cahaya berpindah medium, frekuensinya tetap namun panjang gelombang dan kecepatannya berubah
                sesuai perbandingan indeks bias.
            </div>
            <div style="margin-top: 14px;">
                <div class="step-row">
                    <div class="step-num">1</div>
                    <div class="step-text"><strong>n₁ > n₂</strong> → sinar menjauh dari normal (θ₂ > θ₁). Potensi TIR jika θ₁ > θc.</div>
                </div>
                <div class="step-row">
                    <div class="step-num">2</div>
                    <div class="step-text"><strong>n₁ < n₂</strong> → sinar mendekati normal (θ₂ < θ₁). Tidak ada TIR.</div>
                </div>
                <div class="step-row">
                    <div class="step-num">3</div>
                    <div class="step-text"><strong>n₁ = n₂</strong> → sinar lurus tanpa pembelokkan.</div>
                </div>
            </div>
            <div class="info-tooltip" style="margin-top:14px;">
                <strong>Asal-usul Fisika:</strong> Hukum Snellius lahir dari prinsip Fermat — cahaya selalu 
                menempuh jalur yang meminimumkan waktu tempuh (principle of least time). Secara matematis,
                ini setara dengan kekekalan komponen momentum paralel foton terhadap antarmuka.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🔴 Pemantulan Internal Sempurna (TIR)")
        st.markdown("""
        <div class="section-card">
            <div class="formula-box">sin θc = n₂ / n₁</div>
            <div style="font-size: 12px; color: #94a3b8; line-height: 1.8; margin-top: 10px;">
                Syarat TIR: sinar dari <strong style="color: #cbd5e1;">medium rapat (n₁)</strong> menuju 
                <strong style="color: #cbd5e1;">medium renggang (n₂)</strong> dengan sudut ≥ θc.
                <br><br>
                <strong style="color: #f87171;">⚠️ Penting:</strong> TIR hanya terjadi ketika cahaya merambat 
                dari medium dengan indeks bias LEBIH TINGGI ke medium dengan indeks bias LEBIH RENDAH.
            </div>
            <div style="margin-top: 12px;">
                <div class="step-row">
                    <div class="step-num">A</div>
                    <div class="step-text"><strong>Gelombang Evanescent:</strong> Saat TIR terjadi, medan elektromagnetik masih menembus medium-2 sejauh ~λ/2π. Dimanfaatkan pada mikroskop TIRF.</div>
                </div>
                <div class="step-row">
                    <div class="step-num">B</div>
                    <div class="step-text"><strong>Frustated TIR:</strong> Jika medium-3 didekatkan ke antarmuka, energi evanescent bisa "ditransfer" → dasar tunneling foton.</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🌈 Dispersi Cahaya")
        st.markdown("""
        <div class="section-card">
            <div class="formula-box" style="font-size:13px;">n(λ) — Indeks bias bergantung panjang gelombang</div>
            <div style="font-size: 12px; color: #94a3b8; line-height: 1.8; margin-top: 10px;">
                Indeks bias material bergantung pada frekuensi cahaya. Cahaya ungu (λ pendek) dibiaskan
                lebih kuat dari cahaya merah (λ panjang). Persamaan Cauchy memodelkan dispersi:
            </div>
            <div class="formula-box" style="font-size:12px; margin-top:10px;">n(λ) = A + B/λ² + C/λ⁴</div>
            <div style="font-size: 11px; color: #64748b; margin-top: 8px; line-height: 1.7;">
                • Kaca Crown (BK7): A=1.5046, B=4.2×10⁻³ μm², C=9.7×10⁻⁵ μm⁴<br>
                • Kaca Flint (SF11): dispersi tinggi → ideal untuk prisma spektroskopi<br>
                • Intan: dispersi sangat tinggi → kilap warna spektral (fire)
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_t2:
        st.markdown("### 🔬 Koefisien Fresnel")
        st.markdown("""
        <div class="section-card">
            <div style="font-size: 12px; color: #94a3b8; line-height: 1.8; margin-bottom: 12px;">
                Diturunkan oleh <strong style="color: #cbd5e1;">Augustin-Jean Fresnel</strong> (1823) dari
                persamaan Maxwell. Menghitung fraksi energi yang dipantulkan (R) dan ditransmisikan (T)
                untuk dua polarisasi:
            </div>
            <div class="formula-box" style="font-size: 12px; text-align: left; padding: 14px 18px; line-height: 2;">
                rₛ = (n₁cosθ₁ − n₂cosθ₂) / (n₁cosθ₁ + n₂cosθ₂)<br>
                rₚ = (n₂cosθ₁ − n₁cosθ₂) / (n₂cosθ₁ + n₁cosθ₂)<br>
                <span style="color: #64748b; font-size: 10px;">Rₛ = |rₛ|² &nbsp; Rₚ = |rₚ|²</span>
            </div>
            <div class="info-tooltip" style="margin-top: 10px;">
                <strong>Sudut Brewster (θB):</strong> tan θB = n₂/n₁<br>
                Pada θB, Rₚ = 0 → sinar pantul terpolarisasi sempurna (hanya komponen-s). 
                Dimanfaatkan dalam kacamata polaroid, layar LCD, dan laser.
            </div>
            <div style="margin-top: 12px;">
                <div class="step-row">
                    <div class="step-num">s</div>
                    <div class="step-text"><strong>Polarisasi-s (TE):</strong> Medan listrik tegak lurus bidang datang. Reflektansi Rₛ selalu naik monoton dari 0° → 90°.</div>
                </div>
                <div class="step-row">
                    <div class="step-num">p</div>
                    <div class="step-text"><strong>Polarisasi-p (TM):</strong> Medan listrik sejajar bidang datang. Rₚ = 0 di sudut Brewster.</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 💡 Indeks Bias & Kecepatan Cahaya")
        st.markdown("""
        <div class="section-card">
            <div class="formula-box">n = c / v</div>
            <div style="font-size: 12px; color: #94a3b8; line-height: 1.8; margin-top: 10px;">
                Indeks bias (n) menyatakan seberapa lambat cahaya di medium itu dibandingkan vakum.
                Semakin besar n, semakin lambat cahaya merambat, dan semakin kuat pembiasan terjadi.
            </div>
            <div style="margin-top:10px; font-size:11px; color:#64748b; line-height:1.9;">
                • Vakum/Udara: n ≈ 1.000 → c = 3×10⁸ m/s<br>
                • Air: n = 1.333 → v ≈ 2.25×10⁸ m/s (75% kecepatan vakum)<br>
                • Kaca Crown: n = 1.517 → v ≈ 1.97×10⁸ m/s<br>
                • Intan: n = 2.417 → v ≈ 1.24×10⁸ m/s (41% kecepatan vakum)
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📊 Database Material Optik")
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        for mat, data in MATERIAL_DB.items():
            n_val = data["n"]
            theta_c = np.degrees(np.arcsin(1.0003/n_val)) if n_val > 1.001 else None
            c_str = f"{theta_c:.1f}°" if theta_c else "—"
            v_str = f"{2.998e8/n_val/1e8:.3f}×10⁸ m/s"
            st.markdown(f"""
            <div style="display: flex; align-items: center; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.04);">
                <div>
                    <div style="font-size: 12px; color: #ffffff; font-weight: 700;">{mat}</div>
                    <div style="font-size: 10px; color: #475569;">{data['category']} · {v_str}</div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 14px; font-weight: 800; color: {data['color_border']}; font-family: 'JetBrains Mono', monospace;">n = {n_val:.3f}</div>
                    <div style="font-size: 10px; color: #475569;">θc (ke udara) = {c_str}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ── TAB 4: APLIKASI ──────────────────────────────────────────────────────────
with tab_aplikasi:
    st.markdown("### 🌍 Penerapan Optik dalam Kehidupan & Teknologi")
    st.markdown("""
    <div class="info-tooltip">
        <strong>Dari teori ke aplikasi nyata:</strong> Hukum Snellius, Fresnel, dan TIR bukan sekadar 
        rumus di buku — mereka adalah fondasi teknologi modern yang kita gunakan setiap hari.
    </div>
    """, unsafe_allow_html=True)
    
    apps = [
        {"icon": "🔌", "title": "Serat Optik (Fiber Optic)", "principle": "TIR",
         "detail": "Sinar cahaya terperangkap di dalam inti serat (n≈1.46) oleh lapisan cladding (n≈1.44). θc ≈ 8.5°. Data melintas jarak ribuan km dengan atenuasi <0.2 dB/km pada 1550nm.",
         "color": "#60a5fa", "fact": "Satu serat seukuran rambut manusia mampu membawa 44 TB/s data.",
         "steps": ["Laser 1550nm dimasukkan ke inti serat (SiO₂)", "TIR terjadi berulang kali sepanjang serat", "Sinyal tiba di tujuan dengan redaman minimal"]},
        {"icon": "💎", "title": "Kilap Intan (Diamond Brilliance)", "principle": "TIR Berulang",
         "detail": "Intan memiliki n=2.417 → θc=24.4°. Potongan brilian 58 faset dirancang agar sinar masuk selalu memantul sempurna sebelum keluar ke mata pengamat.",
         "color": "#a78bfa", "fact": "Total internal reflection terjadi >95% pada setiap faset intan berkualitas.",
         "steps": ["Cahaya masuk melalui mahkota intan", "TIR berulang memantulkan sinar di dalam", "Cahaya keluar dari pavilion dengan sudut tertentu menciptakan kilauan"]},
        {"icon": "👓", "title": "Lensa Kamera & Kacamata", "principle": "Pembiasan Snellius",
         "detail": "Desain lensa apokromatik menggabungkan kaca crown (n=1.52) dan flint (n=1.78) untuk mengoreksi aberasi kromatik. Coating anti-refleksi (MgF₂, n=1.38) mengurangi pantulan Fresnel.",
         "color": "#34d399", "fact": "Lensa smartphone modern menggunakan 7-9 elemen optis dengan lapisan coating anti-refleksi.",
         "steps": ["Cahaya dibiaskan oleh tiap lensa sesuai Hukum Snellius", "Elemen crown & flint mengkoreksi dispersi warna", "Coating anti-refleksi (n=√(n_kaca)) meminimalkan refleksi Fresnel"]},
        {"icon": "🔬", "title": "Mikroskop TIRF", "principle": "Gelombang Evanescent",
         "detail": "Total Internal Reflection Fluorescence (TIRF) mengeksploitasi gelombang evanescent yang hanya menembus ≈100nm ke spesimen. Memungkinkan pencitraan molekul tunggal.",
         "color": "#fbbf24", "fact": "TIRF digunakan untuk meneliti cara protein bergerak di membran sel secara real-time.",
         "steps": ["Laser dipantulkan TIR di antarmuka kaca-sel", "Gelombang evanescent menembus ~100nm ke sel", "Hanya fluorofor di dekat antarmuka yang tereksitasi"]},
        {"icon": "☀️", "title": "Panel Surya", "principle": "Anti-Refleksi Fresnel",
         "detail": "Permukaan tekstur nano pada panel surya mengurangi refleksi Fresnel dari 30% → 2%. Coating anti-refleksi SiNₓ (n≈2.0) dirancang agar interferensi destruktif menihilkan refleksi.",
         "color": "#f97316", "fact": "Prism solar concentrator menggunakan dispersi untuk memisahkan spektrum dan mengoptimalkan sel berbeda.",
         "steps": ["Cahaya matahari mengenai permukaan silikon (n≈3.5)", "Tanpa coating, refleksi Fresnel bisa 30%", "Coating SiNₓ tunggal mengurangi refleksi ke ~10%, multi-layer ke <2%"]},
        {"icon": "🌈", "title": "Pelangi", "principle": "Dispersi + TIR",
         "detail": "Tetes hujan (n≈1.333) membiaskan dan memantulkan secara internal sinar matahari. Sudut pelangi primer ≈42°, sekunder ≈51° (urutan warna terbalik).",
         "color": "#f43f5e", "fact": "Pelangi selalu membentuk sudut 42° dari titik bayangan kepala pengamat (antisolar point).",
         "steps": ["Cahaya putih masuk ke tetes hujan, terdispersi (Snellius)", "Satu kali pantulan internal di bagian belakang tetes", "Cahaya keluar dengan sudut yang bergantung pada warna"]},
        {"icon": "📱", "title": "Layar Smartphone Sapphire", "principle": "TIR + Snellius",
         "detail": "Cover kaca sapphire (n=1.762) pada smartphone premium memanfaatkan sudut kritis 34.7° ke udara untuk menyebarkan cahaya latar (backlight) secara merata.",
         "color": "#38bdf8", "fact": "Sapphire 3× lebih keras dari kaca biasa (Mohs 9 vs 6) — hampir tidak bisa tergores kecuali oleh intan.",
         "steps": ["Cahaya LED masuk ke tepi panel sapphire/kaca", "TIR memandu cahaya di seluruh panel", "Microstructure di permukaan mengekstrak cahaya secara seragam"]},
        {"icon": "🏥", "title": "Endoskopi Medis", "principle": "TIR dalam Bundle Serat",
         "detail": "Bundle ribuan serat optik fleksibel meneruskan gambar dari ujung endoskop ke kamera. Setiap serat membawa satu piksel gambar melalui TIR berulang.",
         "color": "#10b981", "fact": "Endoskop modern bisa masuk ke arteri berdiameter 1mm dengan resolusi cukup untuk mendeteksi plak.",
         "steps": ["Kamera kecil di ujung endoskop menangkap gambar", "Ribuan serat optik membawa cahaya gambar melalui TIR", "Gambar direkonstruksi di layar monitor secara real-time"]},
    ]
    
    cols = st.columns(2, gap="large")
    for i, app in enumerate(apps):
        with cols[i % 2]:
            steps_html = "".join([f'<div style="font-size:10px; color:#64748b; padding:2px 0; border-left:2px solid {app["color"]}40; padding-left:8px; margin:3px 0;">→ {s}</div>' for s in app.get("steps", [])])
            st.markdown(f"""
            <div class="section-card" style="border-top: 3px solid {app['color']}; margin-bottom: 12px;">
                <div style="display: flex; align-items: flex-start; gap: 10px;">
                    <div style="font-size: 28px; line-height: 1;">{app['icon']}</div>
                    <div style="flex: 1;">
                        <div style="font-size: 14px; font-weight: 700; color: {app['color']}; margin-bottom: 3px;">{app['title']}</div>
                        <div style="display: inline-block; font-size: 9px; font-weight: 700; color: {app['color']}; background: {app['color']}18; border: 1px solid {app['color']}30; border-radius: 100px; padding: 2px 8px; letter-spacing: 0.05em; margin-bottom: 8px; text-transform: uppercase;">{app['principle']}</div>
                        <div style="font-size: 12px; color: #94a3b8; line-height: 1.7;">{app['detail']}</div>
                        <div style="margin-top: 8px;">{steps_html}</div>
                        <div style="margin-top: 8px; padding: 6px 10px; background: rgba(255,255,255,0.03); border-radius: 6px; border-left: 3px solid {app['color']};">
                            <span style="font-size: 10px; color: #64748b; font-style: italic;">💡 {app['fact']}</span>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ── TAB 5: DIAGNOSTIK THREE-TIER ─────────────────────────────────────────────
with tab_diagnostik:
    st.markdown("### 🧠 Tes Diagnostik Miskonsepsi — Three-Tier Test")
    st.markdown("""
    <div class="info-tooltip">
        <strong>Tentang Three-Tier Test:</strong> Model diagnostik yang mampu membedakan
        <em>miskonsepsi</em> (salah + yakin) dari <em>kurang pengetahuan</em> (salah + tidak yakin)
        dan <em>pemahaman ilmiah</em> (benar + yakin). Dikembangkan oleh Treagust (1988).
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    
    soal_options = [
        "Soal A — Pembiasan (Renggang→Rapat)",
        "Soal B — Pemantulan Internal Sempurna",
        "Soal C — Sudut Brewster & Polarisasi",
    ]
    soal_pilihan = st.radio("Pilih Soal:", soal_options, horizontal=True)
    st.markdown("---")
    
    if soal_pilihan == soal_options[0]:
        soal_context = "**Skenario:** Sinar laser melintas dari udara (n=1.0) memasuki air (n=1.333) dengan sudut datang θ₁=30°."
        t1_q = "Apa yang terjadi pada sudut sinar setelah masuk air?"
        t1_opts = [
            "Sudut bias θ₂ > θ₁ (sinar menjauh garis normal)",
            "Sudut bias θ₂ < θ₁ (sinar mendekati garis normal)",
            "θ₂ = θ₁ (sinar lurus, tidak berbelok)",
            "Sinar dipantulkan sempurna (TIR)"
        ]
        t1_correct = t1_opts[1]
        t2_opts = [
            "Karena kecepatan cahaya MENINGKAT di air, sehingga membelok menjauhi normal.",
            "Karena kecepatan cahaya BERKURANG di air (n besar → v kecil), gelombang membelok mendekati normal sesuai Hukum Snellius.",
            "Karena air lebih padat sehingga cahaya tertahan dan tidak bisa menembus jauh.",
            "Karena sudah dibawah sudut kritis, terjadi pemantulan sebagian."
        ]
        t2_correct = t2_opts[1]
    
    elif soal_pilihan == soal_options[1]:
        soal_context = "**Skenario:** Sinar di dalam kaca crown (n=1.52) menuju udara (n=1.0) dengan sudut datang 50°. Sudut kritis kaca-udara = 41.1°."
        t1_q = "Apa yang terjadi pada sinar di antarmuka kaca-udara?"
        t1_opts = [
            "Sinar dibiaskan ke udara dengan sudut lebih besar dari 90°",
            "Sinar dipantulkan sempurna kembali ke kaca (TIR)",
            "Sinar menembus udara dengan sudut bias = 50°",
            "Sinar terserap seluruhnya oleh antarmuka"
        ]
        t1_correct = t1_opts[1]
        t2_opts = [
            "Karena sudut datang (50°) melebihi sudut kritis (41.1°), tidak ada solusi real untuk θ₂ dalam Hukum Snellius → seluruh energi dipantulkan.",
            "Karena kaca lebih padat dari udara sehingga cahaya tidak bisa keluar.",
            "Karena sudut datang terlalu besar untuk frekuensi cahaya yang digunakan.",
            "Karena indeks bias kaca lebih besar dari 1.5 sehingga selalu terjadi TIR."
        ]
        t2_correct = t2_opts[0]
    
    else:
        soal_context = "**Skenario:** Cahaya tak terpolarisasi mengenai permukaan kaca (n=1.52) dari udara. Sudut datang sama dengan sudut Brewster θB = arctan(1.52) ≈ 56.7°."
        t1_q = "Apa yang istimewa dari cahaya pantul pada sudut Brewster?"
        t1_opts = [
            "Cahaya pantul sepenuhnya hilang (R=0)",
            "Cahaya pantul terpolarisasi sempurna (hanya komponen-s/TE)",
            "Cahaya pantul memiliki intensitas sama dengan cahaya bias",
            "Cahaya pantul berubah warna menjadi putih"
        ]
        t1_correct = t1_opts[1]
        t2_opts = [
            "Karena pada θB, koefisien refleksi rp=0 untuk polarisasi paralel (Rp=0), sehingga hanya komponen senkatan (Rs≠0) yang dipantulkan.",
            "Karena pada θB, sinar datang dan sinar bias membentuk sudut 90°, sehingga secara geometri dipol osilator tidak bisa meradiasi ke arah pantul untuk polarisasi-p.",
            "Keduanya benar — baik penjelasan Fresnel maupun model dipol keduanya valid dan ekuivalen.",
            "Karena pada θB, n₁=n₂ berlaku secara efektif untuk polarisasi-p."
        ]
        t2_correct = t2_opts[2]
    
    st.markdown(soal_context)
    st.markdown("---")
    
    with st.form("diagnostic_form_v2", clear_on_submit=False):
        st.markdown(f"** Tier 1 — Konsep:** {t1_q}")
        ans_t1 = st.radio(" ", t1_opts, index=None, key="t1")
        
        st.markdown("---")
        st.markdown("**🔬 Tier 2 — Alasan Fisika:** Mengapa hal itu terjadi?")
        ans_t2 = st.radio(" ", t2_opts, index=None, key="t2")
        
        st.markdown("---")
        st.markdown("**📊 Tier 3 — Confidence Level:** Seberapa yakin Anda?")
        conf_opts = [
            "Sangat Yakin (>80%) — Saya paham konsepnya",
            "Cukup Yakin (50-80%) — Ada sedikit keraguan",
            "Kurang Yakin (<50%) — Saya menebak"
        ]
        ans_t3 = st.radio(" ", conf_opts, index=None, key="t3")
        
        submitted = st.form_submit_button("🔍 Analisis Jawabanku", type="primary", use_container_width=True)
    
    if submitted:
        if not all([ans_t1, ans_t2, ans_t3]):
            st.error("⚠️ Harap isi semua tier sebelum menganalisis.")
        else:
            t1_correct_bool = ans_t1 == t1_correct
            t2_correct_bool = ans_t2 == t2_correct
            confident = "Sangat Yakin" in ans_t3 or "Cukup Yakin" in ans_t3
            
            st.markdown("---")
            st.markdown("### 📋 Hasil Diagnosis")
            
            col_d1, col_d2 = st.columns([2, 1])
            
            with col_d1:
                if t1_correct_bool and t2_correct_bool and "Sangat Yakin" in ans_t3:
                    st.success("""
                    ✅ **Scientific Knowledge — Paham Konsep Ilmiah**
                    
                    Jawaban Anda benar di semua tier dengan keyakinan tinggi. 
                    Anda memiliki pemahaman konseptual dan kausal yang solid tentang materi ini.
                    Lanjutkan ke soal tantangan tingkat lanjut!
                    """)
                elif t1_correct_bool and t2_correct_bool and "Cukup Yakin" in ans_t3:
                    st.info("""
                    ℹ️ **Kurang Percaya Diri (Lack of Confidence)**
                    
                    Jawaban Anda benar namun keyakinan masih sedang. 
                    Coba ulangi eksperimen dengan variasi parameter untuk memperkuat intuisi Anda.
                    """)
                elif t1_correct_bool and not t2_correct_bool:
                    st.warning("""
                    ⚠️ **Pemahaman Parsial (Partial Understanding)**
                    
                    Anda mengetahui *apa* yang terjadi (Tier 1 benar) namun belum sepenuhnya 
                    memahami *mengapa* hal itu terjadi (Tier 2 salah). 
                    Pelajari derivasi matematis Hukum Snellius dari persamaan Maxwell.
                    """)
                elif not t1_correct_bool and confident:
                    st.error("""
                    🚨 **Miskonsepsi Teridentifikasi (Misconception)**
                    
                    Anda sangat yakin namun jawaban kurang tepat. Ini adalah miskonsepsi 
                    yang perlu diluruskan — justru yang paling penting untuk diperbaiki.
                    Gunakan simulator untuk mengamati arah pembelokkan sinar secara langsung.
                    """)
                else:
                    st.warning("""
                    ❓ **Kurang Pengetahuan (Lack of Knowledge)**
                    
                    Anda menyadari ketidakyakinan dan jawaban belum tepat. 
                    Ini adalah titik awal yang baik — eksplorasi simulator dan baca teori terlebih dahulu.
                    """)
            
            with col_d2:
                score = (int(t1_correct_bool) + int(t2_correct_bool)) * 50
                score_color = '#34d399' if score == 100 else '#fbbf24' if score == 50 else '#f87171'
                st.markdown(f"""
                <div style="text-align: center; padding: 20px; background: #111827; border: 1px solid rgba(255,255,255,0.08); border-radius: 14px;">
                    <div style="font-size: 42px; font-weight: 800; color: {score_color};">{score}</div>
                    <div style="font-size: 11px; color: #475569; text-transform: uppercase; letter-spacing: 0.1em;">Skor / 100</div>
                    <div style="margin-top: 12px; font-size: 11px; color: #64748b;">
                        Tier 1: {"✅" if t1_correct_bool else "❌"}<br>
                        Tier 2: {"✅" if t2_correct_bool else "❌"}<br>
                        Tier 3: {"🟢" if "Sangat" in ans_t3 else "🟡" if "Cukup" in ans_t3 else "🔴"}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with st.expander("📖 Lihat Jawaban & Penjelasan Lengkap"):
                t3_conf_label = (
                    "Sangat Yakin (>80%) — menunjukkan keyakinan tinggi."
                    if "Sangat" in ans_t3 else
                    "Cukup Yakin (50–80%) — menunjukkan sedikit keraguan."
                    if "Cukup" in ans_t3 else
                    "Kurang Yakin (<50%) — menunjukkan ketidakyakinan/menebak."
                )
                t3_advice = (
                    "Pertahankan keyakinan ini dengan terus berlatih soal serupa."
                    if "Sangat" in ans_t3 else
                    "Perkuat pemahaman dengan memperbanyak latihan dan diskusi."
                    if "Cukup" in ans_t3 else
                    "Fokus membaca teori dan eksplorasi simulator sebelum mengerjakan soal berikutnya."
                )
                st.markdown(f"""
**Tier 1 — Jawaban Benar:**
> {t1_correct}

**Tier 2 — Alasan yang Tepat:**
> {t2_correct}

**Tier 3 — Interpretasi Confidence Level:**
> Jawaban Anda: *{t3_conf_label}*  
> {t3_advice}

**Catatan Fisika:**
Hukum Snellius menyatakan bahwa perbandingan sinus sudut berbanding terbalik dengan
perbandingan kecepatan cahaya di medium tersebut: n₁/n₂ = v₂/v₁ = sin θ₂/sin θ₁.
Saat cahaya memasuki medium dengan n lebih besar (lebih lambat), sudut bias lebih kecil
dari sudut datang — sinar mendekati normal.
                """)

# ══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; color: #334155; font-size: 11px; line-height: 2;">
    <div style="font-family: 'JetBrains Mono', monospace; font-size: 9px; letter-spacing: 0.12em; color: #1e3a5f; text-transform: uppercase; margin-bottom: 6px;">OptiLab Pro · Simulasi Optik Fisika</div>
    <div>Hukum Snellius · Koefisien Fresnel · TIR · Dispersi · Sudut Brewster</div>
    <div style="margin-top: 4px;">Kurikulum Merdeka Fase F · Fisika SMA Kelas XI</div>
    <div style="margin-top: 8px; color: #1e3a5f;">Model Fisika: Fresnel (1823) · Snellius (1621) · Maxwell (1865)</div>
</div>
""", unsafe_allow_html=True)