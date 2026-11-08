"""CSR Console — landing page prototype.

Run:
    streamlit run docs/prototype/app.py

This is a UX prototype: all data is mock data and no backend is connected.
Visual language follows docs/DESIGN.md; navigation follows EXPERIENCE.md.
"""

from __future__ import annotations

import datetime as dt

import streamlit as st

st.set_page_config(
    page_title="CSR Console — Overview",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Design tokens (mirrors docs/DESIGN.md)
# ---------------------------------------------------------------------------

CSS = """
:root {
  --primary-50:  #f8f9fa;
  --primary-100: #f1f3f5;
  --primary-200: #e9ecef;
  --primary-300: #dee2e6;
  --primary-500: #212b36;
  --primary-600: #1a232e;
  --primary-700: #131a22;
  --primary-800: #0d1115;
  --primary-900: #050505;
  --primary-950: #020203;
  --success-100: #d4edda;
  --success-500: #28a745;
  --success-600: #1e7e34;
  --warning-100: #fff3cd;
  --warning-500: #ffc107;
  --danger-100:  #f8d7da;
  --danger-500:  #dc3545;
  --danger-600:  #bd2130;
  --info-100:    #d1ecf1;
  --info-500:    #17a2b8;
  --info-600:    #117a8b;
  --text-primary:   #212b36;
  --text-secondary: #6b7280;
  --text-inverse:   #f1f3f5;
  --bg-page:  #f1f3f5;
  --bg-card:  #ffffff;
}

/* ---- Streamlit shell overrides ---- */
.stApp { background: var(--bg-page); }
.block-container {
  padding-top: 2.2rem;
  padding-bottom: 2rem;
  max-width: 1240px;
}
[data-testid="stSidebar"] {
  background: var(--bg-card);
  border-right: 1px solid var(--primary-300);
}
[data-testid="stSidebar"] > div:first-child { padding-top: 1.4rem; }
[data-testid="stHeader"] { background: transparent; }
[data-testid="stToolbar"] { display: none; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }

div[data-testid="stTextInput"] input {
  height: 48px;
  border-radius: 10px;
  border: 1px solid var(--primary-300);
  background: var(--bg-card);
  padding: 0 14px;
  font-size: 0.92rem;
  color: var(--text-primary);
}
div[data-testid="stTextInput"] input:focus {
  border-color: var(--primary-600);
  box-shadow: 0 0 0 3px rgba(26, 35, 46, 0.12);
}
div[data-testid="stButton"] > button {
  border-radius: 8px;
  min-height: 46px;
  font-weight: 600;
  border: 1px solid var(--primary-300);
  background: var(--bg-card);
  color: var(--primary-600);
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
  transition: all 0.15s ease;
}
div[data-testid="stButton"] > button:hover {
  border-color: #ced4da;
  background: var(--primary-50);
  color: var(--primary-800);
}
div[data-testid="stButton"] > button[kind="primary"],
div[data-testid="stButton"] > button[data-testid="baseButton-primary"] {
  background: var(--primary-600);
  color: var(--text-inverse);
  border-color: var(--primary-600);
}
div[data-testid="stButton"] > button[kind="primary"]:hover,
div[data-testid="stButton"] > button[data-testid="baseButton-primary"]:hover {
  background: var(--primary-700);
  color: #ffffff;
}
div[data-testid="stRadio"] label { font-size: 0.92rem; color: var(--text-primary); }
[data-testid="stSidebar"] div[role="radiogroup"] label {
  padding: 6px 8px;
  border-radius: 7px;
}
[data-testid="stSidebar"] div[role="radiogroup"] label:hover { background: var(--primary-100); }

/* ---- Brand / sidebar ---- */
.brand { display: flex; align-items: center; gap: 10px; padding: 0 0 14px; }
.brand-mark {
  width: 38px; height: 38px; border-radius: 10px;
  background: var(--primary-600); color: var(--text-inverse);
  display: flex; align-items: center; justify-content: center;
  flex: 0 0 auto;
}
.brand-name { font-size: 1rem; font-weight: 700; color: var(--primary-800); line-height: 1.1; }
.brand-sub { font-size: 0.72rem; color: var(--text-secondary); }
.nav-label {
  font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.12em;
  color: var(--text-secondary); font-weight: 700; margin: 4px 0 2px;
}
.side-divider { height: 1px; background: var(--primary-200); margin: 16px 0; }
.user-card {
  display: flex; align-items: center; gap: 10px;
  padding: 10px; border: 1px solid var(--primary-300);
  border-radius: 10px; background: var(--bg-card);
}
.user-avatar {
  width: 34px; height: 34px; border-radius: 50%;
  background: var(--primary-600); color: var(--text-inverse);
  display: flex; align-items: center; justify-content: center;
  font-size: 0.72rem; font-weight: 700; flex: 0 0 auto;
}
.user-name { font-size: 0.84rem; font-weight: 700; color: var(--primary-800); }
.user-role { font-size: 0.72rem; color: var(--text-secondary); }
.proto-tag {
  display: inline-block; font-size: 0.6rem; font-weight: 800;
  letter-spacing: 0.1em; text-transform: uppercase;
  color: var(--info-600); background: var(--info-100);
  padding: 3px 7px; border-radius: 5px; margin-bottom: 6px;
}
.proto-note { font-size: 0.72rem; color: var(--text-secondary); line-height: 1.45; }

/* ---- Hero ---- */
.hero {
  display: flex; justify-content: space-between; align-items: flex-end;
  gap: 24px; flex-wrap: wrap; margin-bottom: 14px;
}
.eyebrow {
  font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.13em;
  color: var(--info-600); font-weight: 700;
}
.hero h1 {
  font-size: 2rem; line-height: 1.2; margin: 0.3rem 0 0.35rem;
  color: var(--primary-800); font-weight: 700; letter-spacing: -0.02em;
}
.hero-sub { font-size: 0.95rem; color: #4b5563; max-width: 62ch; margin: 0; }
.hero-meta { display: flex; gap: 8px; flex-wrap: wrap; }
.pill {
  font-size: 0.76rem; font-weight: 600; color: var(--primary-600);
  background: var(--bg-card); border: 1px solid var(--primary-300);
  padding: 6px 11px; border-radius: 999px; white-space: nowrap;
}
.pill-role { background: var(--primary-600); color: var(--text-inverse); border-color: var(--primary-600); }

/* ---- Metric cards ---- */
.metric-card {
  background: var(--bg-card); border: 1px solid var(--primary-300);
  border-radius: 11px; padding: 15px 16px; min-height: 118px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
}
.metric-head { display: flex; align-items: center; justify-content: space-between; gap: 8px; }
.metric-label {
  font-size: 0.7rem; letter-spacing: 0.05em; text-transform: uppercase;
  color: var(--text-secondary); font-weight: 700;
}
.metric-icon {
  width: 32px; height: 32px; border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
}
.metric-icon.up { background: var(--success-100); color: var(--success-600); }
.metric-icon.warn { background: var(--warning-100); color: #7a5c00; }
.metric-icon.info { background: var(--info-100); color: var(--info-600); }
.metric-icon.danger { background: var(--danger-100); color: var(--danger-600); }
.metric-value {
  font-size: 1.85rem; font-weight: 700; color: var(--primary-800);
  line-height: 1.1; margin-top: 11px; letter-spacing: -0.02em;
}
.metric-delta { font-size: 0.78rem; margin-top: 5px; font-weight: 600; }
.metric-delta.up { color: var(--success-600); }
.metric-delta.warn { color: #7a5c00; }
.metric-delta.info { color: var(--info-600); }
.metric-delta.danger { color: var(--danger-600); }

/* ---- Panels ---- */
.panel {
  background: var(--bg-card); border: 1px solid var(--primary-300);
  border-radius: 12px; padding: 16px 18px 10px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
}
.panel-head {
  display: flex; align-items: flex-start; justify-content: space-between;
  gap: 12px; margin-bottom: 4px;
}
.panel-title { font-size: 1rem; font-weight: 700; color: var(--primary-800); margin: 0; }
.panel-sub { font-size: 0.78rem; color: var(--text-secondary); margin: 2px 0 0; }

/* ---- Queue ---- */
.queue-row {
  display: grid; grid-template-columns: 1fr auto; gap: 10px;
  padding: 11px 0; border-top: 1px solid var(--primary-100); align-items: center;
}
.queue-row:first-of-type { border-top: none; }
.queue-id {
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: 0.74rem; color: var(--info-600); font-weight: 700;
}
.queue-title { font-size: 0.9rem; color: var(--primary-600); font-weight: 600; margin-top: 2px; }
.queue-meta { font-size: 0.76rem; color: var(--text-secondary); margin-top: 2px; }
.queue-right { display: flex; flex-direction: column; align-items: flex-end; gap: 6px; }
.queue-amount { font-size: 0.84rem; font-weight: 700; color: var(--primary-800); }

/* ---- Badges ---- */
.badge {
  display: inline-flex; align-items: center; font-size: 0.68rem; font-weight: 700;
  padding: 3px 9px; border-radius: 999px; letter-spacing: 0.03em; white-space: nowrap;
}
.badge-success { background: var(--success-100); color: var(--success-600); }
.badge-warning { background: var(--warning-100); color: #7a5c00; }
.badge-info { background: var(--info-100); color: var(--info-600); }
.badge-danger { background: var(--danger-100); color: var(--danger-600); }
.badge-neutral { background: var(--primary-200); color: var(--primary-600); }

/* ---- Shipments ---- */
.ship-row { padding: 9px 0; border-top: 1px solid var(--primary-100); }
.ship-row:first-of-type { border-top: none; }
.ship-top { display: flex; justify-content: space-between; gap: 8px; font-size: 0.82rem; }
.ship-carrier { font-weight: 700; color: var(--primary-600); }
.ship-status { color: var(--text-secondary); }
.track {
  height: 7px; background: var(--primary-200); border-radius: 999px;
  margin-top: 8px; overflow: hidden;
}
.track-fill { height: 100%; border-radius: 999px; }
.track-fill.success { background: var(--success-500); }
.track-fill.info { background: var(--info-500); }
.track-fill.warning { background: var(--warning-500); }

/* ---- Activity ---- */
.activity-row {
  display: flex; gap: 10px; padding: 8px 0;
  border-top: 1px solid var(--primary-100); align-items: flex-start;
}
.activity-row:first-of-type { border-top: none; }
.avatar {
  width: 30px; height: 30px; border-radius: 50%;
  background: var(--primary-200); color: var(--primary-600);
  display: flex; align-items: center; justify-content: center;
  font-size: 0.68rem; font-weight: 800; flex: 0 0 auto;
}
.activity-text { font-size: 0.82rem; color: var(--primary-600); line-height: 1.35; }
.activity-text b { font-weight: 700; }
.activity-time { font-size: 0.7rem; color: var(--text-secondary); margin-top: 2px; }

/* ---- Pipeline ---- */
.pipeline-bar {
  display: flex; height: 14px; border-radius: 999px; overflow: hidden;
  background: var(--primary-200); margin: 8px 0 12px;
}
.pipeline-legend {
  display: flex; flex-wrap: wrap; gap: 8px 18px;
  font-size: 0.78rem; color: #4b5563;
}
.legend-dot { width: 9px; height: 9px; border-radius: 50%; display: inline-block; margin-right: 6px; }

/* ---- Empty / stub ---- */
.empty-row {
  padding: 26px 8px; text-align: center; font-size: 0.86rem;
  color: var(--text-secondary);
}
.stub-card {
  background: var(--bg-card); border: 1px dashed #ced4da;
  border-radius: 14px; padding: 54px 24px; text-align: center;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
}
.stub-icon {
  width: 54px; height: 54px; border-radius: 14px;
  background: var(--primary-100); color: var(--text-secondary);
  display: flex; align-items: center; justify-content: center;
  margin: 0 auto 14px;
}
.stub-title { font-size: 1.08rem; font-weight: 700; color: var(--primary-800); margin: 0 0 6px; }
.stub-sub { font-size: 0.88rem; color: var(--text-secondary); max-width: 48ch; margin: 0 auto; }

/* ---- Footer ---- */
.footer {
  border-top: 1px solid var(--primary-200); margin-top: 24px; padding-top: 13px;
  font-size: 0.74rem; color: var(--text-secondary);
  display: flex; justify-content: space-between; gap: 12px; flex-wrap: wrap;
}
.footer b { color: var(--primary-600); }

@media (max-width: 768px) {
  .hero h1 { font-size: 1.6rem; }
  .block-container { padding-left: 1rem; padding-right: 1rem; }
}
"""

st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Inline SVG icons (Lucide-style, currentColor)
# ---------------------------------------------------------------------------

ICONS = {
    "life-buoy": '<circle cx="12" cy="12" r="10"/><path d="m4.93 4.93 4.24 4.24"/><path d="m14.83 9.17 4.24-4.24"/><path d="m14.83 14.83 4.24 4.24"/><path d="m9.17 14.83-4.24 4.24"/><circle cx="12" cy="12" r="4"/>',
    "package": '<path d="m7.5 4.27 9 5.15"/><path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/><path d="m3.3 7 8.7 5 8.7-5"/><path d="M12 22V12"/>',
    "rotate-ccw": '<path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/>',
    "truck": '<path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2"/><path d="M15 18H9"/><path d="M19 18h2a1 1 0 0 0 1-1v-3.65a1 1 0 0 0-.22-.624l-3.48-4.35A1 1 0 0 0 17.52 8H14"/><circle cx="17" cy="18" r="2"/><circle cx="7" cy="18" r="2"/>',
    "dollar-sign": '<line x1="12" x2="12" y1="2" y2="22"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>',
    "search": '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
    "bell": '<path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/>',
    "plus": '<path d="M5 12h14"/><path d="M12 5v14"/>',
    "user-plus": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><line x1="19" x2="19" y1="8" y2="14"/><line x1="22" x2="16" y1="11" y2="11"/>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "credit-card": '<rect width="20" height="14" x="2" y="5" rx="2"/><line x1="2" x2="22" y1="10" y2="10"/>',
    "shield": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/>',
    "home": '<path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>',
    "settings": '<path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
    "check-circle": '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/>',
    "alert-triangle": '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><path d="M12 9v4"/><path d="M12 17h.01"/>',
    "arrow-up-right": '<path d="M7 7h10v10"/><path d="M7 17 17 7"/>',
}


def icon(name: str, size: int = 20) -> str:
    path = ICONS.get(name, ICONS["package"])
    return (
        f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
        'stroke="currentColor" stroke-width="2" stroke-linecap="round" '
        f'stroke-linejoin="round" aria-hidden="true">{path}</svg>'
    )


# ---------------------------------------------------------------------------
# Mock data
# ---------------------------------------------------------------------------

NAV_ITEMS = [
    "Overview",
    "Customers",
    "Orders",
    "Shipments",
    "Billing",
    "Users",
    "Settings",
]

NAV_ICONS = {
    "Overview": "home",
    "Customers": "users",
    "Orders": "package",
    "Shipments": "truck",
    "Billing": "credit-card",
    "Users": "shield",
    "Settings": "settings",
}

METRICS = [
    {"label": "Open orders", "value": "24", "delta": "+4 today", "kind": "info", "icon": "package"},
    {"label": "Returns to review", "value": "3", "delta": "1 overdue", "kind": "warn", "icon": "rotate-ccw"},
    {"label": "In transit", "value": "12", "delta": "+6 since 9am", "kind": "up", "icon": "truck"},
    {"label": "Revenue today", "value": "$4,820", "delta": "+12.4% vs avg", "kind": "up", "icon": "dollar-sign"},
]

QUEUE = [
    {
        "id": "RET-1042",
        "title": "Jordan Lee · Gold",
        "meta": "Wrong size · Order ORD-8790",
        "amount": "$86.00",
        "badge": ("Eligible", "success"),
    },
    {
        "id": "RET-1041",
        "title": "Priya Shah · Standard",
        "meta": "Damaged on arrival · Order ORD-8771",
        "amount": "$142.50",
        "badge": ("Review", "warning"),
    },
    {
        "id": "ORD-8821",
        "title": "Acme Co. · Enterprise",
        "meta": "4 line items · Awaiting fulfilment",
        "amount": "$1,240.00",
        "badge": ("Processing", "info"),
    },
    {
        "id": "ORD-8819",
        "title": "Marta Ruiz · Gold",
        "meta": "Payment authorisation pending",
        "amount": "$320.00",
        "badge": ("On hold", "danger"),
    },
]

SHIPMENTS = [
    {"carrier": "FedEx", "tracking": "1Z 999 AA1 01", "status": "Out for delivery", "pct": 82, "kind": "info"},
    {"carrier": "UPS", "tracking": "9400 1102 8875", "status": "In transit · Memphis", "pct": 54, "kind": "warning"},
    {"carrier": "DHL", "tracking": "JD01 4452 9930", "status": "Delivered", "pct": 100, "kind": "success"},
]

ACTIVITY = [
    {"initials": "MC", "text": "<b>Maya Chen</b> created order <b>ORD-8824</b>", "time": "4 min ago"},
    {"initials": "SY", "text": "System flagged <b>RET-1042</b> as eligible for return", "time": "12 min ago"},
    {"initials": "LP", "text": "<b>Leo Park</b> marked shipment delivered", "time": "38 min ago"},
    {"initials": "AD", "text": "<b>Admin</b> invited <b>sam@acme.co</b> as User Manager", "time": "1 hr ago"},
]

PIPELINE = [
    {"label": "Processing", "count": 18, "pct": 20.0, "color": "var(--info-500)"},
    {"label": "Completed", "count": 64, "pct": 71.1, "color": "var(--success-500)"},
    {"label": "Returned", "count": 5, "pct": 5.6, "color": "var(--warning-500)"},
    {"label": "Cancelled", "count": 3, "pct": 3.3, "color": "var(--danger-500)"},
]


# ---------------------------------------------------------------------------
# Render helpers
# ---------------------------------------------------------------------------


def greeting() -> str:
    hour = dt.datetime.now().hour
    if hour < 12:
        return "Good morning"
    if hour < 18:
        return "Good afternoon"
    return "Good evening"


def render_sidebar() -> str:
    with st.sidebar:
        st.markdown(
            f"""
            <div class="brand">
              <div class="brand-mark">{icon("life-buoy", 21)}</div>
              <div>
                <div class="brand-name">CSR Console</div>
                <div class="brand-sub">Support operations</div>
              </div>
            </div>
            <div class="nav-label">Workspace</div>
            """,
            unsafe_allow_html=True,
        )
        nav = st.radio("Navigation", NAV_ITEMS, label_visibility="collapsed")
        st.markdown('<div class="side-divider"></div>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="user-card">
              <div class="user-avatar">DA</div>
              <div>
                <div class="user-name">Dali</div>
                <div class="user-role">CSR · Operator</div>
              </div>
            </div>
            <div class="side-divider"></div>
            <div class="proto-tag">Prototype</div>
            <div class="proto-note">
              Mock data only. No API connected. Design tokens from
              <b>DESIGN.md</b>; navigation from <b>EXPERIENCE.md</b>.
            </div>
            """,
            unsafe_allow_html=True,
        )
    return nav


def render_hero() -> None:
    today = dt.date.today().strftime("%A, %d %b %Y")
    st.markdown(
        f"""
        <div class="hero">
          <div>
            <div class="eyebrow">Support operations · Overview</div>
            <h1>{greeting()}, Dali</h1>
            <p class="hero-sub">
              Here is what needs your attention across customers, orders,
              returns and shipments today.
            </p>
          </div>
          <div class="hero-meta">
            <span class="pill">{today}</span>
            <span class="pill pill-role">CSR · Operator</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_search() -> str:
    return st.text_input(
        "Search",
        placeholder="Search customers, orders or tracking numbers…",
        label_visibility="collapsed",
    )


def render_metrics() -> None:
    cols = st.columns(4, gap="medium")
    for col, metric in zip(cols, METRICS):
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                  <div class="metric-head">
                    <span class="metric-label">{metric["label"]}</span>
                    <span class="metric-icon {metric["kind"]}">{icon(metric["icon"], 17)}</span>
                  </div>
                  <div class="metric-value">{metric["value"]}</div>
                  <div class="metric-delta {metric["kind"]}">{metric["delta"]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_quick_actions() -> None:
    actions = [
        ("Add customer", "user-plus", False),
        ("Create order", "plus", True),
        ("Start return", "rotate-ccw", False),
        ("Track shipment", "truck", False),
        ("Invite user", "shield", False),
    ]
    cols = st.columns(len(actions), gap="small")
    for col, (label, _icon_name, primary) in zip(cols, actions):
        with col:
            if st.button(
                label,
                key=f"quick-{label}",
                use_container_width=True,
                type="primary" if primary else "secondary",
            ):
                st.toast(f"Prototype: the “{label}” screen is not built yet.")


def render_queue(query: str) -> None:
    q = query.strip().lower()
    rows = [
        row
        for row in QUEUE
        if not q
        or q in row["id"].lower()
        or q in row["title"].lower()
        or q in row["meta"].lower()
    ]

    body = ""
    for row in rows:
        badge_label, badge_kind = row["badge"]
        body += f"""
        <div class="queue-row">
          <div>
            <div class="queue-id">{row["id"]}</div>
            <div class="queue-title">{row["title"]}</div>
            <div class="queue-meta">{row["meta"]}</div>
          </div>
          <div class="queue-right">
            <span class="badge badge-{badge_kind}">{badge_label}</span>
            <span class="queue-amount">{row["amount"]}</span>
          </div>
        </div>
        """
    if not rows:
        body = (
            '<div class="empty-row">No matches. Try a different name, order '
            "number or tracking number.</div>"
        )

    st.markdown(
        f"""
        <div class="panel">
          <div class="panel-head">
            <div>
              <p class="panel-title">Priority queue</p>
              <p class="panel-sub">Returns and orders that need a decision</p>
            </div>
            <span class="badge badge-neutral">{len(rows)} shown</span>
          </div>
          {body}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_shipments() -> None:
    body = ""
    for ship in SHIPMENTS:
        body += f"""
        <div class="ship-row">
          <div class="ship-top">
            <span><span class="ship-carrier">{ship["carrier"]}</span>
              <span class="ship-status"> · {ship["tracking"]}</span></span>
            <span class="ship-status">{ship["status"]}</span>
          </div>
          <div class="track">
            <div class="track-fill {ship["kind"]}" style="width:{ship["pct"]}%"></div>
          </div>
        </div>
        """
    st.markdown(
        f"""
        <div class="panel">
          <div class="panel-head">
            <div>
              <p class="panel-title">Shipment pulse</p>
              <p class="panel-sub">Live tracking across carriers</p>
            </div>
            <span class="badge badge-info">{len(SHIPMENTS)} active</span>
          </div>
          {body}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_activity() -> None:
    body = ""
    for item in ACTIVITY:
        body += f"""
        <div class="activity-row">
          <div class="avatar">{item["initials"]}</div>
          <div>
            <div class="activity-text">{item["text"]}</div>
            <div class="activity-time">{item["time"]}</div>
          </div>
        </div>
        """
    st.markdown(
        f"""
        <div class="panel">
          <div class="panel-head">
            <div>
              <p class="panel-title">Recent activity</p>
              <p class="panel-sub">Team actions in the last hour</p>
            </div>
          </div>
          {body}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_pipeline() -> None:
    segments = "".join(
        f'<div style="width:{seg["pct"]}%;background:{seg["color"]}"></div>'
        for seg in PIPELINE
    )
    legend = "".join(
        f'<span><span class="legend-dot" style="background:{seg["color"]}"></span>'
        f'{seg["label"]} · {seg["count"]}</span>'
        for seg in PIPELINE
    )
    st.markdown(
        f"""
        <div class="panel">
          <div class="panel-head">
            <div>
              <p class="panel-title">Order pipeline</p>
              <p class="panel-sub">90 orders across the fulfilment lifecycle</p>
            </div>
            <span class="badge badge-neutral">Last 7 days</span>
          </div>
          <div class="pipeline-bar">{segments}</div>
          <div class="pipeline-legend">{legend}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_footer() -> None:
    st.markdown(
        """
        <div class="footer">
          <span><b>CSR Console</b> · UX prototype · mock data</span>
          <span>Tokens: DESIGN.md · Flows: EXPERIENCE.md · Not connected to the API</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_overview() -> None:
    render_hero()
    query = render_search()
    st.write("")
    render_metrics()
    st.write("")
    render_quick_actions()
    st.write("")

    left, right = st.columns([1.55, 1], gap="large")
    with left:
        render_queue(query)
    with right:
        render_shipments()
        st.write("")
        render_activity()

    st.write("")
    render_pipeline()
    render_footer()


def render_stub(nav: str) -> None:
    st.markdown(
        f"""
        <div class="hero">
          <div>
            <div class="eyebrow">Support operations · {nav}</div>
            <h1>{nav}</h1>
            <p class="hero-sub">This area of the console shell is mapped in
            EXPERIENCE.md and ready for the next prototype pass.</p>
          </div>
          <div class="hero-meta"><span class="pill pill-role">Prototype</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div class="stub-card">
          <div class="stub-icon">{icon(NAV_ICONS.get(nav, "package"), 26)}</div>
          <p class="stub-title">{nav} screen</p>
          <p class="stub-sub">
            The landing page is the focus of this prototype. Use the sidebar to
            return to Overview, or wire this screen to the matching user flow.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Back to Overview"):
        st.info("Select Overview in the sidebar to return to the landing page.")


# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------

nav = render_sidebar()

if nav == "Overview":
    render_overview()
else:
    render_stub(nav)
