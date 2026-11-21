import os
import random
import subprocess
import sys
from datetime import datetime
import pandas as pd
import streamlit as st

# -----------------------------
# 1. PAGE CONFIG & EARTHY UI THEME
# -----------------------------
st.set_page_config(
    page_title="ShopImpact | Conscious Shopping Dashboard",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

def apply_theme(high_contrast: bool = False):
    if high_contrast:
        bg_main = "#0F1713"
        text_color = "#F4F8F5"
        muted_text = "#C4D6CB"
        accent = "#74C69D"
        border = "#40916C"
        metric_bg = "#132019"
    else:
        bg_main = "#F5F2EB"      # Warm sand / linen background
        text_color = "#1B3022"   # Deep forest text
        muted_text = "#4A6353"
        accent = "#2D6A4F"       # Earthy forest green
        border = "#D5E0D7"
        metric_bg = "#EDF4EE"

    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');

        html, body, [class*="css"] {{
            font-family: 'Plus Jakarta Sans', sans-serif;
        }}
        .stApp {{
            background-color: {bg_main};
            color: {text_color};
        }}
        .hero-banner {{
            background: linear-gradient(135deg, #1B4332 0%, #2D6A4F 55%, #40916C 100%);
            color: #FFFFFF;
            padding: 24px 28px;
            border-radius: 16px;
            margin-bottom: 18px;
            box-shadow: 0 6px 16px rgba(27, 67, 50, 0.14);
        }}
        .hero-banner h1 {{
            color: #FFFFFF !important;
            font-size: 2rem;
            font-weight: 800;
            margin: 0;
        }}
        .hero-banner p {{
            color: #E6F4EA;
            font-size: 1rem;
            margin: 8px 0 0 0;
        }}
        .kpi-box {{
            background-color: {metric_bg};
            border: 1px solid {border};
            border-radius: 14px;
            padding: 16px 18px;
            text-align: center;
        }}
        .kpi-label {{
            font-size: 0.9rem;
            font-weight: 600;
            color: {muted_text};
            margin-bottom: 4px;
        }}
        .kpi-value {{
            font-size: 1.75rem;
            font-weight: 800;
            color: {accent};
        }}
        .badge-pill {{
            display: inline-block;
            background-color: #D8F3DC;
            color: #1B4332;
            font-weight: 700;
            padding: 8px 14px;
            border-radius: 999px;
            margin: 5px 6px 5px 0;
            border: 1px solid #74C69D;
            font-size: 0.92rem;
        }}
        .swap-item {{
            background-color: {metric_bg};
            border-left: 4px solid {accent};
            color: {text_color};
            padding: 10px 14px;
            border-radius: 8px;
            margin-bottom: 8px;
            font-size: 0.96rem;
        }}
        .stButton > button {{
            border-radius: 10px;
            font-weight: 700;
            padding: 0.55rem 1.1rem;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# ------------------------------------
# 2. CURATED DATA & PYTHON LOGIC
# ------------------------------------
IMPACT_MULTIPLIERS = {
    "T-Shirts & Tops": 0.015,
    "Jeans & Trousers": 0.020,
    "Footwear (Sneakers / Shoes)": 0.024,
    "Thrift & Second-Hand Finds": 0.003,
    "Electronics & Accessories": 0.022,
    "Daily Essentials & Bags": 0.010,
}

IMPACT_LABELS = {
    "T-Shirts & Tops": "Moderate–High Impact",
    "Jeans & Trousers": "High Impact",
    "Footwear (Sneakers / Shoes)": "High Impact",
    "Thrift & Second-Hand Finds": "Very Low Impact (Eco Pick!)",
    "Electronics & Accessories": "High Impact",
    "Daily Essentials & Bags": "Low–Moderate Impact",
}

GREENER_ALTERNATIVES = {
    "T-Shirts & Tops": [
        "Thrift or second-hand tops (cuts footprint by ~80%)",
        "100% organic cotton or hemp tees from local ethical labels",
        "Clothing swap with friends before buying brand-new",
    ],
    "Jeans & Trousers": [
        "Second-hand / vintage denim stores",
        "Low-water recycled cotton denim brands",
        "Repairing or tailoring an existing pair",
    ],
    "Footwear (Sneakers / Shoes)": [
        "Sneakers made with recycled rubber & knit uppers",
        "Plant-based / vegan leather alternatives",
        "Resoling or deep-cleaning your current pair",
    ],
    "Thrift & Second-Hand Finds": [
        "Awesome choice! Thrifting keeps clothes in circulation longer.",
        "Share your thrift haul with friends to inspire low-impact habits.",
    ],
    "Electronics & Accessories": [
        "Certified refurbished devices with warranty",
        "Modular or repairable accessories",
        "Replacing a battery/cable instead of the whole gadget",
    ],
    "Daily Essentials & Bags": [
        "Reusable canvas, jute, or recycled-PET tote bags",
        "Refillable bottles, jars, and bulk packs",
        "Bamboo or stainless-steel everyday swaps",
    ],
}

ECO_TIPS = [
    "Did you know? Buying one second-hand garment saves around 2,000+ litres of water compared to making a new one.",
    "Bamboo grows rapidly without chemical pesticides, making it a great lower-impact everyday swap.",
    "Using the '30-wear test' before buying clothes helps avoid impulse fast-fashion waste.",
    "Extending the life of a phone or laptop by just 1 extra year lowers its annual carbon footprint by ~25%.",
    "Carrying a reusable tote bag replaces hundreds of single-use plastic bags every year.",
]

ECO_QUOTES = [
    "“We don’t need a handful of people doing zero waste perfectly. We need millions of people doing it imperfectly.” — Anne Marie Bonneau",
    "“The greatest threat to our planet is the belief that someone else will save it.” — Robert Swan",
    "“Buy less, choose well, make it last.” — Vivienne Westwood",
]

def calculate_co2_kg(product_type: str, price: float) -> float:
    multiplier = IMPACT_MULTIPLIERS.get(product_type, 0.012)
    return round(price * multiplier, 2)

def add_purchase(purchases: list, product_type: str, brand: str, price: float, purchase_date: datetime):
    co2_kg = calculate_co2_kg(product_type, price)
    purchases.append(
        {
            "product_type": product_type,
            "brand": brand.strip() if brand.strip() else "Local / Unspecified",
            "price": round(float(price), 2),
            "co2_kg": co2_kg,
            "date": purchase_date,
            "month": purchase_date.strftime("%Y-%m"),
        }
    )

def get_monthly_summary(purchases: list, month_str: str) -> dict:
    month_items = [p for p in purchases if p["month"] == month_str]
    total_spend = round(sum(p["price"] for p in month_items), 2)
    total_co2 = round(sum(p["co2_kg"] for p in month_items), 2)
    return {
        "items": month_items,
        "count": len(month_items),
        "total_spend": total_spend,
        "total_co2": total_co2,
    }

def evaluate_badges(monthly_co2: float, month_items: list) -> list:
    badges = []
    if len(month_items) >= 1 and monthly_co2 <= 12.0:
        badges.append("🌱 Eco Saver (CO₂ ≤ 12 kg)")
    if len(month_items) >= 3 and monthly_co2 <= 25.0:
        badges.append("🌍 Low Impact Shopper (3+ buys ≤ 25 kg)")
    eco_swaps = [
        p for p in month_items
        if p["product_type"] in ("Thrift & Second-Hand Finds", "Daily Essentials & Bags")
    ]
    if len(eco_swaps) >= 2:
        badges.append("♻️ Green Swap Champion (2+ Eco Picks)")
    return badges

# ----------------------------------------------------
# 3. TURTLE GRAPHICS GENERATOR (CLOUD-SAFE RENDERING)
# ----------------------------------------------------
def generate_turtle_visual(eco_level: str) -> str:
    out_png = f"turtle_{eco_level}.png"
    ps_file = f"turtle_{eco_level}.ps"

    turtle_script = f"""
import turtle

screen = turtle.Screen()
screen.setup(width=420, height=320)
screen.bgcolor("#F5F2EB")

t = turtle.Turtle()
t.hideturtle()
t.speed(0)

level = "{eco_level}"

if level == "leaf":
    t.penup()
    t.goto(0, -75)
    t.pendown()
    t.color("#1B4332", "#52B788")
    t.pensize(3)
    t.begin_fill()
    t.setheading(45)
    t.circle(105, 90)
    t.left(90)
    t.circle(105, 90)
    t.end_fill()
    t.color("#1B4332")
    t.penup()
    t.goto(0, -75)
    t.setheading(90)
    t.pendown()
    t.forward(148)
    t.penup()
    t.goto(0, -118)
    t.write("Eco Leaf Unlocked!", align="center", font=("Arial", 14, "bold"))

elif level == "badge":
    t.penup()
    t.goto(0, -65)
    t.pendown()
    t.color("#2D6A4F", "#B7E4C7")
    t.pensize(4)
    t.begin_fill()
    t.circle(80)
    t.end_fill()
    t.penup()
    t.goto(0, -45)
    t.pendown()
    t.color("#1B4332", "#74C69D")
    t.begin_fill()
    t.circle(60)
    t.end_fill()
    t.penup()
    t.goto(0, 8)
    t.color("#1B4332")
    t.write("ECO", align="center", font=("Arial", 18, "bold"))
    t.goto(0, -16)
    t.write("STAR", align="center", font=("Arial", 15, "bold"))
    t.goto(0, -118)
    t.write("Eco Saver Badge!", align="center", font=("Arial", 14, "bold"))

else:
    t.penup()
    t.goto(-10, -38)
    t.pendown()
    t.color("#5C4033", "#D4A373")
    t.pensize(3)
    t.begin_fill()
    t.circle(42)
    t.end_fill()
    toes = [(-36, 52, 12), (-11, 64, 11), (12, 61, 10), (31, 49, 9)]
    for x, y, r in toes:
        t.penup()
        t.goto(x, y)
        t.pendown()
        t.begin_fill()
        t.circle(r)
        t.end_fill()
    t.penup()
    t.goto(0, -118)
    t.color("#5C4033")
    t.write("Mindful Footprint Check", align="center", font=("Arial", 13, "bold"))

canvas = screen.getcanvas()
canvas.postscript(file="{ps_file}")
turtle.bye()
"""
    script_path = "_draw_turtle_tmp.py"
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(turtle_script)

    try:
        cmd = ["xvfb-run", "-a", sys.executable, script_path] if os.name != "nt" else [sys.executable, script_path]
        subprocess.run(cmd, check=True, timeout=10)
        from PIL import Image
        img = Image.open(ps_file)
        img.save(out_png, "PNG")
        return out_png
    except Exception:
        from PIL import Image, ImageDraw
        img = Image.new("RGB", (420, 290), "#F5F2EB")
        draw = ImageDraw.Draw(img)
        if eco_level == "leaf":
            draw.ellipse([130, 45, 290, 205], fill="#52B788", outline="#1B4332", width=4)
            draw.line([210, 45, 210, 220], fill="#1B4332", width=4)
            draw.text((135, 240), "Eco Leaf Unlocked!", fill="#1B4332")
        elif eco_level == "badge":
            draw.ellipse([125, 40, 295, 210], fill="#B7E4C7", outline="#2D6A4F", width=5)
            draw.text((175, 115), "ECO STAR", fill="#1B4332")
            draw.text((140, 240), "Eco Saver Badge!", fill="#1B4332")
        else:
            draw.ellipse([155, 80, 255, 190], fill="#D4A373", outline="#5C4033", width=4)
            for tx in [155, 182, 208, 232]:
                draw.ellipse([tx, 48, tx + 20, 70], fill="#D4A373", outline="#5C4033", width=2)
            draw.text((120, 240), "Mindful Footprint Check", fill="#5C4033")
        img.save(out_png, "PNG")
        return out_png

# ------------------------------------
# 4. SESSION STATE INITIALIZATION
# ------------------------------------
if "purchases" not in st.session_state:
    st.session_state.purchases = []
if "current_tip" not in st.session_state:
    st.session_state.current_tip = random.choice(ECO_TIPS)
if "current_quote" not in st.session_state:
    st.session_state.current_quote = random.choice(ECO_QUOTES)

# ------------------------------------
# 5. SIDEBAR: CONTROLS & QUICK DEMO
# ------------------------------------
with st.sidebar:
    st.markdown("## 🌱 ShopImpact Studio")
    high_contrast = st.toggle("High-Contrast / Dark Mode", value=False)
    apply_theme(high_contrast)

    st.divider()
    st.markdown("### ⚡ Quick Actions")
    if st.button("Load Sample Purchases", use_container_width=True):
        now = datetime.now()
        samples = [
            ("Thrift & Second-Hand Finds", "Local Thrift", 450, now),
            ("Daily Essentials & Bags", "EcoCarry", 350, now),
            ("T-Shirts & Tops", "BasicWear", 850, now),
        ]
        for prod, br, pr, dt in samples:
            add_purchase(st.session_state.purchases, prod, br, pr, dt)
        st.session_state.current_tip = random.choice(ECO_TIPS)
        st.rerun()

    if st.button("New Eco Tip", use_container_width=True):
        st.session_state.current_tip = random.choice(ECO_TIPS)
        st.session_state.current_quote = random.choice(ECO_QUOTES)
        st.rerun()

    if st.button("Clear All Purchases", use_container_width=True):
        st.session_state.purchases = []
        st.rerun()

    st.divider()
    st.markdown("### 📊 Impact Guide (per ₹1)")
    for k, v in IMPACT_MULTIPLIERS.items():
        st.caption(f"**{k}**: `{v}` kg CO₂")

# ------------------------------------
# 6. HERO HEADER
# ------------------------------------
st.markdown(
    """
    <div class="hero-banner">
        <h1>🌿 ShopImpact — Conscious Shopping Dashboard</h1>
        <p>Plan mindful purchases, see your live CO₂ footprint, discover greener swaps, and earn eco badges.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------
# 7. TOP PANEL: LOG PURCHASE + LIVE PREVIEW
# ------------------------------------
top_left, top_right = st.columns([1.45, 1.0], gap="large")

with top_left:
    with st.container(border=True):
        st.subheader("🛒 Log a Planned Purchase")

        c1, c2 = st.columns(2)
        with c1:
            product_type = st.selectbox("Product Type", list(IMPACT_MULTIPLIERS.keys()))
        with c2:
            brand = st.text_input("Brand Name", placeholder="e.g., Fabindia, Local Thrift, Nike")

        c3, c4 = st.columns(2)
        with c3:
            price = st.number_input("Price (₹)", min_value=1.0, value=500.0, step=50.0)
        with c4:
            p_date = st.date_input("Purchase Date", value=datetime.now().date())

        live_est = calculate_co2_kg(product_type, price)
        st.caption(
            f"Live Preview: **{IMPACT_LABELS[product_type]}** • Estimated CO₂ for this item: **{live_est} kg**"
        )

        if st.button("➕ Log Purchase", type="primary", use_container_width=True):
            dt_obj = datetime.combine(p_date, datetime.now().time())
            add_purchase(st.session_state.purchases, product_type, brand, price, dt_obj)
            st.session_state.current_tip = random.choice(ECO_TIPS)
            st.session_state.current_quote = random.choice(ECO_QUOTES)
            st.success(f"Added **{product_type}** (₹{price:,.0f}) — **{live_est} kg CO₂**")

with top_right:
    with st.container(border=True):
        st.subheader("🌱 Greener Alternatives")
        st.caption(f"Mindful options for **{product_type}**:")
        for alt in GREENER_ALTERNATIVES[product_type]:
            st.markdown(f'<div class="swap-item">✓ {alt}</div>', unsafe_allow_html=True)

# ------------------------------------------------
# 8. MAIN DASHBOARD & ECO COMPANION
# ------------------------------------------------
active_month = datetime.now().strftime("%Y-%m")
if st.session_state.purchases:
    available_months = sorted({p["month"] for p in st.session_state.purchases}, reverse=True)
    active_month = st.selectbox("📅 Monthly View", available_months, index=0)

summary = get_monthly_summary(st.session_state.purchases, active_month)
badges = evaluate_badges(summary["total_co2"], summary["items"])

dash_col, side_col = st.columns([2.1, 1.0], gap="large")

with dash_col:
    with st.container(border=True):
        st.subheader(f"📈 Monthly Impact Overview ({active_month})")

        k1, k2, k3 = st.columns(3)
        with k1:
            st.markdown(
                f'<div class="kpi-box"><div class="kpi-label">Items Logged</div><div class="kpi-value">{summary["count"]}</div></div>',
                unsafe_allow_html=True,
            )
        with k2:
            st.markdown(
                f'<div class="kpi-box"><div class="kpi-label">Total Monthly Spend</div><div class="kpi-value">₹{summary["total_spend"]:,.0f}</div></div>',
                unsafe_allow_html=True,
            )
        with k3:
            st.markdown(
                f'<div class="kpi-box"><div class="kpi-label">Estimated CO₂</div><div class="kpi-value">{summary["total_co2"]} kg</div></div>',
                unsafe_allow_html=True,
            )

        st.write("")
        if summary["items"]:
            tab_chart, tab_table = st.tabs(["📊 CO₂ Breakdown Chart", "🧾 Purchase History"])
            df = pd.DataFrame(summary["items"])

            with tab_chart:
                chart_df = df.groupby("product_type", as_index=False)["co2_kg"].sum()
                st.bar_chart(chart_df.set_index("product_type")["co2_kg"], color="#2D6A4F")

            with tab_table:
                display_df = df[["product_type", "brand", "price", "co2_kg", "month"]].rename(
                    columns={
                        "product_type": "Product Type",
                        "brand": "Brand",
                        "price": "Price (₹)",
                        "co2_kg": "Est. CO₂ (kg)",
                        "month": "Month",
                    }
                )
                st.dataframe(display_df, use_container_width=True, hide_index=True)
        else:
            st.info("No purchases logged for this month yet. Log a planned item above or click **Load Sample Purchases** in the sidebar!")

with side_col:
    with st.container(border=True):
        st.subheader("🐢 Turtle Eco Companion")

        if not summary["items"]:
            turtle_state = "leaf"
        elif len(badges) >= 2:
            turtle_state = "badge"
        elif summary["total_co2"] <= 20.0:
            turtle_state = "leaf"
        else:
            turtle_state = "footprint"

        img_path = generate_turtle_visual(turtle_state)
        st.image(img_path, use_container_width=True)

        st.markdown("#### 🏅 Earned Badges")
        if badges:
            badge_html = "".join([f'<span class="badge-pill">{b}</span>' for b in badges])
            st.markdown(badge_html, unsafe_allow_html=True)
        else:
            st.caption("Log low-impact or thrift items to unlock your first badge!")

        st.divider()
        st.info(f"💡 **Eco Tip:** {st.session_state.current_tip}")
        st.caption(f"✨ {st.session_state.current_quote}")
