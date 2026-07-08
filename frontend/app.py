import streamlit as st
import requests
import json
import time

# ─── Page Config ───────────────────────────────────────────────
st.set_page_config(
    page_title="XAI Tutor",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ── App background ── */
    .stApp {
        background: linear-gradient(145deg, #f8f6ff 0%, #f0f4ff 40%, #f5f8ff 100%);
        color: #1e1b4b;
    }

    .main .block-container {
        padding-top: 1.5rem;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f5f3ff 100%);
        border-right: 1px solid #e0d9ff;
    }

    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stCaption {
        color: #4c1d95 !important;
    }

    /* ── Answer box ── */
    .answer-box {
        background: linear-gradient(135deg, #ffffff 0%, #faf9ff 100%);
        border: 1px solid #ddd6fe;
        border-left: 4px solid #7c3aed;
        border-radius: 14px;
        padding: 20px 24px;
        font-size: 15px;
        line-height: 1.85;
        color: #1e1b4b;
        margin: 10px 0;
        box-shadow: 0 2px 12px rgba(124, 58, 237, 0.06);
    }

    /* ── XAI card ── */
    .xai-card {
        background: linear-gradient(135deg, #faf5ff 0%, #f5f3ff 100%);
        border: 1px solid #e9d5ff;
        border-radius: 12px;
        padding: 16px 18px;
        margin: 8px 0;
        box-shadow: 0 1px 6px rgba(124, 58, 237, 0.05);
    }

    /* ── Badges ── */
    .badge-high {
        background: linear-gradient(135deg, #d1fae5, #a7f3d0);
        color: #065f46;
        padding: 3px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        border: 1px solid #6ee7b7;
    }
    .badge-moderate {
        background: linear-gradient(135deg, #fef3c7, #fde68a);
        color: #78350f;
        padding: 3px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        border: 1px solid #fcd34d;
    }
    .badge-low {
        background: linear-gradient(135deg, #fee2e2, #fecaca);
        color: #7f1d1d;
        padding: 3px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        border: 1px solid #fca5a5;
    }

    /* ── Word chips ── */
    .word-chip {
        display: inline-block;
        background: linear-gradient(135deg, #ede9fe, #ddd6fe);
        color: #5b21b6;
        border: 1px solid #c4b5fd;
        border-radius: 8px;
        padding: 3px 11px;
        margin: 3px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 12px;
        font-weight: 500;
    }

    /* ── Trace steps ── */
    .trace-step {
        background: linear-gradient(90deg, #faf5ff 0%, #ffffff 100%);
        border-left: 3px solid #8b5cf6;
        padding: 9px 14px;
        margin: 4px 0;
        border-radius: 0 8px 8px 0;
        font-family: 'JetBrains Mono', monospace;
        font-size: 12px;
        color: #6d28d9;
        box-shadow: 0 1px 4px rgba(139, 92, 246, 0.07);
    }

    /* ── Section title ── */
    .section-title {
        font-size: 11px;
        font-weight: 700;
        color: #7c3aed;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 10px;
        margin-top: 4px;
    }

    /* ── Hint box ── */
    .hint-box {
        background: linear-gradient(135deg, #eff6ff 0%, #f0f9ff 100%);
        border: 1px solid #bfdbfe;
        border-left: 3px solid #3b82f6;
        border-radius: 10px;
        padding: 14px 18px;
        color: #1e40af;
        font-size: 14px;
        margin: 6px 0;
        line-height: 1.7;
    }

    /* ── User message bubble ── */
    .user-bubble {
        background: linear-gradient(135deg, #ede9fe 0%, #e0e7ff 100%);
        border: 1px solid #c4b5fd;
        border-radius: 14px;
        padding: 14px 18px;
        margin: 12px 0 6px 0;
        box-shadow: 0 2px 8px rgba(124, 58, 237, 0.08);
    }

    /* ── Tabs ── */
    /* ── Tabs Container Fix ── */
    [data-testid="stTabs"] {
        gap: 6px;
    }

    /* ── All Tabs (Base + Streamlit) ── */
    button[data-baseweb="tab"],
    [data-testid="stTabs"] button {
        color: #5b5fc7 !important;
        background: #f8f7ff !important;
        border-radius: 12px 12px 0 0 !important;
        padding: 8px 14px !important;
        border: 1px solid #ddd6fe !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }

    /* ── Hover ── */
    button[data-baseweb="tab"]:hover,
    [data-testid="stTabs"] button:hover {
        color: #4f46e5 !important;
        background: #ede9fe !important;
    }

    /* ── Active Tab ── */
    button[data-baseweb="tab"][aria-selected="true"],
    [data-testid="stTabs"] button[aria-selected="true"] {
        color: #ffffff !important;
        background: linear-gradient(135deg, #6d5bd0, #4f7df3) !important;
        border: 1px solid #c4b5fd !important;
        border-bottom: none !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 14px rgba(109, 91, 208, 0.25) !important;
    }

    /* ── Remove Default Red Indicator ── */
    button[data-baseweb="tab"]::after {
        display: none !important;
    }

    /* ── Tab Content Box ── */
    [data-testid="stTabContent"] {
        background: #ffffff;
        border: 1px solid #ddd6fe;
        border-top: none;
        border-radius: 0 0 12px 12px;
        padding: 16px;
    }

    /* ── Primary button ── */
    .stButton button {
        background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        padding: 0.5rem 1.5rem;
        transition: all 0.2s ease;
        box-shadow: 0 2px 8px rgba(124, 58, 237, 0.25);
        letter-spacing: 0.3px;
    }

    .stButton button:hover {
        background: linear-gradient(135deg, #6d28d9 0%, #5b21b6 100%);
        transform: translateY(-1px);
        box-shadow: 0 5px 16px rgba(124, 58, 237, 0.35);
    }

    .stButton button:active {
        transform: translateY(0px);
    }

    /* ── Inputs ── */
    .stTextInput input {
        background: #ffffff !important;
        color: #1e1b4b !important;
        border: 1.5px solid #ddd6fe !important;
        border-radius: 10px !important;
        font-family: 'Inter', sans-serif;
        transition: border-color 0.2s;
        box-shadow: 0 1px 4px rgba(124, 58, 237, 0.06);
    }

    .stTextInput input::placeholder {
        color: #a78bfa !important;
        opacity: 1 !important;
    }

    .stTextInput input:focus {
        border-color: #8b5cf6 !important;
        box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.12) !important;
    }

    .stTextArea textarea {
        background: #ffffff;
        color: #1e1b4b;
        border: 1.5px solid #ddd6fe;
        border-radius: 10px;
        font-family: 'Inter', sans-serif;
    }

    .stTextArea textarea:focus {
        border-color: #8b5cf6;
    }

    /* ── Selectbox ── */
    .stSelectbox > div > div {
        background: #ffffff;
        border: 1.5px solid #ddd6fe;
        border-radius: 10px;
        color: #1e1b4b;
    }

    /* ── Metric ── */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #faf5ff 0%, #f5f3ff 100%);
        border: 1px solid #ddd6fe;
        border-radius: 12px;
        padding: 16px;
    }

    [data-testid="stMetricValue"] {
        color: #5b21b6 !important;
        font-weight: 700;
    }

    /* ── Divider ── */
    hr {
        border: none;
        border-top: 1px solid #ede9fe;
        margin: 1.2rem 0;
    }

    /* ── Expander ── */
    [data-testid="stExpander"] {
        background: #faf9ff;
        border: 1px solid #e9d5ff;
        border-radius: 10px;
    }

    /* ── Success/info/error ── */
    .stSuccess {
        background: linear-gradient(135deg, #ecfdf5, #d1fae5) !important;
        color: #065f46 !important;
        border-radius: 10px !important;
    }

    .stInfo {
        background: linear-gradient(135deg, #eff6ff, #e0f2fe) !important;
        color: #1e40af !important;
        border-radius: 10px !important;
    }

    .stError {
        background: linear-gradient(135deg, #fef2f2, #fee2e2) !important;
        color: #7f1d1d !important;
        border-radius: 10px !important;
    }

    /* ── Caption ── */
    .stCaption, [data-testid="stCaptionContainer"] {
        color: #7c3aed !important;
        opacity: 0.75;
    }

    /* ── Code ── */
    code {
        background: #ede9fe;
        color: #5b21b6;
        padding: 1px 6px;
        border-radius: 5px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 12px;
    }

    /* ── Header area ── */
    .app-header {
        background: linear-gradient(135deg, #7c3aed 0%, #4f46e5 50%, #6366f1 100%);
        border-radius: 16px;
        padding: 24px 28px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(124, 58, 237, 0.2);
    }

    .app-header h1 {
        color: #ffffff !important;
        font-weight: 700;
        font-size: 26px;
        margin: 0 0 4px 0;
    }

    .app-header p {
        color: rgba(255,255,255,0.8) !important;
        font-size: 13px;
        margin: 0;
        letter-spacing: 0.5px;
    }

    /* ── Empty state ── */
    .empty-state {
        text-align: center;
        padding: 70px 20px;
        color: #a78bfa;
    }

    .empty-state h3 {
        color: #7c3aed;
        font-weight: 600;
    }

    /* ── Bar chart color override ── */
    [data-testid="stVegaLiteChart"] {
        border-radius: 10px;
        overflow: hidden;
    }
    /* ── FIX ENTIRE UPLOADER ROW (black background issue) ── */
    [data-testid="stFileUploader"] section {
        background: #f8f7ff !important;
        border: 1px solid #ddd6fe !important;
        border-radius: 14px !important;
        padding: 12px !important;
    }

    /* ── Inner row (the dark strip you see) ── */
    [data-testid="stFileUploader"] section > div {
        background: #ffffff !important;
        border-radius: 10px !important;
        padding: 10px !important;
        display: flex !important;
        align-items: center !important;
        gap: 12px !important;
    }

    /* ── Upload button ── */
    [data-testid="stFileUploader"] section button {
        background: linear-gradient(135deg, #ede9fe, #e0e7ff) !important;
        color: #5b21b6 !important;
        border: 1px solid #c4b5fd !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
    }

    /* ── Upload text ── */
    [data-testid="stFileUploader"] span {
        color: #5b21b6 !important;
    }
</style>
""", unsafe_allow_html=True)

API_BASE = "http://localhost:8000"

# ─── Markdown → Clean HTML renderer ───────────────────────────
import re

def render_answer(text: str) -> str:
    """Convert LLM markdown output into styled HTML with no raw asterisks."""
    lines = text.split("\n")
    html_parts = []
    in_ol = False
    in_ul = False

    def close_lists():
        nonlocal in_ol, in_ul
        if in_ol:
            html_parts.append("</ol>")
            in_ol = False
        if in_ul:
            html_parts.append("</ul>")
            in_ul = False

    def inline_fmt(s):
        # Bold: **text** or __text__
        s = re.sub(r'\*\*(.+?)\*\*', r'<strong style="color:#4c1d95;font-weight:600;">\1</strong>', s)
        s = re.sub(r'__(.+?)__',     r'<strong style="color:#4c1d95;font-weight:600;">\1</strong>', s)
        # Italic: *text* or _text_
        s = re.sub(r'\*(.+?)\*', r'<em>\1</em>', s)
        s = re.sub(r'_(.+?)_',   r'<em>\1</em>', s)
        # Inline code
        s = re.sub(r'`(.+?)`', r'<code style="background:#ede9fe;color:#5b21b6;padding:1px 5px;border-radius:4px;">\1</code>', s)
        return s

    for line in lines:
        stripped = line.strip()
        if not stripped:
            close_lists()
            continue

        # H1 / H2 / H3
        h3 = re.match(r'^###\s+(.*)', stripped)
        h2 = re.match(r'^##\s+(.*)',  stripped)
        h1 = re.match(r'^#\s+(.*)',   stripped)
        if h1:
            close_lists()
            html_parts.append(f'<h2 style="color:#5b21b6;font-size:17px;font-weight:700;margin:16px 0 6px;">{inline_fmt(h1.group(1))}</h2>')
            continue
        if h2:
            close_lists()
            html_parts.append(f'<h3 style="color:#5b21b6;font-size:15px;font-weight:700;margin:14px 0 4px;">{inline_fmt(h2.group(1))}</h3>')
            continue
        if h3:
            close_lists()
            html_parts.append(f'<h4 style="color:#6d28d9;font-size:13px;font-weight:700;margin:10px 0 4px;text-transform:uppercase;letter-spacing:1px;">{inline_fmt(h3.group(1))}</h4>')
            continue

        # Numbered list: "1. " or "1) "
        ol_match = re.match(r'^\d+[\.\)]\s+(.*)', stripped)
        if ol_match:
            if in_ul:
                html_parts.append("</ul>")
                in_ul = False
            if not in_ol:
                html_parts.append('<ol style="margin:10px 0 10px 20px;padding:0;display:flex;flex-direction:column;gap:6px;">')
                in_ol = True
            html_parts.append(f'<li style="color:#1e1b4b;line-height:1.75;">{inline_fmt(ol_match.group(1))}</li>')
            continue

        # Bullet list: "- " or "* " or "• "
        ul_match = re.match(r'^[-\*•]\s+(.*)', stripped)
        if ul_match:
            if in_ol:
                html_parts.append("</ol>")
                in_ol = False
            if not in_ul:
                html_parts.append('<ul style="margin:10px 0 10px 18px;padding:0;display:flex;flex-direction:column;gap:5px;">')
                in_ul = True
            html_parts.append(f'<li style="color:#1e1b4b;line-height:1.75;">{inline_fmt(ul_match.group(1))}</li>')
            continue

        # Plain paragraph
        close_lists()
        html_parts.append(f'<p style="margin:6px 0;line-height:1.85;color:#1e1b4b;">{inline_fmt(stripped)}</p>')

    close_lists()
    return "\n".join(html_parts)

# ─── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='background:linear-gradient(135deg,#7c3aed,#4f46e5);border-radius:12px;padding:18px 20px;margin-bottom:16px;'>
        <div style='font-size:22px;margin-bottom:4px;'>🧠</div>
        <div style='color:#fff;font-weight:700;font-size:18px;letter-spacing:0.3px;'>XAI Tutor</div>
        <div style='color:rgba(255,255,255,0.75);font-size:12px;margin-top:2px;'>Transparent AI-powered learning</div>
    </div>
    """, unsafe_allow_html=True)

    mode = st.selectbox("Mode", ["auto", "tutor", "quiz", "simple"], index=0,
                        help="auto = smart routing | tutor = step-by-step | quiz = generate questions | simple = brief answer")

    st.divider()
    st.markdown("### ⚙️ Backend Status")
    try:
        r = requests.get(f"{API_BASE}/health", timeout=2)
        if r.status_code == 200:
            st.success("✅ Backend Online")
        else:
            st.error("❌ Backend Error")
    except:
        st.error("❌ Backend Offline")
        st.code("cd backend\nuvicorn app:app --reload", language="bash")

    st.divider()
    st.markdown("""
    <div style='background:linear-gradient(135deg,#ede9fe,#e0e7ff);border-radius:10px;padding:14px;border:1px solid #c4b5fd;'>
        <div style='font-size:11px;font-weight:700;color:#5b21b6;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:6px;'>About</div>
        <div style='font-size:12px;color:#4c1d95;line-height:1.6;'>TF-IDF retrieval + Ollama LLM + LIME / SHAP / Counterfactual explanations</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

# ─── Session State ─────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ─── Header ────────────────────────────────────────────────────
st.markdown("""
<div class='app-header'>
    <h1>🧠 XAI Tutor Chatbot</h1>
    <p>Explainable AI &nbsp;•&nbsp; Interpretable Retrieval &nbsp;•&nbsp; Transparent Reasoning</p>
</div>
""", unsafe_allow_html=True)

# ─── Input ─────────────────────────────────────────────────────
col_q, col_btn = st.columns([5, 1])
with col_q:
    query = st.text_input("", placeholder="Ask anything… e.g. 'Explain photosynthesis' or 'Quiz me on Newton's laws'",
                          label_visibility="collapsed")
with col_btn:
    st.markdown("<br>", unsafe_allow_html=True)
    ask_btn = st.button("Ask →", use_container_width=True)

# Image upload
with st.expander("📎 Upload Image / PDF text (optional)"):
    uploaded_file = st.file_uploader("Upload an image with text", type=["png", "jpg", "jpeg"])
    extra_context = st.text_area("Or paste additional context here", height=80)

# ─── Query Execution ───────────────────────────────────────────
if ask_btn and query.strip():
    full_query = query.strip()
    if extra_context.strip():
        full_query += f"\n\nAdditional context:\n{extra_context.strip()}"

    with st.spinner("🔍 Retrieving context… 🧠 Reasoning with LLM… ⚗️ Generating explanations…"):
        try:
            payload = {"query": full_query, "mode": mode}
            resp = requests.post(f"{API_BASE}/query", json=payload, timeout=90)
            resp.raise_for_status()
            data = resp.json()
            st.session_state.chat_history.append({"query": query, "data": data})
        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to backend. Run: `cd backend && uvicorn app:app --reload`")
            st.stop()
        except Exception as e:
            st.error(f"Error: {e}")
            st.stop()

# ─── Chat History ──────────────────────────────────────────────
if st.session_state.chat_history:
    for i, entry in enumerate(reversed(st.session_state.chat_history)):
        q = entry["query"]
        d = entry["data"]

        st.markdown(f"""
        <div class='user-bubble'>
            <span style='color:#7c3aed;font-weight:700;font-size:11px;letter-spacing:1.5px;text-transform:uppercase;'>You</span>
            <br><span style='color:#1e1b4b;font-size:15px;font-weight:400;'>{q}</span>
        </div>
        """, unsafe_allow_html=True)

        # ─── Answer ───
        st.markdown('<div class="section-title">Answer</div>', unsafe_allow_html=True)
        answer_text = d.get("answer", "No answer.")
        st.markdown(f'<div class="answer-box">{render_answer(answer_text)}</div>', unsafe_allow_html=True)

        # ─── Simplified (if available) ───
        if d.get("simplified") and d["simplified"] != answer_text:
            with st.expander("📖 Simplified Version"):
                st.info(d["simplified"])

        # ─── Tabs ───
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["🔍 Why (XAI)", "⚙️ How (Interpretability)", "📚 Evidence", "📊 Confidence", "🧑‍🏫 Tutor"])

        with tab1:
            xai = d.get("xai", {})

            st.markdown('<div class="section-title">LIME — Important Words</div>', unsafe_allow_html=True)
            lime = xai.get("lime", {})
            if lime.get("important_words"):
                word_html = " ".join([f'<span class="word-chip">{w["word"]} ({w["importance"]})</span>'
                                       for w in lime["important_words"]])
                st.markdown(word_html, unsafe_allow_html=True)
                st.caption(lime.get("explanation", ""))

            st.divider()
            st.markdown('<div class="section-title">SHAP — Feature Contributions</div>', unsafe_allow_html=True)
            shap = xai.get("shap", {})
            if shap.get("contributions"):
                import pandas as pd
                df = pd.DataFrame(shap["contributions"])
                st.bar_chart(df.set_index("word")["shap_value"], height=200)
                st.caption(shap.get("explanation", ""))

            st.divider()
            st.markdown('<div class="section-title">Counterfactual Analysis</div>', unsafe_allow_html=True)
            cf = xai.get("counterfactual", {})
            if cf.get("counterfactuals"):
                for c in cf["counterfactuals"]:
                    with st.container():
                        st.markdown(f"""<div class="xai-card">
                            <b style='color:#d97706'>If "{c['removed_word']}" removed:</b><br>
                            <span style='color:#6d28d9'>{c['impact']}</span><br>
                            <code style='color:#7c3aed;font-size:11px'>{c['modified_query']}</code>
                        </div>""", unsafe_allow_html=True)

        with tab2:
            interp = d.get("interpretability", {})
            trace = interp.get("trace", {})

            st.markdown('<div class="section-title">Pipeline Trace</div>', unsafe_allow_html=True)
            if trace.get("steps"):
                for step in trace["steps"]:
                    st.markdown(f"""<div class="trace-step">
                        <span style='color:#7c3aed;font-weight:600'>Step {step['step']}</span>
                        <span style='color:#a78bfa'> ({step['elapsed_ms']}ms)</span>
                        <span style='color:#4c1d95'> — {step['message']}</span>
                    </div>""", unsafe_allow_html=True)
                st.caption(f"Total pipeline time: {trace.get('total_time_ms', 0)}ms")

            st.divider()
            st.markdown('<div class="section-title">Decision Rules Fired</div>', unsafe_allow_html=True)
            rules = interp.get("rule_used", {})
            if rules.get("rules_fired"):
                for r in rules["rules_fired"]:
                    st.markdown(f"- `{r}`")
            st.info(rules.get("explanation", ""))

            st.markdown(f"**Method:** {interp.get('method', 'N/A')}")
            st.markdown(f"**Intent detected:** `{d.get('intent', 'N/A')}`")

        with tab3:
            evidence = d.get("evidence", [])
            rs = d.get("retrieval_score", 0)
            st.markdown(f'<div class="section-title">Top Retrieved Documents (TF-IDF Score: {rs})</div>', unsafe_allow_html=True)
            if evidence:
                for ev in evidence:
                    st.markdown(f"""<div class="xai-card">
                        <div style='display:flex;align-items:center;gap:8px;'>
                            <span style='font-size:18px;'>📄</span>
                            <div>
                                <b style='color:#5b21b6'>{ev['source']}</b><br>
                                <span style='color:#7c3aed;font-size:12px;font-family:JetBrains Mono,monospace;'>
                                    TF-IDF Similarity: {ev['score']}
                                </span>
                            </div>
                        </div>
                    </div>""", unsafe_allow_html=True)
            else:
                st.caption("No documents retrieved.")

        with tab4:
            conf = d.get("confidence", {})
            score = conf.get("score", 0)
            label = conf.get("label", "Unknown")
            badge_class = f"badge-{label.lower()}"

            col_s, col_l = st.columns([2, 3])
            with col_s:
                st.metric("Confidence Score", f"{score * 100:.0f}%")
                st.markdown(f'<span class="{badge_class}">{label}</span>', unsafe_allow_html=True)
            with col_l:
                breakdown = conf.get("breakdown", {})
                if breakdown:
                    import pandas as pd
                    bd_df = pd.DataFrame({
                        "Factor": list(breakdown.keys()),
                        "Value": list(breakdown.values())
                    })
                    st.bar_chart(bd_df.set_index("Factor"), height=160)

            st.caption(conf.get("explanation", ""))

        with tab5:
            tutor = d.get("tutor", {})

            st.markdown('<div class="section-title">💡 Hint</div>', unsafe_allow_html=True)
            hint = tutor.get("hint", "")
            if hint:
                hints = hint.split(" | ")
                for h in hints:
                    st.markdown(f'<div class="hint-box">{h}</div>', unsafe_allow_html=True)

            quiz_data = tutor.get("quiz")
            if quiz_data:
                st.divider()
                st.markdown('<div class="section-title">📝 Quiz Questions</div>', unsafe_allow_html=True)
                for qi, q_item in enumerate(quiz_data, 1):
                    with st.expander(f"Q{qi}: {q_item.get('question', '')}"):
                        st.markdown(f"**Type:** `{q_item.get('type', 'N/A')}`")
                        st.markdown(f"**Hint:** {q_item.get('hint', '')}")
                        if st.toggle(f"Show Answer", key=f"ans_{i}_{qi}"):
                            st.success(f"**Answer:** {q_item.get('answer', '')}")
            else:
                st.caption("Ask a question with 'quiz me on…' to generate quiz questions.")

        st.divider()

# ─── Empty state ───────────────────────────────────────────────
if not st.session_state.chat_history:
    st.markdown("""
    <div class='empty-state'>
        <div style='font-size:52px;margin-bottom:12px;'>🧠</div>
        <h3>Ask anything to get started</h3>
        <p style='color:#a78bfa;font-size:14px;margin-top:8px;'>
            Try: <code>Explain photosynthesis</code> &nbsp;or&nbsp; <code>Quiz me on Newton's laws</code>
        </p>
        <div style='display:flex;justify-content:center;gap:10px;margin-top:24px;flex-wrap:wrap;'>
            <span style='background:linear-gradient(135deg,#ede9fe,#e0e7ff);color:#5b21b6;border:1px solid #c4b5fd;border-radius:20px;padding:6px 16px;font-size:13px;font-weight:500;'>📘 Tutor mode</span>
            <span style='background:linear-gradient(135deg,#ecfdf5,#d1fae5);color:#065f46;border:1px solid #6ee7b7;border-radius:20px;padding:6px 16px;font-size:13px;font-weight:500;'>✅ Quiz mode</span>
            <span style='background:linear-gradient(135deg,#eff6ff,#dbeafe);color:#1e40af;border:1px solid #bfdbfe;border-radius:20px;padding:6px 16px;font-size:13px;font-weight:500;'>⚡ Simple mode</span>
        </div>
    </div>
    """, unsafe_allow_html=True)