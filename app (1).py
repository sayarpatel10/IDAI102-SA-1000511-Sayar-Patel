import os
import random
import subprocess
import sys
import uuid
from datetime import datetime, date
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import streamlit as st
# ==============================================================================
# 1. PAGE CONFIGURATION & THEME STYLING
# ==============================================================================
st.set_page_config(
    page_title="ShopImpact | Conscious Shopping Dashboard",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)
def apply_theme(high_contrast: bool = False):
    """
    Applies custom CSS styling for an inviting, accessible user interface.
    Supports a warm Earthy Sand palette and a High-Contrast Dark Mode.
    """
    if high_contrast:
        bg_main = "#0B130E"          # Deep obsidian forest
        card_bg = "#13231A"          # Dark moss card background
        card_border = "#2A593F"      # Emerald border
        text_color = "#F4F9F5"       # Crisp high-contrast white
        muted_text = "#A3C4B0"       # Soft sage
        accent = "#52B788"           # Bright mint accent
        accent_hover = "#74C69D"
        kpi_bg = "#182E22"
        badge_bg = "#1B4332"
        badge_text = "#D8F3DC"
        hero_grad = "linear-gradient(135deg, #081C15 0%, #1B4332 50%, #2D6A4F 100%)"
    else:
        bg_main = "#F7F5EE"          # Warm linen / earthy sand
        card_bg = "#FFFFFF"          # Pure white card
        card_border = "#DCE7DE"      # Subtle sage border
        text_color = "#162B1D"       # Deep pine text
        muted_text = "#4F6856"       # Muted forest slate
        accent = "#2D6A4F"           # Rich forest green
        accent_hover = "#1B4332"
        kpi_bg = "#EDF5EF"           # Light mint wash
        badge_bg = "#D8F3DC"
        badge_text = "#1B4332"
        hero_grad = "linear-gradient(135deg, #1B4332 0%, #2D6A4F 55%, #40916C 100%)"
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Outfit:wght@500;700;800&display=swap');
        html, body, [class*="css"], .stMarkdown {{
            font-family: 'Plus Jakarta Sans', sans-serif;
        }}
        .stApp {{
            background-color: {bg_main};
            color: {text_color};
        }}
        /* Hero Banner */
        .hero-banner {{
            background: {hero_grad};
            color: #FFFFFF !important;
            padding: 28px 32px;
            border-radius: 20px;
            margin-bottom: 22px;
            box-shadow: 0 10px 25px rgba(27, 67, 50, 0.18);
            position: relative;
            overflow: hidden;
        }}
        .hero-banner h1 {{
            font-family: 'Outfit', sans-serif;
            color: #FFFFFF !important;
            font-size: 2.2rem;
            font-weight: 800;
            margin: 0;
            letter-spacing: -0.5px;
        }}
        .hero-banner p {{
            color: #E2F2E7 !important;
            font-size: 1.05rem;
            margin: 10px 0 0 0;
            max-width: 850px;
            line-height: 1.5;
        }}
        /* Card Container */
        .eco-card {{
            background-color: {card_bg};
            border: 1px solid {card_border};
            border-radius: 16px;
            padding: 20px 22px;
            margin-bottom: 16px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }}
        .eco-card:hover {{
            box-shadow: 0 6px 18px rgba(0, 0, 0, 0.06);
        }}
        /* KPI Metric Box */
        .kpi-box {{
            background-color: {kpi_bg};
            border: 1px solid {card_border};
            border-radius: 14px;
            padding: 18px;
            text-align: center;
            height: 100%;
        }}
        .kpi-icon {{
            font-size: 1.5rem;
            margin-bottom: 4px;
        }}
        .kpi-label {{
            font-size: 0.85rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: {muted_text};
            margin-bottom: 6px;
        }}
        .kpi-value {{
            font-family: 'Outfit', sans-serif;
            font-size: 1.85rem;
            font-weight: 800;
            color: {accent};
            margin-bottom: 4px;
        }}
        .kpi-subtext {{
            font-size: 0.8rem;
            color: {muted_text};
        }}
        /* Badge Pill */
        .badge-pill {{
            display: inline-flex;
            align-items: center;
            background-color: {badge_bg};
            color: {badge_text};
            font-weight: 700;
            padding: 8px 16px;
            border-radius: 999px;
            margin: 5px 6px 5px 0;
            border: 1px solid {card_border};
            font-size: 0.9rem;
            box-shadow: 0 2px 6px rgba(0,0,0,0.04);
        }}
        /* Swap Recommendation Item */
        .swap-item {{
            background-color: {kpi_bg};
            border-left: 4px solid {accent};
            color: {text_color};
            padding: 12px 16px;
            border-radius: 8px;
            margin-bottom: 10px;
            font-size: 0.95rem;
            line-height: 1.4;
        }}
        /* Carbon Tag Indicators */
        .tag-eco {{
            background-color: #D8F3DC;
            color: #1B4332;
            padding: 3px 10px;
            border-radius: 12px;
            font-weight: 700;
            font-size: 0.8rem;
        }}
        .tag-mod {{
            background-color: #FEF3C7;
            color: #92400E;
            padding: 3px 10px;
            border-radius: 12px;
            font-weight: 700;
            font-size: 0.8rem;
        }}
        .tag-high {{
            background-color: #FEE2E2;
            color: #991B1B;
            padding: 3px 10px;
            border-radius: 12px;
            font-weight: 700;
            font-size: 0.8rem;
        }}
        /* Buttons & Forms */
        .stButton > button {{
            border-radius: 12px;
            font-weight: 700;
            padding: 0.55rem 1.25rem;
            transition: all 0.2s ease;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
# ==============================================================================
# 2. CURATED DATA MODELS & DOMAIN LOGIC
# ==============================================================================
# CO2 multipliers: estimated kg CO2 emitted per ₹1 spent
IMPACT_MULTIPLIERS = {
    "T-Shirts, Tops & Blouses": 0.015,
    "Jeans, Denim & Trousers": 0.020,
    "Footwear (Sneakers & Leather Shoes)": 0.024,
    "Fast Fashion Dresses & Jackets": 0.025,
    "Electronics, Gadgets & Cables": 0.022,
    "Single-Use & Packaged Goods": 0.018,
    "Daily Essentials & Reusable Bags": 0.008,
    "Certified Sustainable / Organic Brands": 0.005,
    "Thrift & Second-Hand Finds": 0.002,
}
IMPACT_LABELS = {
    "T-Shirts, Tops & Blouses": ("Moderate Impact", "tag-mod"),
    "Jeans, Denim & Trousers": ("High Impact (Water & Carbon)", "tag-high"),
    "Footwear (Sneakers & Leather Shoes)": ("High Impact", "tag-high"),
    "Fast Fashion Dresses & Jackets": ("Very High Impact", "tag-high"),
    "Electronics, Gadgets & Cables": ("High Impact (E-Waste & Energy)", "tag-high"),
    "Single-Use & Packaged Goods": ("Moderate Impact", "tag-mod"),
    "Daily Essentials & Reusable Bags": ("Low Impact (Eco Essential)", "tag-eco"),
    "Certified Sustainable / Organic Brands": ("Very Low Impact (Ethical Choice)", "tag-eco"),
    "Thrift & Second-Hand Finds": ("Minimal Impact (Circular Champion)", "tag-eco"),
}
GREENER_ALTERNATIVES = {
    "T-Shirts, Tops & Blouses": [
        "🔄 Thrift or vintage tees (cuts manufacturing footprint by ~85%).",
        "🌿 Look for 100% GOTS certified organic cotton or hemp from ethical makers.",
        "🤝 Organize a clothing swap party with friends before ordering new fast fashion.",
        "🏷️ Check certified brands like Fabindia (handloom), Brown Boy, or No Nasties.",
    ],
    "Jeans, Denim & Trousers": [
        "👖 Second-hand / vintage denim: A single new pair of jeans consumes ~7,500L of water!",
        "✂️ Repair, tailor, or patch your existing jeans to double their lifespan.",
        "💧 Choose low-water, laser-treated denim brands (e.g. Mud Jeans, Levi's Water<Less).",
        "🧵 Opt for recycled cotton or linen trousers for warmer weather.",
    ],
    "Footwear (Sneakers & Leather Shoes)": [
        "👟 Try sneakers made from recycled ocean plastics, sugarcane EVA, or eucalyptus knit.",
        "🌱 Plant-based / vegan leather options (apple leather, Piñatex pineapple leather, cork).",
        "🥾 Resoling or deep-cleaning your favorite shoes instead of buying new pairs.",
        "🔍 Brands: Veja, Allbirds, Neeman's (merino wool/recycled PET), Paaduks.",
    ],
    "Fast Fashion Dresses & Jackets": [
        "👗 Rent occasion wear and party dresses from fashion rental platforms.",
        "🧣 Invest in timeless, durable capsule-wardrobe pieces made of natural fibers.",
        "♻️ Upcycle old sarees or fabrics into chic bespoke jackets and dresses.",
        "📦 Try pre-loved thrift platforms like Relove, FreeUp, or Suta pre-loved.",
    ],
    "Electronics, Gadgets & Cables": [
        "📱 Buy certified refurbished laptops and smartphones with warranty (Cashify, Apple Refurbished).",
        "🔌 Replace a degraded battery or frayed cable rather than discarding the whole device.",
        "🔋 Use modular or repairable electronics (like Fairphone or iFixit-compatible gadgets).",
        "♻️ Always safely drop decommissioned gadgets at e-waste recycling collection bins.",
    ],
    "Single-Use & Packaged Goods": [
        "🛍️ Carry a foldable jute or canvas tote bag in your everyday backpack.",
        "🧴 Choose refillable body washes, shampoo bars, and bulk-packaged pantry items.",
        "🥤 Carry a reusable stainless steel water bottle and thermal coffee tumbler.",
        "🌿 Swap plastic cling wrap for washable beeswax wraps or silicone bowl lids.",
    ],
    "Daily Essentials & Reusable Bags": [
        "🌟 Excellent mindful choice! Reusables prevent hundreds of single-use items from landfills.",
        "🧼 Choose compostable, plastic-free personal care items (bamboo toothbrush, bar soaps).",
        "🧺 Support local artisans and self-help groups making handwoven baskets and bags.",
    ],
    "Certified Sustainable / Organic Brands": [
        "✨ Supporting certified ethical labels incentivizes fair wages and clean supply chains.",
        "📜 Verify certifications like Fair Trade, OEKO-TEX, GOTS, or B-Corp.",
        "🌱 Keep wear frequency high: Even eco-fashion is best when loved for years!",
    ],
    "Thrift & Second-Hand Finds": [
        "🏆 Circular Economy Champion! Thrifting extends garment lifecycles and eliminates new factory emissions.",
        "📸 Share your thrift haul with friends to normalize pre-loved style over fast fashion.",
        "💫 Wash thrifted pieces gently in cold water and air-dry to keep them looking fresh.",
    ],
}
ECO_TIPS = [
    "💧 Producing a single cotton t-shirt requires approximately 2,700 litres of fresh water — enough for one person to drink for 900 days!",
    "👕 The '30-Wear Test': Before buying any garment, ask yourself: 'Will I wear this at least 30 times?' If not, skip it.",
    "📱 Extending the operational life of your smartphone or laptop by just 1 year reduces its annual carbon footprint by nearly 25%.",
    "👟 Washing your clothes in cold water and line-drying cuts laundry carbon emissions by up to 60% while protecting fabric fibers.",
    "♻️ Buying one second-hand or thrifted item saves around 85% of the carbon emissions compared to manufacturing a brand-new fast-fashion piece.",
    "🛍️ A single sturdy organic cotton or canvas tote bag can replace up to 500 single-use plastic bags over its lifetime.",
    "👖 Making one pair of denim jeans releases around 20–33 kg of CO₂ and uses roughly 7,500–10,000 litres of water during production.",
    "🥦 Food packaging waste accounts for over 35% of all consumer plastic. Choosing bulk dispensers and refill stations makes a massive dent.",
]
ECO_QUOTES = [
    "“We don’t need a handful of people doing zero waste perfectly. We need millions of people doing it imperfectly.” — Anne Marie Bonneau",
    "“Buy less, choose well, make it last.” — Vivienne Westwood",
    "“The greatest threat to our planet is the belief that someone else will save it.” — Robert Swan",
    "“There is no such thing as ‘away’. When we throw anything away it must go somewhere.” — Annie Leonard",
    "“Every time you spend money, you're casting a vote for the kind of world you want.” — Anna Lappé",
    "“The most sustainable garment is the one already in your wardrobe.” — Orsola de Castro",
]
def calculate_co2_kg(product_type: str, price: float) -> float:
    """Calculates estimated CO2 footprint in kg based on curated multipliers."""
    multiplier = IMPACT_MULTIPLIERS.get(product_type, 0.012)
    return round(float(price) * multiplier, 2)
def calculate_equivalencies(co2_kg: float) -> dict:
    """Translates abstract CO2 kg numbers into tangible real-world metrics."""
    trees_needed = round(co2_kg / 1.75, 1) if co2_kg > 0 else 0.0
    car_km = round(co2_kg * 6.2, 1)
    smartphones = int(co2_kg * 120)
    return {
        "trees_needed": trees_needed,
        "car_km": car_km,
        "smartphones": smartphones,
    }
def add_purchase(
    purchases_list: list,
    product_type: str,
    brand: str,
    price: float,
    purchase_date: date,
    notes: str = "",
) -> dict:
    """Creates a new purchase record dictionary and appends it to the session list."""
    co2_kg = calculate_co2_kg(product_type, price)
    is_eco_pick = product_type in [
        "Thrift & Second-Hand Finds",
        "Certified Sustainable / Organic Brands",
        "Daily Essentials & Reusable Bags",
    ]
    new_item = {
        "id": str(uuid.uuid4())[:8],
        "product_type": product_type,
        "brand": brand.strip() if brand.strip() else "Unspecified / Local",
        "price": round(float(price), 2),
        "co2_kg": co2_kg,
        "date": purchase_date.strftime("%Y-%m-%d"),
        "month": purchase_date.strftime("%Y-%m"),
        "is_eco_pick": is_eco_pick,
        "notes": notes.strip(),
    }
    purchases_list.append(new_item)
    return new_item
def delete_purchase(purchases_list: list, item_id: str) -> bool:
    """Removes a purchase record by its unique ID."""
    for i, item in enumerate(purchases_list):
        if item.get("id") == item_id:
            purchases_list.pop(i)
            return True
    return False
def get_monthly_summary(purchases_list: list, month_str: str) -> dict:
    """Aggregates all purchases for a selected month."""
    items = [p for p in purchases_list if p.get("month") == month_str]
    count = len(items)
    total_spend = round(sum(p["price"] for p in items), 2)
    total_co2 = round(sum(p["co2_kg"] for p in items), 2)
    eco_items = [p for p in items if p.get("is_eco_pick", False)]
    eco_count = len(eco_items)
    eco_ratio = round((eco_count / count * 100), 1) if count > 0 else 0.0
    equiv = calculate_equivalencies(total_co2)
    return {
        "items": items,
        "count": count,
        "total_spend": total_spend,
        "total_co2": total_co2,
        "eco_count": eco_count,
        "eco_ratio": eco_ratio,
        "equivalencies": equiv,
    }
def evaluate_all_badges(monthly_summary: dict, total_purchases: list, carbon_budget: float) -> dict:
    """Evaluates earned badges vs available badges with criteria tracking."""
    items = monthly_summary["items"]
    m_co2 = monthly_summary["total_co2"]
    count = monthly_summary["count"]
    eco_count = monthly_summary["eco_count"]
    badges_catalog = [
        {
            "id": "starter",
            "name": "🌱 Eco Starter",
            "desc": "Logged your first conscious shopping item",
            "unlocked": len(total_purchases) >= 1,
            "status_text": "Completed! First step to mindfulness." if len(total_purchases) >= 1 else "Log 1 purchase to unlock",
        },
        {
            "id": "saver",
            "name": "🍃 Eco Saver",
            "desc": "Kept monthly carbon impact under 12 kg CO₂",
            "unlocked": count >= 1 and m_co2 <= 12.0,
            "status_text": f"Current: {m_co2} kg CO₂ (Target ≤ 12 kg)" if count >= 1 else "Log purchases this month",
        },
        {
            "id": "low_impact",
            "name": "🌍 Low Impact Shopper",
            "desc": "Logged 3+ purchases while keeping monthly CO₂ ≤ 25 kg",
            "unlocked": count >= 3 and m_co2 <= 25.0,
            "status_text": f"Items: {count}/3, CO₂: {m_co2} kg (Target ≤ 25 kg)",
        },
        {
            "id": "swap_champ",
            "name": "♻️ Green Swap Champion",
            "desc": "Logged 2 or more Eco/Thrift/Sustainable picks",
            "unlocked": eco_count >= 2,
            "status_text": f"Eco picks logged: {eco_count}/2",
        },
        {
            "id": "budget_master",
            "name": "🎯 Carbon Budget Master",
            "desc": f"Stayed within your monthly carbon goal (≤ {carbon_budget:.0f} kg)",
            "unlocked": count >= 1 and m_co2 <= carbon_budget,
            "status_text": f"Current: {m_co2} kg vs Budget: {carbon_budget} kg",
        },
        {
            "id": "guardian",
            "name": "🛡️ Conscious Guardian",
            "desc": "50% or more of your monthly purchases are eco-friendly",
            "unlocked": count >= 2 and (eco_count / count) >= 0.5,
            "status_text": f"Current Eco Ratio: {monthly_summary['eco_ratio']}% (Target ≥ 50%)",
        },
    ]
    unlocked_list = [b["name"] for b in badges_catalog if b["unlocked"]]
    return {
        "catalog": badges_catalog,
        "unlocked_names": unlocked_list,
        "unlocked_count": len(unlocked_list),
        "total_count": len(badges_catalog),
    }
# ==============================================================================
# 3. TURTLE GRAPHICS COMPANION (CLOUD-SAFE & HEADLESS-RESILIENT)
# ==============================================================================
def draw_turtle_with_pillow(eco_level: str, filename: str) -> str:
    """Renders companion artwork using Pillow with guaranteed headless uptime."""
    width, height = 440, 320
    bg_color = (247, 245, 238)
    img = Image.new("RGBA", (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    if eco_level == "leaf":
        draw.arc([190, 160, 250, 240], start=180, end=270, fill="#2D6A4F", width=6)
        draw.chord([120, 50, 320, 220], start=30, end=210, fill="#52B788", outline="#1B4332", width=4)
        draw.chord([120, 50, 320, 220], start=210, end=30, fill="#74C69D", outline="#1B4332", width=4)
        draw.line([130, 190, 310, 80], fill="#1B4332", width=4)
        draw.line([180, 160, 205, 130], fill="#1B4332", width=3)
        draw.line([225, 130, 250, 105], fill="#1B4332", width=3)
        draw.line([220, 135, 210, 175], fill="#1B4332", width=3)
        draw.ellipse([250, 120, 268, 138], fill="#A7E8BD", outline="#2D6A4F", width=2)
        draw.rectangle([70, 250, 370, 290], fill="#D8F3DC", outline="#52B788", width=2)
        draw.text((130, 260), "🌿 Eco Leaf Unlocked!", fill="#1B4332")
    elif eco_level == "badge":
        draw.polygon([(170, 170), (140, 255), (175, 235), (200, 255), (195, 170)], fill="#2D6A4F", outline="#1B4332")
        draw.polygon([(245, 170), (240, 255), (265, 235), (300, 255), (270, 170)], fill="#2D6A4F", outline="#1B4332")
        draw.ellipse([130, 35, 310, 215], fill="#B7E4C7", outline="#1B4332", width=6)
        draw.ellipse([155, 60, 285, 190], fill="#52B788", outline="#2D6A4F", width=4)
        star_points = [
            (220, 80), (229, 108), (258, 108), (235, 126),
            (244, 154), (220, 137), (196, 154), (205, 126),
            (182, 108), (211, 108)
        ]
        draw.polygon(star_points, fill="#FFD166", outline="#E09F3E", width=2)
        draw.rectangle([75, 255, 365, 298], fill="#1B4332", outline="#52B788", width=2)
        draw.text((140, 267), "⭐ ECO SAVER BADGE ⭐", fill="#FFFFFF")
    elif eco_level == "sprout":
        draw.ellipse([140, 90, 300, 250], fill="#A8DADC", outline="#1D3557", width=5)
        draw.chord([160, 110, 240, 190], start=45, end=270, fill="#52B788", outline="#1B4332", width=2)
        draw.chord([210, 140, 285, 230], start=0, end=180, fill="#52B788", outline="#1B4332", width=2)
        draw.line([220, 95, 220, 45], fill="#2D6A4F", width=6)
        draw.chord([180, 30, 220, 65], start=0, end=180, fill="#74C69D", outline="#1B4332", width=3)
        draw.chord([220, 25, 260, 60], start=180, end=360, fill="#74C69D", outline="#1B4332", width=3)
        draw.rectangle([65, 265, 375, 305], fill="#D8F3DC", outline="#2D6A4F", width=2)
        draw.text((120, 275), "🌍 Planet Guardian Champion", fill="#1B4332")
    else:
        draw.ellipse([175, 110, 265, 215], fill="#E9C46A", outline="#8A5A36", width=4)
        draw.ellipse([185, 65, 255, 135], fill="#E9C46A", outline="#8A5A36", width=4)
        toes = [(180, 42, 14), (200, 32, 16), (222, 34, 15), (242, 42, 13), (258, 55, 11)]
        for tx, ty, r in toes:
            draw.ellipse([tx, ty, tx + 2 * r, ty + 2 * r], fill="#E9C46A", outline="#8A5A36", width=3)
        draw.line([220, 140, 220, 100], fill="#2D6A4F", width=4)
        draw.chord([200, 95, 220, 115], start=0, end=180, fill="#74C69D", outline="#1B4332", width=2)
        draw.rectangle([70, 255, 370, 298], fill="#FDE2E4", outline="#C9184A", width=2)
        draw.text((125, 267), "👣 Mindful Footprint Check", fill="#8A5A36")
    img.save(filename, "PNG")
    return filename
def generate_turtle_visual(eco_level: str) -> str:
    """Attempts native turtle execution with seamless Pillow fallback."""
    out_png = f"turtle_{eco_level}.png"
    ps_file = f"turtle_{eco_level}.ps"
    script_path = "_draw_turtle_tmp.py"
    turtle_script = f"""
import turtle
try:
    screen = turtle.Screen()
    screen.setup(width=440, height=320)
    screen.bgcolor("#F7F5EE")
    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)
    level = "{eco_level}"
    if level == "leaf":
        t.penup(); t.goto(0, -75); t.pendown(); t.color("#1B4332", "#52B788"); t.pensize(4)
        t.begin_fill(); t.setheading(45); t.circle(105, 90); t.left(90); t.circle(105, 90); t.end_fill()
    elif level == "badge":
        t.penup(); t.goto(0, -65); t.pendown(); t.color("#2D6A4F", "#B7E4C7"); t.pensize(5)
        t.begin_fill(); t.circle(80); t.end_fill()
    canvas = screen.getcanvas()
    canvas.postscript(file="{ps_file}")
    turtle.bye()
except Exception:
    pass
"""
    try:
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(turtle_script)
        cmd = [sys.executable, script_path]
        subprocess.run(cmd, check=True, timeout=5)
        if os.path.exists(ps_file):
            img = Image.open(ps_file)
            img.save(out_png, "PNG")
            return out_png
    except Exception:
        pass
    return draw_turtle_with_pillow(eco_level, out_png)
# ==============================================================================
# 4. SESSION STATE INITIALIZATION
# ==============================================================================
if "purchases" not in st.session_state:
    st.session_state.purchases = []
if "current_tip" not in st.session_state:
    st.session_state.current_tip = random.choice(ECO_TIPS)
if "current_quote" not in st.session_state:
    st.session_state.current_quote = random.choice(ECO_QUOTES)
if "carbon_budget" not in st.session_state:
    st.session_state.carbon_budget = 25.0
if "spend_budget" not in st.session_state:
    st.session_state.spend_budget = 5000.0
if "show_balloons" not in st.session_state:
    st.session_state.show_balloons = False
# ==============================================================================
# 5. SIDEBAR: CONTROLS, PROFILE PRESETS & BUDGET TARGETS
# ==============================================================================
with st.sidebar:
    st.markdown("## 🌿 ShopImpact Studio")
    st.caption("Conscious Shopping & Carbon Footprint Assistant")
    high_contrast = st.toggle("♿ High-Contrast / Dark Mode", value=False)
    apply_theme(high_contrast)
    st.divider()
    st.markdown("### 🎯 Monthly Eco Budgets")
    st.caption("Set your personal monthly ceiling:")
    carbon_budget = st.slider(
        "CO₂ Ceiling (kg / month)",
        min_value=5.0,
        max_value=100.0,
        value=float(st.session_state.carbon_budget),
        step=5.0,
        help="Recommended mindful target is ≤ 25 kg CO₂/month.",
    )
    st.session_state.carbon_budget = carbon_budget
    spend_budget = st.slider(
        "Spending Limit (₹ / month)",
        min_value=1000.0,
        max_value=25000.0,
        value=float(st.session_state.spend_budget),
        step=500.0,
    )
    st.session_state.spend_budget = spend_budget
    st.divider()
    st.markdown("### ⚡ Quick Demo Profiles")
    st.caption("Populate realistic scenarios with one click:")
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🌱 Eco Saver", use_container_width=True):
            today = date.today()
            st.session_state.purchases = []
            add_purchase(st.session_state.purchases, "Thrift & Second-Hand Finds", "Vintage Vault", 450, today, "Oversized denim jacket")
            add_purchase(st.session_state.purchases, "Daily Essentials & Reusable Bags", "EcoCarry Co", 299, today, "Organic jute tote")
            add_purchase(st.session_state.purchases, "Certified Sustainable / Organic Brands", "No Nasties", 1200, today, "Organic hemp tee")
            st.session_state.current_tip = random.choice(ECO_TIPS)
            st.toast("Loaded Eco Saver Demo Haul! 🌿", icon="✨")
            st.rerun()
    with col_btn2:
        if st.button("⚠️ Fast Fashion", use_container_width=True):
            today = date.today()
            st.session_state.purchases = []
            add_purchase(st.session_state.purchases, "Fast Fashion Dresses & Jackets", "UltraTrend", 2400, today, "Polyester party dress")
            add_purchase(st.session_state.purchases, "Jeans, Denim & Trousers", "FastDenim", 1800, today, "Distressed skinny jeans")
            add_purchase(st.session_state.purchases, "Footwear (Sneakers & Leather Shoes)", "SoleVibe", 3500, today, "Synthetic leather sneakers")
            st.toast("Loaded Fast-Fashion Haul Demo! 🚨", icon="⚠️")
            st.rerun()
    if st.button("⚖️ Balanced Student Shopper", use_container_width=True):
        today = date.today()
        st.session_state.purchases = []
        add_purchase(st.session_state.purchases, "Thrift & Second-Hand Finds", "Local Thrift Store", 350, today, "Graphic tee")
        add_purchase(st.session_state.purchases, "T-Shirts, Tops & Blouses", "Everyday Basics", 699, today, "Cotton work shirt")
        add_purchase(st.session_state.purchases, "Single-Use & Packaged Goods", "Supermarket", 400, today, "Snack multipacks")
        st.toast("Loaded Balanced Shopper Profile!", icon="📊")
        st.rerun()
    if st.button("🗑️ Clear All Purchases", use_container_width=True):
        st.session_state.purchases = []
        st.toast("All purchase history cleared.", icon="🧹")
        st.rerun()
    st.divider()
    st.markdown("### 📚 Carbon Multiplier Guide")
    with st.expander("View Curated Factors"):
        for item_name, factor in IMPACT_MULTIPLIERS.items():
            st.markdown(f"- **{item_name}**:<br>`{factor}` kg CO₂ per ₹1", unsafe_allow_html=True)
# ==============================================================================
# 6. HERO HEADER SECTION
# ==============================================================================
st.markdown(
    """
    <div class="hero-banner">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap;">
            <div>
                <h1>🌿 ShopImpact — Conscious Shopping Companion</h1>
                <p>
                    Transform everyday buying into mindful climate action. Log planned purchases, track your live CO₂ footprint,
                    discover greener alternatives, and celebrate sustainable habits with interactive badges and Turtle graphics.
                </p>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
if st.session_state.show_balloons:
    st.balloons()
    st.session_state.show_balloons = False
# ==============================================================================
# 7. MAIN INTERACTIVE WORKSPACE (TABBED ARCHITECTURE)
# ==============================================================================
tab_log, tab_simulator, tab_dashboard, tab_history, tab_companion, tab_wisdom = st.tabs([
    "🛒 Log & Plan Purchase",
    "🔄 Greener Swap Simulator",
    "📊 Monthly Impact Dashboard",
    "🧾 History & Data Management",
    "🐢 Turtle Companion & Badges",
    "💡 Eco Wisdom & Living Hub",
])
# ------------------------------------------------------------------------------
# TAB 1: LOG & PLAN PURCHASE
# ------------------------------------------------------------------------------
with tab_log:
    col_input, col_preview = st.columns([1.35, 1.0], gap="large")
    with col_input:
        with st.container(border=True):
            st.markdown("### 🛍️ Plan or Log an Item")
            st.caption("Enter product details to preview environmental cost before buying.")
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                selected_prod = st.selectbox("Product Category", list(IMPACT_MULTIPLIERS.keys()), index=0)
            with col_p2:
                brand_input = st.text_input("Brand / Store Name", placeholder="e.g. Fabindia, Thrift, H&M, Nike")
            col_p3, col_p4 = st.columns(2)
            with col_p3:
                price_input = st.number_input("Item Price (₹)", min_value=1.0, max_value=200000.0, value=799.0, step=50.0)
            with col_p4:
                date_input = st.date_input("Purchase / Planned Date", value=date.today())
            st.caption("Quick Price Presets:")
            preset_cols = st.columns(5)
            quick_prices = [299, 499, 999, 1999, 3999]
            for i, p_val in enumerate(quick_prices):
                if preset_cols[i].button(f"₹{p_val}", use_container_width=True):
                    price_input = float(p_val)
            notes_input = st.text_input("Notes or Tags (Optional)", placeholder="e.g., Bought for college event, 100% recycled cotton")
            est_co2 = calculate_co2_kg(selected_prod, price_input)
            label_text, label_class = IMPACT_LABELS[selected_prod]
            eq = calculate_equivalencies(est_co2)
            st.markdown(
                f"""
                <div style="background-color: #F0F7F2; border-left: 4px solid #2D6A4F; padding: 12px 16px; border-radius: 8px; margin: 16px 0;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: 700; color: #1B4332;">⚡ Instant Preview</span>
                        <span class="{label_class}">{label_text}</span>
                    </div>
                    <div style="margin-top: 6px; font-size: 1.15rem; font-weight: 800; color: #2D6A4F;">
                        Estimated Footprint: {est_co2} kg CO₂
                    </div>
                    <div style="font-size: 0.85rem; color: #4F6856; margin-top: 4px;">
                        🚗 Approx. <b>{eq['car_km']} km</b> driven in a petrol car • 🌳 Takes <b>{eq['trees_needed']} tree-months</b> to absorb
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("➕ Confirm & Log Purchase", type="primary", use_container_width=True):
                new_item = add_purchase(st.session_state.purchases, selected_prod, brand_input, price_input, date_input, notes_input)
                st.session_state.current_tip = random.choice(ECO_TIPS)
                st.session_state.current_quote = random.choice(ECO_QUOTES)
                if new_item["is_eco_pick"]:
                    st.session_state.show_balloons = True
                    st.toast("🎉 Awesome! You logged a sustainable choice!", icon="🌟")
                else:
                    st.toast(f"Logged {selected_prod} (₹{price_input:,.0f})", icon="✅")
                st.rerun()
    with col_preview:
        with st.container(border=True):
            st.markdown("### 🌿 Recommended Greener Swaps")
            st.caption(f"Mindful alternatives for **{selected_prod}**:")
            for alt in GREENER_ALTERNATIVES[selected_prod]:
                st.markdown(f'<div class="swap-item">{alt}</div>', unsafe_allow_html=True)
            st.info("💡 **Pro-Tip:** Pausing 24 hours before buying non-essential items eliminates over 70% of impulse buying regret.")
# ------------------------------------------------------------------------------
# TAB 2: GREENER SWAP SIMULATOR
# ------------------------------------------------------------------------------
with tab_simulator:
    with st.container(border=True):
        st.markdown("### 🔄 Conscious Swap Simulator")
        st.write("Simulate your decision to see the immediate environmental and financial dividend of choosing a greener swap!")
        sim_col1, sim_col2 = st.columns(2, gap="large")
        with sim_col1:
            st.markdown("#### ❌ Standard Conventional Choice")
            conv_prod = st.selectbox(
                "Conventional Item",
                ["Fast Fashion Dresses & Jackets", "Jeans, Denim & Trousers", "Footwear (Sneakers & Leather Shoes)", "T-Shirts, Tops & Blouses", "Electronics, Gadgets & Cables"],
                key="conv_prod",
            )
            conv_price = st.number_input("Estimated Brand-New Price (₹)", min_value=100.0, value=2500.0, step=100.0, key="conv_price")
            conv_co2 = calculate_co2_kg(conv_prod, conv_price)
            st.metric("Conventional CO₂ Footprint", f"{conv_co2} kg CO₂")
        with sim_col2:
            st.markdown("#### ✅ Greener / Circular Alternative")
            eco_prod = st.selectbox(
                "Greener Swap Choice",
                ["Thrift & Second-Hand Finds", "Certified Sustainable / Organic Brands", "Daily Essentials & Reusable Bags"],
                key="eco_prod",
            )
            eco_price = st.number_input("Alternative Price (₹)", min_value=50.0, value=800.0, step=50.0, key="eco_price")
            eco_co2 = calculate_co2_kg(eco_prod, eco_price)
            st.metric("Greener Choice Footprint", f"{eco_co2} kg CO₂")
        co2_saved = round(max(0.0, conv_co2 - eco_co2), 2)
        money_saved = round(max(0.0, conv_price - eco_price), 2)
        pct_saved = round((co2_saved / conv_co2 * 100), 1) if conv_co2 > 0 else 0.0
        equiv_saved = calculate_equivalencies(co2_saved)
        st.divider()
        st.markdown("#### 🌟 Your Environmental Dividend")
        res1, res2, res3, res4 = st.columns(4)
        with res1:
            st.markdown(f'<div class="kpi-box"><div class="kpi-icon">📉</div><div class="kpi-label">CO₂ Prevented</div><div class="kpi-value">{co2_saved} kg</div><div class="kpi-subtext">{pct_saved}% reduction</div></div>', unsafe_allow_html=True)
        with res2:
            st.markdown(f'<div class="kpi-box"><div class="kpi-icon">💰</div><div class="kpi-label">Money Saved</div><div class="kpi-value">₹{money_saved:,.0f}</div><div class="kpi-subtext">Direct wallet relief</div></div>', unsafe_allow_html=True)
        with res3:
            st.markdown(f'<div class="kpi-box"><div class="kpi-icon">🚗</div><div class="kpi-label">Car Travel Avoided</div><div class="kpi-value">{equiv_saved["car_km"]} km</div><div class="kpi-subtext">In petrol emissions</div></div>', unsafe_allow_html=True)
        with res4:
            st.markdown(f'<div class="kpi-box"><div class="kpi-icon">🌳</div><div class="kpi-label">Tree-Months Spared</div><div class="kpi-value">{equiv_saved["trees_needed"]}</div><div class="kpi-subtext">Planting equivalent</div></div>', unsafe_allow_html=True)
        st.write("")
        if st.button("✨ Log This Greener Swap to My Dashboard", use_container_width=True):
            add_purchase(st.session_state.purchases, eco_prod, "Greener Swap Alternative", eco_price, date.today(), f"Swapped from {conv_prod} (Saved {co2_saved} kg CO₂)")
            st.session_state.show_balloons = True
            st.toast("Greener swap logged successfully!", icon="🌱")
            st.rerun()
# ------------------------------------------------------------------------------
# TAB 3: MONTHLY IMPACT DASHBOARD
# ------------------------------------------------------------------------------
with tab_dashboard:
    current_month_str = date.today().strftime("%Y-%m")
    all_months = sorted({p["month"] for p in st.session_state.purchases}, reverse=True) if st.session_state.purchases else [current_month_str]
    col_m1, col_m2 = st.columns([1.5, 2.5])
    with col_m1:
        selected_month = st.selectbox("📅 Select Month to Review", all_months, index=0)
    summary = get_monthly_summary(st.session_state.purchases, selected_month)
    carbon_limit = st.session_state.carbon_budget
    spend_limit = st.session_state.spend_budget
    co2_pct = min(100.0, (summary["total_co2"] / carbon_limit * 100)) if carbon_limit > 0 else 0.0
    spend_pct = min(100.0, (summary["total_spend"] / spend_limit * 100)) if spend_limit > 0 else 0.0
    st.write("")
    kpi_c1, kpi_c2, kpi_c3, kpi_c4 = st.columns(4)
    with kpi_c1:
        st.markdown(f'<div class="kpi-box"><div class="kpi-icon">📦</div><div class="kpi-label">Items Logged</div><div class="kpi-value">{summary["count"]}</div><div class="kpi-subtext">{summary["eco_count"]} eco picks</div></div>', unsafe_allow_html=True)
    with kpi_c2:
        st.markdown(f'<div class="kpi-box"><div class="kpi-icon">💳</div><div class="kpi-label">Monthly Spending</div><div class="kpi-value">₹{summary["total_spend"]:,.0f}</div><div class="kpi-subtext">Budget: ₹{spend_limit:,.0f}</div></div>', unsafe_allow_html=True)
    with kpi_c3:
        status_color = "#2D6A4F" if summary["total_co2"] <= carbon_limit else "#D90429"
        st.markdown(f'<div class="kpi-box"><div class="kpi-icon">☁️</div><div class="kpi-label">Carbon Footprint</div><div class="kpi-value" style="color: {status_color};">{summary["total_co2"]} kg</div><div class="kpi-subtext">Ceiling: {carbon_limit:.0f} kg CO₂</div></div>', unsafe_allow_html=True)
    with kpi_c4:
        st.markdown(f'<div class="kpi-box"><div class="kpi-icon">🌿</div><div class="kpi-label">Eco-Pick Ratio</div><div class="kpi-value">{summary["eco_ratio"]}%</div><div class="kpi-subtext">Sustainable & circular buys</div></div>', unsafe_allow_html=True)
    st.write("")
    with st.container(border=True):
        st.markdown("#### 🎯 Budget & Eco Target Tracking")
        b_c1, b_c2 = st.columns(2)
        with b_c1:
            st.write(f"**Carbon Footprint Budget:** `{summary['total_co2']} / {carbon_limit:.0f} kg CO₂` ({co2_pct:.1f}%)")
            st.progress(co2_pct / 100.0)
            if summary["total_co2"] > carbon_limit:
                st.warning(f"⚠️ Exceeded monthly carbon ceiling by {round(summary['total_co2'] - carbon_limit, 1)} kg CO₂.")
            else:
                st.caption(f"✅ Remaining carbon buffer: **{round(carbon_limit - summary['total_co2'], 1)} kg CO₂**.")
        with b_c2:
            st.write(f"**Monthly Spending Budget:** `₹{summary['total_spend']:,.0f} / ₹{spend_limit:,.0f}` ({spend_pct:.1f}%)")
            st.progress(spend_pct / 100.0)
            if summary["total_spend"] > spend_limit:
                st.warning(f"⚠️ Exceeded monthly spending budget by ₹{round(summary['total_spend'] - spend_limit, 0):,.0f}.")
            else:
                st.caption(f"✅ Remaining spending buffer: **₹{round(spend_limit - summary['total_spend'], 0):,.0f}**.")
    if summary["items"]:
        df_month = pd.DataFrame(summary["items"])
        chart_col1, chart_col2 = st.columns(2)
        with chart_col1:
            with st.container(border=True):
                st.markdown("#### 📊 CO₂ Impact by Category (kg)")
                chart_df = df_month.groupby("product_type", as_index=False)["co2_kg"].sum().sort_values(by="co2_kg", ascending=False)
                st.bar_chart(chart_df.set_index("product_type")["co2_kg"], color="#2D6A4F", use_container_width=True)
        with chart_col2:
            with st.container(border=True):
                st.markdown("#### 💰 Spend Distribution by Category (₹)")
                spend_df = df_month.groupby("product_type", as_index=False)["price"].sum().sort_values(by="price", ascending=False)
                st.bar_chart(spend_df.set_index("product_type")["price"], color="#D4A373", use_container_width=True)
        eq = summary["equivalencies"]
        st.markdown(
            f"""
            <div style="background-color: #EDF5EF; border: 1px solid #74C69D; border-radius: 14px; padding: 18px 24px; margin-top: 10px;">
                <h4 style="color: #1B4332; margin: 0 0 8px 0;">🌍 Real-World Environmental Context</h4>
                <div style="font-size: 0.95rem; color: #2D6A4F; line-height: 1.6;">
                    • Driving equivalent: <b>{eq['car_km']} km</b> driven in an average petrol passenger car.<br>
                    • Tree sequestration: It will take roughly <b>{eq['trees_needed']} mature tree-months</b> to absorb this footprint.<br>
                    • Energy equivalent: Equal to fully charging <b>{eq['smartphones']:,} smartphones</b>.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.info("💡 No purchases logged for this month yet. Use **Log & Plan Purchase** or click **🌱 Eco Saver** in the sidebar to populate data!")
# ------------------------------------------------------------------------------
# TAB 4: HISTORY & DATA MANAGEMENT
# ------------------------------------------------------------------------------
with tab_history:
    with st.container(border=True):
        st.markdown("### 🧾 Purchase History & Management")
        st.caption("Review, search, filter, and manage all your logged conscious shopping entries.")
        if st.session_state.purchases:
            df_all = pd.DataFrame(st.session_state.purchases)
            f_col1, f_col2, f_col3 = st.columns([1.5, 1.5, 1.0])
            with f_col1:
                search_query = st.text_input("🔍 Search Brand or Notes", placeholder="e.g. Fabindia, thrift...")
            with f_col2:
                filter_cat = st.selectbox("Filter Category", ["All Categories"] + list(IMPACT_MULTIPLIERS.keys()))
            with f_col3:
                sort_by = st.selectbox("Sort By", ["Date (Newest)", "Price (High-Low)", "CO₂ (High-Low)"])
            filtered_df = df_all.copy()
            if search_query:
                filtered_df = filtered_df[
                    filtered_df["brand"].str.contains(search_query, case=False, na=False)
                    | filtered_df["notes"].str.contains(search_query, case=False, na=False)
                ]
            if filter_cat != "All Categories":
                filtered_df = filtered_df[filtered_df["product_type"] == filter_cat]
            if sort_by == "Date (Newest)":
                filtered_df = filtered_df.sort_values(by="date", ascending=False)
            elif sort_by == "Price (High-Low)":
                filtered_df = filtered_df.sort_values(by="price", ascending=False)
            elif sort_by == "CO₂ (High-Low)":
                filtered_df = filtered_df.sort_values(by="co2_kg", ascending=False)
            view_cols = ["date", "product_type", "brand", "price", "co2_kg", "is_eco_pick", "notes"]
            clean_display_df = filtered_df[view_cols].rename(
                columns={
                    "date": "Date",
                    "product_type": "Category",
                    "brand": "Brand",
                    "price": "Price (₹)",
                    "co2_kg": "Est. CO₂ (kg)",
                    "is_eco_pick": "Eco Pick?",
                    "notes": "Notes",
                }
            )
            st.dataframe(clean_display_df, use_container_width=True, hide_index=True)
            act_col1, act_col2 = st.columns([1.5, 2.0])
            with act_col1:
                csv_data = filtered_df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="📥 Export Purchases to CSV",
                    data=csv_data,
                    file_name=f"shopimpact_purchases_{date.today().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True,
                )
            with act_col2:
                item_options = {
                    f"{p['date']} - {p['product_type']} ({p['brand']}, ₹{p['price']}) [ID: {p['id']}]": p["id"]
                    for p in st.session_state.purchases
                }
                del_selection = st.selectbox("Select Item to Remove", list(item_options.keys()))
                if st.button("🗑️ Remove Selected Item", use_container_width=True):
                    del_id = item_options[del_selection]
                    delete_purchase(st.session_state.purchases, del_id)
                    st.toast("Item removed from your records.", icon="🗑️")
                    st.rerun()
        else:
            st.info("No purchases recorded yet. Start by logging an item or loading a demo preset!")
# ------------------------------------------------------------------------------
# TAB 5: TURTLE COMPANION & BADGES
# ------------------------------------------------------------------------------
with tab_companion:
    t_col1, t_col2 = st.columns([1.2, 1.8], gap="large")
    active_month = date.today().strftime("%Y-%m")
    summary = get_monthly_summary(st.session_state.purchases, active_month)
    badge_eval = evaluate_all_badges(summary, st.session_state.purchases, st.session_state.carbon_budget)
    if not summary["items"]:
        turtle_state = "leaf"
        state_title = "🌱 Eco Leaf (New Beginning)"
        state_desc = "Ready to start logging mindful purchases."
    elif badge_eval["unlocked_count"] >= 3 or (summary["count"] >= 3 and summary["total_co2"] <= 15.0):
        turtle_state = "badge"
        state_title = "⭐ Eco Star Badge Unlocked!"
        state_desc = "Outstanding habit! You are maintaining an exceptionally low carbon footprint."
    elif summary["eco_ratio"] >= 40.0:
        turtle_state = "sprout"
        state_title = "🌍 Planet Guardian Sprout"
        state_desc = "Superb! Over 40% of your items are second-hand or certified eco-picks."
    elif summary["total_co2"] <= st.session_state.carbon_budget:
        turtle_state = "leaf"
        state_title = "🌿 Healthy Eco Leaf"
        state_desc = "You are currently within your personal carbon ceiling."
    else:
        turtle_state = "footprint"
        state_title = "👣 Mindful Footprint Check"
        state_desc = "Carbon ceiling exceeded. Explore greener alternatives above to bring footprint down!"
    with t_col1:
        with st.container(border=True):
            st.markdown("### 🐢 Turtle Eco Companion")
            st.caption(f"Current State: **{state_title}**")
            st.write(state_desc)
            img_path = generate_turtle_visual(turtle_state)
            st.image(img_path, use_container_width=True)
            with st.expander("🎨 Test All Turtle Visual States"):
                manual_level = st.selectbox(
                    "Switch Graphic Style",
                    ["leaf", "badge", "sprout", "footprint"],
                    format_func=lambda x: {
                        "leaf": "🌿 Eco Leaf",
                        "badge": "⭐ Eco Saver Badge",
                        "sprout": "🌍 Planet Guardian Sprout",
                        "footprint": "👣 Mindful Footprint",
                    }[x],
                )
                if st.button("Render Selected Graphic"):
                    test_img = generate_turtle_visual(manual_level)
                    st.image(test_img, use_container_width=True)
    with t_col2:
        with st.container(border=True):
            st.markdown(f"### 🏅 Sustainable Milestone Badges ({badge_eval['unlocked_count']}/{badge_eval['total_count']} Unlocked)")
            st.caption("Earn badges as you make mindful purchases and stay within low-impact limits.")
            for b in badge_eval["catalog"]:
                if b["unlocked"]:
                    st.markdown(
                        f"""
                        <div style="background-color: #D8F3DC; border: 1px solid #74C69D; border-radius: 12px; padding: 12px 16px; margin-bottom: 10px;">
                            <div style="font-weight: 800; color: #1B4332; font-size: 1.05rem;">{b['name']} <span style="font-size: 0.8rem; background: #52B788; color: white; padding: 2px 8px; border-radius: 999px; margin-left: 8px;">UNLOCKED</span></div>
                            <div style="font-size: 0.88rem; color: #2D6A4F; margin-top: 3px;">{b['desc']}</div>
                            <div style="font-size: 0.78rem; color: #1B4332; margin-top: 4px; font-weight: 600;">✓ {b['status_text']}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f"""
                        <div style="background-color: transparent; border: 1px dashed #C4D6CB; border-radius: 12px; padding: 12px 16px; margin-bottom: 10px; opacity: 0.85;">
                            <div style="font-weight: 700; color: #6C757D; font-size: 1.0rem;">🔒 {b['name']}</div>
                            <div style="font-size: 0.85rem; color: #6C757D; margin-top: 3px;">{b['desc']}</div>
                            <div style="font-size: 0.78rem; color: #8A9A86; margin-top: 4px;">• {b['status_text']}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
# ------------------------------------------------------------------------------
# TAB 6: ECO WISDOM & LIVING HUB
# ------------------------------------------------------------------------------
with tab_wisdom:
    w_col1, w_col2 = st.columns(2, gap="large")
    with w_col1:
        with st.container(border=True):
            st.markdown("### 💡 Daily Conscious Tip")
            st.info(st.session_state.current_tip)
            if st.button("🎲 Get Another Eco Tip", use_container_width=True):
                st.session_state.current_tip = random.choice(ECO_TIPS)
                st.rerun()
            st.divider()
            st.markdown("### ✨ Sustainability Thought")
            st.markdown(f"> *{st.session_state.current_quote}*")
            if st.button("💬 Get New Quote", use_container_width=True):
                st.session_state.current_quote = random.choice(ECO_QUOTES)
                st.rerun()
    with w_col2:
        with st.container(border=True):
            st.markdown("### 📋 The 30-Wear Test Checklist")
            st.write("Before purchasing any new fashion item, verify its mindful longevity:")
            chk1 = st.checkbox("Can I pair this item with at least 3 things I already own?", value=True)
            chk2 = st.checkbox("Will I still feel happy wearing this a year from today?", value=True)
            chk3 = st.checkbox("Is the material durable, repairable, and breathable?")
            chk4 = st.checkbox("Did I search if I could thrift or borrow it first?")
            total_checked = sum([chk1, chk2, chk3, chk4])
            if total_checked == 4:
                st.success("🌟 4/4! This item passes the 30-wear mindful test with flying colors.")
            elif total_checked >= 2:
                st.warning("⚠️ 2–3/4: Consider sleeping on it for 24 hours before buying.")
            else:
                st.error("🚨 0–1/4: High risk of impulse buying regret. Consider skipping!")
# ==============================================================================
# 8. FOOTER & ATTRIBUTION
# ==============================================================================
st.markdown("---")
f_c1, f_c2 = st.columns([2, 1])
with f_c1:
    st.caption("🌿 **ShopImpact™** — Built with Python & Streamlit | Promoting Conscious Consumerism & Climate Action.")
with f_c2:
    st.caption(f"📅 Session Date: {date.today().strftime('%B %d, %Y')} | Earth-Friendly Mode Active")
