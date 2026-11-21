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
# 1. PAGE CONFIGURATION & AESTHETIC STYLING
# ==============================================================================
st.set_page_config(
    page_title="ShopImpact | Conscious Shopping Companion",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

def apply_custom_styles(dark_mode: bool = False):
    """
    Injects professional CSS styling with proper spacing, generous margins,
    colorful cards, and elegant typography for a friendly, catchy UI.
    """
    if dark_mode:
        bg_page = "#0D1712"
        card_bg = "#14231B"
        border_col = "#244231"
        text_primary = "#F5FAF6"
        text_muted = "#A2C4AF"
        hero_gradient = "linear-gradient(135deg, #091A12 0%, #173827 50%, #23593D 100%)"
        input_bg = "#192D23"
        kpi_spend_bg = "linear-gradient(135deg, #1C2719 0%, #263822 100%)"
        kpi_co2_bg = "linear-gradient(135deg, #2A1F1F 0%, #3D2626 100%)"
        kpi_items_bg = "linear-gradient(135deg, #18282C 0%, #1F363C 100%)"
        kpi_eco_bg = "linear-gradient(135deg, #182C22 0%, #213D2F 100%)"
    else:
        bg_page = "#F8F6F0"          # Warm sand / linen
        card_bg = "#FFFFFF"          # Crisp card white
        border_col = "#E3ECE5"       # Gentle sage border
        text_primary = "#14261B"     # Deep forest ink
        text_muted = "#526B5B"       # Muted slate green
        hero_gradient = "linear-gradient(135deg, #133926 0%, #1F5338 52%, #2D7A51 100%)"
        input_bg = "#FFFFFF"
        kpi_spend_bg = "linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%)"
        kpi_co2_bg = "linear-gradient(135deg, #FEF2F2 0%, #FEE2E2 100%)"
        kpi_items_bg = "linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%)"
        kpi_eco_bg = "linear-gradient(135deg, #F0FDFA 0%, #CCFBF1 100%)"

    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Outfit:wght@500;600;700;800&display=swap');

        /* Global Reset & Typography */
        html, body, [class*="css"], .stMarkdown {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            color: {text_primary};
        }}

        .stApp {{
            background-color: {bg_page};
        }}

        /* Adjust Block Container Spacing */
        .block-container {{
            padding-top: 1.8rem;
            padding-bottom: 3.5rem;
            padding-left: 2.5rem;
            padding-right: 2.5rem;
            max-width: 1440px;
        }}

        /* Professional Hero Banner */
        .hero-container {{
            background: {hero_gradient};
            border-radius: 24px;
            padding: 34px 40px;
            margin-bottom: 28px;
            box-shadow: 0 14px 35px rgba(19, 57, 38, 0.18);
            color: #FFFFFF !important;
            position: relative;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.12);
        }}
        .hero-title {{
            font-family: 'Outfit', sans-serif;
            font-size: 2.35rem;
            font-weight: 800;
            color: #FFFFFF !important;
            margin: 0 0 10px 0;
            letter-spacing: -0.5px;
            line-height: 1.2;
        }}
        .hero-subtitle {{
            font-size: 1.08rem;
            color: #E3F4EA !important;
            margin: 0;
            line-height: 1.55;
            max-width: 820px;
        }}
        .hero-pill-badge {{
            display: inline-flex;
            align-items: center;
            background: rgba(255, 255, 255, 0.18);
            backdrop-filter: blur(8px);
            padding: 6px 16px;
            border-radius: 999px;
            color: #FFFFFF;
            font-weight: 700;
            font-size: 0.85rem;
            margin-bottom: 14px;
            border: 1px solid rgba(255, 255, 255, 0.25);
        }}

        /* Section Headings with Clear Distances */
        .section-header {{
            font-family: 'Outfit', sans-serif;
            font-size: 1.45rem;
            font-weight: 700;
            color: {text_primary};
            margin-top: 12px;
            margin-bottom: 18px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        /* Polished UI Card Containers */
        .pro-card {{
            background-color: {card_bg};
            border: 1px solid {border_col};
            border-radius: 20px;
            padding: 24px 26px;
            margin-bottom: 24px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.04);
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }}
        .pro-card:hover {{
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.07);
        }}

        /* Colorful KPI Cards */
        .kpi-card-spend {{
            background: {kpi_spend_bg};
            border: 1px solid #FCD34D;
            border-radius: 18px;
            padding: 20px 22px;
            text-align: center;
            box-shadow: 0 6px 16px rgba(245, 158, 11, 0.08);
            height: 100%;
        }}
        .kpi-card-co2 {{
            background: {kpi_co2_bg};
            border: 1px solid #FCA5A5;
            border-radius: 18px;
            padding: 20px 22px;
            text-align: center;
            box-shadow: 0 6px 16px rgba(239, 68, 68, 0.08);
            height: 100%;
        }}
        .kpi-card-items {{
            background: {kpi_items_bg};
            border: 1px solid #86EFAC;
            border-radius: 18px;
            padding: 20px 22px;
            text-align: center;
            box-shadow: 0 6px 16px rgba(34, 197, 94, 0.08);
            height: 100%;
        }}
        .kpi-card-eco {{
            background: {kpi_eco_bg};
            border: 1px solid #5EEAD4;
            border-radius: 18px;
            padding: 20px 22px;
            text-align: center;
            box-shadow: 0 6px 16px rgba(20, 184, 166, 0.08);
            height: 100%;
        }}

        .kpi-icon {{
            font-size: 1.8rem;
            margin-bottom: 6px;
        }}
        .kpi-label {{
            font-size: 0.82rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.6px;
            color: {text_muted};
            margin-bottom: 4px;
        }}
        .kpi-value {{
            font-family: 'Outfit', sans-serif;
            font-size: 2.05rem;
            font-weight: 800;
            line-height: 1.15;
            margin-bottom: 4px;
        }}
        .kpi-subtext {{
            font-size: 0.82rem;
            font-weight: 600;
            color: {text_muted};
        }}

        /* Live Reactive Preview Box */
        .live-preview-box {{
            background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);
            border: 1.5px solid #86EFAC;
            border-radius: 18px;
            padding: 22px 24px;
            margin-top: 10px;
            margin-bottom: 18px;
        }}
        .live-preview-dark {{
            background: linear-gradient(135deg, #142E21 0%, #1B402E 100%);
            border: 1.5px solid #2D6A4F;
            border-radius: 18px;
            padding: 22px 24px;
            margin-top: 10px;
            margin-bottom: 18px;
        }}

        /* Swap Recommendation Items */
        .swap-card-item {{
            background-color: {card_bg};
            border-left: 4.5px solid #2D6A4F;
            border-top: 1px solid {border_col};
            border-right: 1px solid {border_col};
            border-bottom: 1px solid {border_col};
            padding: 12px 16px;
            border-radius: 10px;
            margin-bottom: 10px;
            font-size: 0.94rem;
            line-height: 1.45;
            box-shadow: 0 2px 8px rgba(0,0,0,0.02);
        }}

        /* Badges Cards */
        .badge-unlocked-card {{
            background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);
            border: 1.5px solid #4ADE80;
            border-radius: 14px;
            padding: 14px 18px;
            margin-bottom: 12px;
            box-shadow: 0 4px 12px rgba(74, 222, 128, 0.12);
        }}
        .badge-locked-card {{
            background: transparent;
            border: 1.5px dashed {border_col};
            border-radius: 14px;
            padding: 14px 18px;
            margin-bottom: 12px;
            opacity: 0.82;
        }}

        /* Interactive Buttons */
        .stButton > button {{
            border-radius: 12px;
            font-weight: 700;
            padding: 0.6rem 1.3rem;
            border: none;
            transition: all 0.2s ease;
        }}
        .stButton > button:hover {{
            transform: translateY(-1.5px);
            box-shadow: 0 6px 18px rgba(0,0,0,0.1);
        }}

        /* Companion Speech Bubble */
        .speech-bubble {{
            background-color: #FEF3C7;
            border: 1px solid #FDE68A;
            color: #78350F;
            border-radius: 14px;
            padding: 14px 18px;
            font-size: 0.95rem;
            font-weight: 600;
            line-height: 1.45;
            margin-bottom: 16px;
        }}

        /* Environmental Equivalency Callout */
        .equiv-card {{
            background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
            border: 1px solid #93C5FD;
            border-radius: 16px;
            padding: 20px 24px;
            margin-top: 18px;
            margin-bottom: 12px;
        }}
        .equiv-card-dark {{
            background: linear-gradient(135deg, #172554 0%, #1E3A8A 100%);
            border: 1px solid #3B82F6;
            border-radius: 16px;
            padding: 20px 24px;
            margin-top: 18px;
            margin-bottom: 12px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# ==============================================================================
# 2. CURATED DATA MODELS & CALIBRATED MULTIPLIERS
# ==============================================================================
PRODUCT_CATEGORIES = [
    "👕 T-Shirts, Tops & Shirts",
    "👖 Jeans, Denim & Trousers",
    "👟 Footwear (Sneakers & Shoes)",
    "👗 Fast Fashion Dresses & Jackets",
    "💻 Electronics & Gadgets",
    "🛍️ Single-Use & Packaged Goods",
    "🧺 Daily Essentials & Reusable Bags",
    "🌿 Certified Sustainable & Organic",
    "♻️ Thrift & Second-Hand Finds",
]

# Estimated kg CO2 per ₹1 spent
IMPACT_MULTIPLIERS = {
    "👕 T-Shirts, Tops & Shirts": 0.015,
    "👖 Jeans, Denim & Trousers": 0.020,
    "👟 Footwear (Sneakers & Shoes)": 0.024,
    "👗 Fast Fashion Dresses & Jackets": 0.025,
    "💻 Electronics & Gadgets": 0.022,
    "🛍️ Single-Use & Packaged Goods": 0.018,
    "🧺 Daily Essentials & Reusable Bags": 0.008,
    "🌿 Certified Sustainable & Organic": 0.005,
    "♻️ Thrift & Second-Hand Finds": 0.002,
}

IMPACT_RATINGS = {
    "👕 T-Shirts, Tops & Shirts": ("Moderate Carbon Impact", "#D97706", "#FEF3C7"),
    "👖 Jeans, Denim & Trousers": ("High Water & Carbon Footprint", "#DC2626", "#FEE2E2"),
    "👟 Footwear (Sneakers & Shoes)": ("High Carbon Footprint", "#DC2626", "#FEE2E2"),
    "👗 Fast Fashion Dresses & Jackets": ("Very High Carbon Footprint", "#991B1B", "#FEE2E2"),
    "💻 Electronics & Gadgets": ("High Resource & E-Waste Impact", "#DC2626", "#FEE2E2"),
    "🛍️ Single-Use & Packaged Goods": ("Moderate Plastic/Packaging Impact", "#D97706", "#FEF3C7"),
    "🧺 Daily Essentials & Reusable Bags": ("Low Footprint (Eco Essential)", "#059669", "#D1FAE5"),
    "🌿 Certified Sustainable & Organic": ("Very Low Footprint (Ethical Brand)", "#059669", "#D1FAE5"),
    "♻️ Thrift & Second-Hand Finds": ("Minimal Footprint (Circular Hero!)", "#047857", "#A7F3D0"),
}

GREENER_ALTERNATIVES = {
    "👕 T-Shirts, Tops & Shirts": [
        "🔄 Thrift or vintage tees (cuts manufacturing footprint by ~85%).",
        "🌿 100% GOTS certified organic cotton or hemp from ethical brands.",
        "🤝 Host a clothing swap with friends before ordering brand-new tops.",
        "🏷️ Check certified ethical labels like Fabindia, No Nasties, or Brown Boy.",
    ],
    "👖 Jeans, Denim & Trousers": [
        "👖 Second-hand / vintage denim: Making 1 new pair takes ~7,500L of water!",
        "✂️ Repair, tailor, or patch your existing pair to double its life.",
        "💧 Choose low-water, laser-finished denim lines (e.g., Mud Jeans, Levi's Water<Less).",
        "🧵 Choose lightweight recycled cotton or breathable linen trousers.",
    ],
    "👟 Footwear (Sneakers & Shoes)": [
        "👟 Try sneakers made of recycled ocean plastics, sugarcane EVA, or eucalyptus knit.",
        "🌱 Plant-based vegan leathers (Piñatex pineapple leather, apple leather, cork).",
        "🥾 Resoling or deep-cleaning your favorite pair instead of discarding.",
        "🔍 Brands: Veja, Allbirds, Neeman's (recycled PET/merino wool), Paaduks.",
    ],
    "👗 Fast Fashion Dresses & Jackets": [
        "👗 Rent formal occasion wear from fashion rental services.",
        "🧣 Invest in timeless, durable capsule wardrobe pieces made of natural fibers.",
        "♻️ Upcycle old fabrics or vintage sarees into bespoke chic dresses/jackets.",
        "📦 Explore pre-loved fashion marketplaces like Relove, FreeUp, or Suta pre-loved.",
    ],
    "💻 Electronics & Gadgets": [
        "📱 Buy certified refurbished laptops & smartphones with warranty (Cashify, Apple Certified).",
        "🔌 Replace a degraded battery or frayed cable rather than replacing the whole gadget.",
        "🔋 Choose modular, repairable electronics designed for disassembly.",
        "♻️ Safely deposit retired electronics at official e-waste recycling collection centers.",
    ],
    "🛍️ Single-Use & Packaged Goods": [
        "🛍️ Keep a foldable canvas or jute tote bag in your backpack.",
        "🧴 Choose refillable personal care, shampoo bars, and bulk-dispensed pantry foods.",
        "🥤 Carry a reusable insulated stainless steel tumbler and water bottle.",
        "🌿 Replace plastic cling wrap with washable organic beeswax wraps.",
    ],
    "🧺 Daily Essentials & Reusable Bags": [
        "🌟 Outstanding mindful choice! Reusables divert hundreds of single-use plastics.",
        "🧼 Choose compostable, plastic-free toiletries (bamboo brush, unpackaged soaps).",
        "🧺 Support local artisan co-ops and self-help groups crafting natural fiber bags.",
    ],
    "🌿 Certified Sustainable & Organic": [
        "✨ Supporting certified ethical makers builds cleaner, worker-safe supply chains.",
        "📜 Verify legitimate certifications like Fair Trade, OEKO-TEX, GOTS, or B-Corp.",
        "🌱 Longevity test: Even ethical fashion has the highest impact when worn for years!",
    ],
    "♻️ Thrift & Second-Hand Finds": [
        "🏆 Circular Economy Champion! Thrifting extends product life with near-zero emissions.",
        "📸 Share your thrift finds to inspire friends and normalize pre-loved fashion.",
        "💫 Gentle wash in cold water and air-drying keeps vintage items looking brand new.",
    ],
}

ECO_TIPS = [
    "💧 Making one cotton t-shirt requires ~2,700 litres of water — enough for one person to drink for 900 days!",
    "👕 The '30-Wear Test': Before buying, ask yourself: 'Will I wear this at least 30 times?' If not, skip it.",
    "📱 Extending your smartphone or laptop life by just 1 year cuts its annual carbon footprint by ~25%.",
    "👟 Washing clothes in cold water and line-drying slashes laundry emissions by 60% while protecting fabric fibers.",
    "♻️ Buying one second-hand or thrifted item saves around 85% of emissions compared to buying brand-new.",
    "🛍️ A single durable organic cotton or canvas tote replaces up to 500 single-use plastic bags over its lifetime.",
    "👖 Producing one pair of denim jeans emits ~25 kg of CO₂ and consumes up to 8,000 litres of water.",
    "🥦 Food packaging waste accounts for over 35% of all consumer plastic. Choosing bulk refill stations makes a huge dent.",
]

ECO_QUOTES = [
    "“We don’t need a handful of people doing zero waste perfectly. We need millions of people doing it imperfectly.” — Anne Marie Bonneau",
    "“Buy less, choose well, make it last.” — Vivienne Westwood",
    "“The greatest threat to our planet is the belief that someone else will save it.” — Robert Swan",
    "“There is no such thing as ‘away’. When we throw anything away it must go somewhere.” — Annie Leonard",
    "“Every time you spend money, you're casting a vote for the kind of world you want.” — Anna Lappé",
    "“The most sustainable garment is the one already in your wardrobe.” — Orsola de Castro",
]

# ------------------------------------------------------------------------------
# Core Calculation & Helper Functions
# ------------------------------------------------------------------------------
def calculate_co2_kg(product_type: str, price: float) -> float:
    """Calculates estimated CO2 footprint in kg based on curated multipliers."""
    multiplier = IMPACT_MULTIPLIERS.get(product_type, 0.012)
    return round(float(price) * multiplier, 2)

def calculate_equivalencies(co2_kg: float) -> dict:
    """Translates abstract CO2 kg numbers into tangible, relatable real-world metrics."""
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
    """Adds a new purchase entry with complete metadata."""
    co2_kg = calculate_co2_kg(product_type, price)
    is_eco_pick = product_type in [
        "♻️ Thrift & Second-Hand Finds",
        "🌿 Certified Sustainable & Organic",
        "🧺 Daily Essentials & Reusable Bags",
    ]
    new_item = {
        "id": str(uuid.uuid4())[:8],
        "product_type": product_type,
        "brand": brand.strip() if brand.strip() else "Local / Unspecified",
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
    """Removes a purchase by ID."""
    for i, item in enumerate(purchases_list):
        if item.get("id") == item_id:
            purchases_list.pop(i)
            return True
    return False

def get_monthly_summary(purchases_list: list, month_str: str) -> dict:
    """Calculates total spend, total CO2, and eco metrics for a given month."""
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
    """Evaluates badge milestones with clear conditions."""
    items = monthly_summary["items"]
    m_co2 = monthly_summary["total_co2"]
    count = monthly_summary["count"]
    eco_count = monthly_summary["eco_count"]

    catalog = [
        {
            "id": "starter",
            "name": "🌱 Eco Starter",
            "desc": "Logged your first conscious shopping item",
            "unlocked": len(total_purchases) >= 1,
            "status_text": "Unlocked! Your mindfulness journey begins." if len(total_purchases) >= 1 else "Log 1 purchase to unlock",
        },
        {
            "id": "saver",
            "name": "🍃 Eco Saver of the Month",
            "desc": "Kept monthly carbon impact under 12 kg CO₂",
            "unlocked": count >= 1 and m_co2 <= 12.0,
            "status_text": f"Current: {m_co2} kg CO₂ (Target ≤ 12 kg)" if count >= 1 else "Log purchases this month",
        },
        {
            "id": "low_impact",
            "name": "🌍 Low Impact Shopper",
            "desc": "3+ purchases logged while keeping monthly CO₂ ≤ 25 kg",
            "unlocked": count >= 3 and m_co2 <= 25.0,
            "status_text": f"Items: {count}/3 | CO₂: {m_co2} kg",
        },
        {
            "id": "swap_champ",
            "name": "♻️ Green Swap Champion",
            "desc": "Logged 2 or more Thrift or Sustainable picks",
            "unlocked": eco_count >= 2,
            "status_text": f"Eco picks logged: {eco_count}/2",
        },
        {
            "id": "budget_master",
            "name": "🎯 Carbon Budget Master",
            "desc": f"Emissions stayed within monthly limit (≤ {carbon_budget:.0f} kg)",
            "unlocked": count >= 1 and m_co2 <= carbon_budget,
            "status_text": f"{m_co2} kg / {carbon_budget} kg limit",
        },
        {
            "id": "guardian",
            "name": "🛡️ Conscious Guardian",
            "desc": "50%+ of monthly items are circular/eco-friendly",
            "unlocked": count >= 2 and (eco_count / count) >= 0.5,
            "status_text": f"Current Eco Ratio: {monthly_summary['eco_ratio']}% (Target ≥ 50%)",
        },
    ]

    unlocked_list = [b["name"] for b in catalog if b["unlocked"]]
    return {
        "catalog": catalog,
        "unlocked_names": unlocked_list,
        "unlocked_count": len(unlocked_list),
        "total_count": len(catalog),
    }

# ==============================================================================
# 3. TURTLE GRAPHICS COMPANION (CLOUD-SAFE & HEADLESS-RESILIENT)
# ==============================================================================
def draw_turtle_with_pillow(eco_level: str, filename: str) -> str:
    """Renders antialiased companion artwork that never fails on Streamlit Cloud."""
    width, height = 440, 320
    bg_color = (248, 246, 240)
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
    """Attempts native Python Turtle first, seamlessly falling back to Pillow."""
    out_png = f"turtle_{eco_level}.png"
    ps_file = f"turtle_{eco_level}.ps"

    script_path = "_draw_turtle_tmp.py"
    turtle_script = f"""
import turtle
try:
    screen = turtle.Screen()
    screen.setup(width=440, height=320)
    screen.bgcolor("#F8F6F0")
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
        subprocess.run(cmd, check=True, timeout=4)
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
if "celebrate" not in st.session_state:
    st.session_state.celebrate = False

# ==============================================================================
# 5. SIDEBAR: THEME, TARGETS & 1-CLICK DEMO PROFILES
# ==============================================================================
with st.sidebar:
    st.markdown("## 🌿 ShopImpact Studio")
    st.caption("Conscious Shopping & Carbon Footprint Assistant")

    dark_mode = st.toggle("🌙 High-Contrast / Dark Mode", value=False)
    apply_custom_styles(dark_mode)

    st.markdown("<hr style='margin: 18px 0; border: none; border-top: 1px solid #D5E2D9;'>", unsafe_allow_html=True)
    st.markdown("### 🎯 Monthly Targets")
    st.caption("Personal ceiling for mindful shopping:")

    carbon_budget = st.slider(
        "CO₂ Ceiling (kg / month)",
        min_value=5.0,
        max_value=80.0,
        value=float(st.session_state.carbon_budget),
        step=5.0,
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

    st.markdown("<hr style='margin: 18px 0; border: none; border-top: 1px solid #D5E2D9;'>", unsafe_allow_html=True)
    st.markdown("### ⚡ 1-Click Demo Profiles")
    st.caption("Instantly test realistic scenarios:")

    c_d1, c_d2 = st.columns(2)
    with c_d1:
        if st.button("🌱 Eco Saver", use_container_width=True, help="Load mindful thrift & eco picks"):
            today = date.today()
            st.session_state.purchases = []
            add_purchase(st.session_state.purchases, "♻️ Thrift & Second-Hand Finds", "Vintage Vault", 450, today, "Oversized denim jacket")
            add_purchase(st.session_state.purchases, "🧺 Daily Essentials & Reusable Bags", "EcoCarry", 299, today, "Organic jute tote")
            add_purchase(st.session_state.purchases, "🌿 Certified Sustainable & Organic", "No Nasties", 1200, today, "Hemp casual tee")
            st.session_state.current_tip = random.choice(ECO_TIPS)
            st.toast("Loaded Eco Saver Demo Haul! 🌿", icon="✨")
            st.rerun()

    with c_d2:
        if st.button("🚨 Fast Fashion", use_container_width=True, help="Load high carbon impulse haul"):
            today = date.today()
            st.session_state.purchases = []
            add_purchase(st.session_state.purchases, "👗 Fast Fashion Dresses & Jackets", "UltraFast", 2400, today, "Polyester party dress")
            add_purchase(st.session_state.purchases, "👖 Jeans, Denim & Trousers", "DenimTrend", 1800, today, "Ripped skinny jeans")
            add_purchase(st.session_state.purchases, "👟 Footwear (Sneakers & Shoes)", "VibeSneaks", 3500, today, "Synthetic high tops")
            st.toast("Loaded Fast Fashion Haul! 🚨", icon="⚠️")
            st.rerun()

    if st.button("⚖️ Balanced Everyday Shopper", use_container_width=True):
        today = date.today()
        st.session_state.purchases = []
        add_purchase(st.session_state.purchases, "♻️ Thrift & Second-Hand Finds", "Thrift Corner", 350, today, "Graphic tee")
        add_purchase(st.session_state.purchases, "👕 T-Shirts, Tops & Shirts", "Everyday Basics", 699, today, "Work cotton shirt")
        add_purchase(st.session_state.purchases, "🛍️ Single-Use & Packaged Goods", "Supermarket", 400, today, "Snack multipacks")
        st.toast("Loaded Balanced Shopper Profile!", icon="📊")
        st.rerun()

    if st.button("🧹 Clear All Purchases", use_container_width=True):
        st.session_state.purchases = []
        st.toast("Records cleared.", icon="🧹")
        st.rerun()

# ==============================================================================
# 6. HERO BANNER
# ==============================================================================
st.markdown(
    """
    <div class="hero-container">
        <div class="hero-pill-badge">✨ Conscious Consumerism Engine</div>
        <h1 class="hero-title">🌿 ShopImpact — Conscious Shopping Dashboard</h1>
        <p class="hero-subtitle">
            Transform everyday shopping into mindful climate action. Plan your purchases, see your live CO₂ footprint,
            discover greener alternatives, and celebrate sustainable habits with interactive badges and Turtle graphics.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

if st.session_state.celebrate:
    st.balloons()
    st.session_state.celebrate = False

# ==============================================================================
# 7. TOP PANEL: INPUT FIELDS & REAL-TIME IMPACT PREVIEW (BRIEF COMPULSORY)
# ==============================================================================
st.markdown('<div class="section-header">🛒 1. Log a Planned Purchase (Inputs at the Top)</div>', unsafe_allow_html=True)

input_left, input_right = st.columns([1.35, 1.0], gap="large")

with input_left:
    with st.container():
        st.markdown(
            f"""
            <div class="pro-card">
                <div style="font-weight: 700; font-size: 1.12rem; margin-bottom: 12px; color: #1B4332;">
                    🛍️ Purchase Details
                </div>
            """,
            unsafe_allow_html=True,
        )

        c1, c2 = st.columns(2)
        with c1:
            product_type = st.selectbox(
                "Product Category",
                PRODUCT_CATEGORIES,
                index=0,
                help="Different goods carry vastly different water & carbon costs.",
            )
        with c2:
            brand = st.text_input("Brand or Store Name", placeholder="e.g., Fabindia, Nike, Local Thrift")

        c3, c4 = st.columns(2)
        with c3:
            price = st.number_input("Item Price (₹)", min_value=1.0, max_value=250000.0, value=799.0, step=50.0)
        with c4:
            p_date = st.date_input("Purchase / Planned Date", value=date.today())

        # Quick price chip shortcuts
        st.caption("Quick Price Shortcut Chips:")
        chip_cols = st.columns(5)
        chips = [299, 499, 999, 1999, 3999]
        for i, val in enumerate(chips):
            if chip_cols[i].button(f"₹{val}", use_container_width=True):
                price = float(val)

        notes = st.text_input("Notes or Tags (Optional)", placeholder="e.g., College wear, low-water fabric, 100% hemp")

        st.markdown("</div>", unsafe_allow_html=True)

        if st.button("➕ Confirm & Log Purchase", type="primary", use_container_width=True):
            new_item = add_purchase(st.session_state.purchases, product_type, brand, price, p_date, notes)
            st.session_state.current_tip = random.choice(ECO_TIPS)
            st.session_state.current_quote = random.choice(ECO_QUOTES)
            if new_item["is_eco_pick"]:
                st.session_state.celebrate = True
                st.toast("🎉 Awesome! Logged a sustainable eco pick!", icon="🌟")
            else:
                st.toast(f"Logged {product_type} (₹{price:,.0f})", icon="✅")
            st.rerun()

with input_right:
    with st.container():
        # Live Reactive Calculation Preview
        live_co2 = calculate_co2_kg(product_type, price)
        rating_desc, rating_color, rating_bg = IMPACT_RATINGS[product_type]
        eq_live = calculate_equivalencies(live_co2)

        preview_style = "live-preview-dark" if dark_mode else "live-preview-box"

        st.markdown(
            f"""
            <div class="{preview_style}">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span style="font-weight: 800; font-size: 0.95rem; text-transform: uppercase; letter-spacing: 0.5px; color: #1B4332;">
                        ⚡ Live Impact Preview
                    </span>
                    <span style="background-color: {rating_bg}; color: {rating_color}; font-weight: 800; font-size: 0.8rem; padding: 4px 12px; border-radius: 999px;">
                        {rating_desc}
                    </span>
                </div>
                <div style="font-family: 'Outfit', sans-serif; font-size: 2.1rem; font-weight: 800; color: #1B4332; margin-bottom: 4px;">
                    {live_co2} kg CO₂
                </div>
                <div style="font-size: 0.88rem; color: #2D6A4F; line-height: 1.45;">
                    🚗 Approx. <b>{eq_live['car_km']} km</b> driven in a petrol car<br>
                    🌳 Takes <b>{eq_live['trees_needed']} tree-months</b> to sequester
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Greener Alternatives for this category
        st.markdown(
            f"""
            <div class="pro-card" style="padding: 18px 20px;">
                <div style="font-weight: 700; font-size: 1.05rem; margin-bottom: 10px; color: #1B4332;">
                    🌱 Greener Alternatives for {product_type.split(' ', 1)[-1]}
                </div>
            """,
            unsafe_allow_html=True,
        )
        for alt in GREENER_ALTERNATIVES[product_type]:
            st.markdown(f'<div class="swap-card-item">{alt}</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

# ==============================================================================
# 8. MAIN DASHBOARD (CENTER) & COMPANION / BADGES (ON THE SIDE)
# ==============================================================================
dash_col, side_col = st.columns([1.8, 1.0], gap="large")

# ------------------------------------------------------------------------------
# 8A. DASHBOARD IN THE CENTER
# ------------------------------------------------------------------------------
with dash_col:
    st.markdown('<div class="section-header">📊 2. Monthly Impact Dashboard (In the Center)</div>', unsafe_allow_html=True)

    # Month Selector
    curr_month = date.today().strftime("%Y-%m")
    available_months = sorted({p["month"] for p in st.session_state.purchases}, reverse=True) if st.session_state.purchases else [curr_month]
    active_month = st.selectbox("📅 Review Month", available_months, index=0)

    summary = get_monthly_summary(st.session_state.purchases, active_month)
    carbon_ceiling = st.session_state.carbon_budget
    spend_ceiling = st.session_state.spend_budget

    co2_pct = min(100.0, (summary["total_co2"] / carbon_ceiling * 100)) if carbon_ceiling > 0 else 0.0
    spend_pct = min(100.0, (summary["total_spend"] / spend_ceiling * 100)) if spend_ceiling > 0 else 0.0

    # 4 Colorful Catchy KPI Boxes
    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.markdown(
            f"""
            <div class="kpi-card-items">
                <div class="kpi-icon">📦</div>
                <div class="kpi-label">Items Logged</div>
                <div class="kpi-value" style="color: #166534;">{summary['count']}</div>
                <div class="kpi-subtext">{summary['eco_count']} eco picks</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with k2:
        st.markdown(
            f"""
            <div class="kpi-card-spend">
                <div class="kpi-icon">💰</div>
                <div class="kpi-label">Total Spend</div>
                <div class="kpi-value" style="color: #92400E;">₹{summary['total_spend']:,.0f}</div>
                <div class="kpi-subtext">Limit: ₹{spend_ceiling:,.0f}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with k3:
        co2_color = "#166534" if summary["total_co2"] <= carbon_ceiling else "#991B1B"
        st.markdown(
            f"""
            <div class="kpi-card-co2">
                <div class="kpi-icon">☁️</div>
                <div class="kpi-label">Est. CO₂ Footprint</div>
                <div class="kpi-value" style="color: {co2_color};">{summary['total_co2']} kg</div>
                <div class="kpi-subtext">Target: ≤ {carbon_ceiling:.0f} kg</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with k4:
        st.markdown(
            f"""
            <div class="kpi-card-eco">
                <div class="kpi-icon">🌿</div>
                <div class="kpi-label">Eco-Pick Ratio</div>
                <div class="kpi-value" style="color: #0F766E;">{summary['eco_ratio']}%</div>
                <div class="kpi-subtext">Mindful circular buys</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

    # Budget & Carbon Target Progress Bars
    with st.container():
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        st.markdown("<div style='font-weight: 700; font-size: 1.05rem; margin-bottom: 12px;'>🎯 Monthly Progress Meters</div>", unsafe_allow_html=True)

        bar_c1, bar_c2 = st.columns(2)
        with bar_c1:
            st.write(f"**Carbon Footprint:** `{summary['total_co2']} / {carbon_ceiling:.0f} kg CO₂` ({co2_pct:.1f}%)")
            st.progress(co2_pct / 100.0)
            if summary["total_co2"] > carbon_ceiling:
                st.warning(f"⚠️ Exceeded carbon ceiling by {round(summary['total_co2'] - carbon_ceiling, 1)} kg CO₂.")
            else:
                st.caption(f"✅ Safe carbon buffer: **{round(carbon_ceiling - summary['total_co2'], 1)} kg CO₂ remaining**.")

        with bar_c2:
            st.write(f"**Spending Budget:** `₹{summary['total_spend']:,.0f} / ₹{spend_ceiling:,.0f}` ({spend_pct:.1f}%)")
            st.progress(spend_pct / 100.0)
            if summary["total_spend"] > spend_ceiling:
                st.warning(f"⚠️ Exceeded budget by ₹{round(summary['total_spend'] - spend_ceiling, 0):,.0f}.")
            else:
                st.caption(f"✅ Safe spending buffer: **₹{round(spend_ceiling - summary['total_spend'], 0):,.0f} remaining**.")

        st.markdown('</div>', unsafe_allow_html=True)

    # Charts & Category Breakdowns
    if summary["items"]:
        df_month = pd.DataFrame(summary["items"])
        ch_col1, ch_col2 = st.columns(2)

        with ch_col1:
            with st.container():
                st.markdown('<div class="pro-card">', unsafe_allow_html=True)
                st.markdown("<div style='font-weight: 700; font-size: 1.05rem; margin-bottom: 10px;'>📊 Carbon Impact by Category (kg CO₂)</div>", unsafe_allow_html=True)
                chart_df = df_month.groupby("product_type", as_index=False)["co2_kg"].sum().sort_values(by="co2_kg", ascending=False)
                st.bar_chart(chart_df.set_index("product_type")["co2_kg"], color="#2D6A4F", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

        with ch_col2:
            with st.container():
                st.markdown('<div class="pro-card">', unsafe_allow_html=True)
                st.markdown("<div style='font-weight: 700; font-size: 1.05rem; margin-bottom: 10px;'>💰 Spending Distribution by Category (₹)</div>", unsafe_allow_html=True)
                spend_df = df_month.groupby("product_type", as_index=False)["price"].sum().sort_values(by="price", ascending=False)
                st.bar_chart(spend_df.set_index("product_type")["price"], color="#D97706", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

        # Environmental Equivalency Banner
        eq = summary["equivalencies"]
        eq_box_style = "equiv-card-dark" if dark_mode else "equiv-card"
        st.markdown(
            f"""
            <div class="{eq_box_style}">
                <div style="font-weight: 800; font-size: 1.08rem; color: #1E3A8A; margin-bottom: 8px;">
                    🌍 Real-World Environmental Equivalency
                </div>
                <div style="font-size: 0.95rem; color: #1E40AF; line-height: 1.6;">
                    🚗 Equivalent to driving <b>{eq['car_km']} km</b> in a standard petrol passenger car.<br>
                    🌳 Requires roughly <b>{eq['trees_needed']} mature tree-months</b> to naturally sequester.<br>
                    🔋 Energy equal to charging <b>{eq['smartphones']:,} smartphones</b>.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Purchase History Table with Search, Filter & Delete
        st.markdown('<div class="pro-card" style="margin-top: 18px;">', unsafe_allow_html=True)
        st.markdown("<div style='font-weight: 700; font-size: 1.15rem; margin-bottom: 12px;'>🧾 Logged Items History</div>", unsafe_allow_html=True)

        f1, f2 = st.columns([2, 1.2])
        with f1:
            q_search = st.text_input("🔍 Search by Brand or Notes", placeholder="e.g. Fabindia, thrift...")
        with f2:
            sort_opt = st.selectbox("Sort Order", ["Newest First", "Price (High to Low)", "CO₂ (High to Low)"])

        filtered_df = df_month.copy()
        if q_search:
            filtered_df = filtered_df[
                filtered_df["brand"].str.contains(q_search, case=False, na=False)
                | filtered_df["notes"].str.contains(q_search, case=False, na=False)
            ]

        if sort_opt == "Newest First":
            filtered_df = filtered_df.sort_values(by="date", ascending=False)
        elif sort_opt == "Price (High to Low)":
            filtered_df = filtered_df.sort_values(by="price", ascending=False)
        elif sort_opt == "CO₂ (High to Low)":
            filtered_df = filtered_df.sort_values(by="co2_kg", ascending=False)

        show_df = filtered_df[["date", "product_type", "brand", "price", "co2_kg", "is_eco_pick", "notes"]].rename(
            columns={
                "date": "Date",
                "product_type": "Category",
                "brand": "Brand",
                "price": "Price (₹)",
                "co2_kg": "CO₂ (kg)",
                "is_eco_pick": "Eco Pick?",
                "notes": "Notes",
            }
        )
        st.dataframe(show_df, use_container_width=True, hide_index=True)

        # CSV Download & Delete Purchase
        a1, a2 = st.columns([1.5, 2.0])
        with a1:
            csv_bytes = filtered_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "📥 Export Purchases to CSV",
                data=csv_bytes,
                file_name=f"shopimpact_{active_month}.csv",
                mime="text/csv",
                use_container_width=True,
            )
        with a2:
            del_opts = {
                f"{p['date']} - {p['product_type']} (₹{p['price']}) [{p['brand']}]": p["id"]
                for p in st.session_state.purchases
            }
            if del_opts:
                del_choice = st.selectbox("Select Item to Delete", list(del_opts.keys()))
                if st.button("🗑️ Delete Selected Item", use_container_width=True):
                    del_id = del_opts[del_choice]
                    delete_purchase(st.session_state.purchases, del_id)
                    st.toast("Item deleted successfully.", icon="🗑️")
                    st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.info("💡 No purchases logged for this month yet. Use the form above or click **🌱 Eco Saver** in the sidebar to populate realistic data!")

    # Conscious Swap Simulator (Collapsible Feature)
    with st.expander("🔄 Launch Greener Swap Simulator (Compare Before Buying)", expanded=False):
        st.markdown("#### Test the Environmental & Financial Dividend of a Greener Choice:")
        s_c1, s_c2 = st.columns(2)
        with s_c1:
            conv_p = st.selectbox("Conventional Brand-New Item", PRODUCT_CATEGORIES[:5], key="sim_conv_p")
            conv_pr = st.number_input("Conventional Price (₹)", min_value=100.0, value=2500.0, step=100.0, key="sim_conv_pr")
            conv_c = calculate_co2_kg(conv_p, conv_pr)
            st.metric("Conventional CO₂", f"{conv_c} kg CO₂")

        with s_c2:
            eco_p = st.selectbox("Greener / Thrift Alternative", PRODUCT_CATEGORIES[6:], key="sim_eco_p")
            eco_pr = st.number_input("Alternative Price (₹)", min_value=50.0, value=850.0, step=50.0, key="sim_eco_pr")
            eco_c = calculate_co2_kg(eco_p, eco_pr)
            st.metric("Greener Choice CO₂", f"{eco_c} kg CO₂")

        co2_diff = round(max(0.0, conv_c - eco_c), 2)
        money_diff = round(max(0.0, conv_pr - eco_pr), 2)
        eq_diff = calculate_equivalencies(co2_diff)

        st.success(
            f"🌟 **Swap Dividend:** You save **₹{money_diff:,.0f}** and avoid **{co2_diff} kg CO₂** "
            f"(Equal to **{eq_diff['car_km']} km** car travel avoided and **{eq_diff['trees_needed']} tree-months** spared!)"
        )
        if st.button("✨ Log This Greener Swap to My Dashboard", use_container_width=True):
            add_purchase(
                st.session_state.purchases,
                eco_p,
                "Conscious Alternative",
                eco_pr,
                date.today(),
                f"Swapped from {conv_p} (Saved {co2_diff} kg CO₂)",
            )
            st.session_state.celebrate = True
            st.toast("Greener swap logged!", icon="🌱")
            st.rerun()

# ------------------------------------------------------------------------------
# 8B. BADGES AND TURTLE DRAWINGS (ON THE SIDE - BRIEF COMPULSORY)
# ------------------------------------------------------------------------------
with side_col:
    st.markdown('<div class="section-header">🐢 3. Companion & Badges (On the Side)</div>', unsafe_allow_html=True)

    # Turtle Companion State
    badge_eval = evaluate_all_badges(summary, st.session_state.purchases, st.session_state.carbon_budget)

    if not summary["items"]:
        turtle_state = "leaf"
        state_title = "🌱 Eco Leaf"
        state_msg = "Ready to start tracking conscious choices!"
    elif badge_eval["unlocked_count"] >= 3 or (summary["count"] >= 3 and summary["total_co2"] <= 15.0):
        turtle_state = "badge"
        state_title = "⭐ Eco Star Badge!"
        state_msg = "Incredible habit! You've maintained an ultra-low carbon footprint."
    elif summary["eco_ratio"] >= 40.0:
        turtle_state = "sprout"
        state_title = "🌍 Planet Champion"
        state_msg = "Awesome! Over 40% of your items are second-hand or certified eco-picks."
    elif summary["total_co2"] <= st.session_state.carbon_budget:
        turtle_state = "leaf"
        state_title = "🌿 Healthy Eco Leaf"
        state_msg = "You are currently within your monthly carbon ceiling. Keep it up!"
    else:
        turtle_state = "footprint"
        state_title = "👣 Mindful Footprint Check"
        state_msg = "Footprint is running high. Check the suggested greener swaps!"

    with st.container():
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        st.markdown(f"<div style='font-weight: 800; font-size: 1.15rem; margin-bottom: 6px; color: #1B4332;'>🐢 Turtle Companion: {state_title}</div>", unsafe_allow_html=True)

        st.markdown(f'<div class="speech-bubble">💬 <b>Turtle Companion says:</b><br>"{state_msg}"</div>', unsafe_allow_html=True)

        # Generate and show graphic
        turtle_img = generate_turtle_visual(turtle_state)
        st.image(turtle_img, use_container_width=True)

        with st.expander("🎨 Test All Turtle Drawings"):
            t_pick = st.selectbox(
                "Choose Artwork",
                ["leaf", "badge", "sprout", "footprint"],
                format_func=lambda x: {
                    "leaf": "🌿 Eco Leaf",
                    "badge": "⭐ Eco Saver Badge",
                    "sprout": "🌍 Planet Guardian Sprout",
                    "footprint": "👣 Mindful Footprint",
                }[x],
            )
            if st.button("Draw Graphic"):
                preview_pic = generate_turtle_visual(t_pick)
                st.image(preview_pic, use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # Badges Milestone Showcase
    with st.container():
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        st.markdown(
            f"<div style='font-weight: 800; font-size: 1.15rem; margin-bottom: 4px; color: #1B4332;'>🏅 Milestone Badges ({badge_eval['unlocked_count']}/{badge_eval['total_count']})</div>",
            unsafe_allow_html=True,
        )
        st.caption("Earn badges as you build mindful shopping habits:")

        for b in badge_eval["catalog"]:
            if b["unlocked"]:
                st.markdown(
                    f"""
                    <div class="badge-unlocked-card">
                        <div style="font-weight: 800; font-size: 1.02rem; color: #14532D;">
                            {b['name']} <span style="font-size: 0.72rem; background: #22C55E; color: white; padding: 2px 8px; border-radius: 999px; margin-left: 6px;">UNLOCKED</span>
                        </div>
                        <div style="font-size: 0.84rem; color: #166534; margin-top: 3px;">{b['desc']}</div>
                        <div style="font-size: 0.76rem; color: #14532D; font-weight: 700; margin-top: 4px;">✓ {b['status_text']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"""
                    <div class="badge-locked-card">
                        <div style="font-weight: 700; font-size: 0.95rem; color: #64748B;">🔒 {b['name']}</div>
                        <div style="font-size: 0.82rem; color: #64748B; margin-top: 3px;">{b['desc']}</div>
                        <div style="font-size: 0.75rem; color: #94A3B8; margin-top: 4px;">• {b['status_text']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.markdown('</div>', unsafe_allow_html=True)

    # Eco Tip & Quote Card
    with st.container():
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        st.markdown("<div style='font-weight: 700; font-size: 1.05rem; margin-bottom: 8px;'>💡 Daily Eco Wisdom</div>", unsafe_allow_html=True)
        st.info(st.session_state.current_tip)

        if st.button("🎲 Shuffle Tip & Quote", use_container_width=True):
            st.session_state.current_tip = random.choice(ECO_TIPS)
            st.session_state.current_quote = random.choice(ECO_QUOTES)
            st.rerun()

        st.markdown(f"<div style='font-style: italic; font-size: 0.88rem; color: #4B5563; margin-top: 10px;'>{st.session_state.current_quote}</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # 30-Wear Checklist Expander
    with st.expander("📋 The 30-Wear Longevity Test"):
        st.caption("Ask these 4 questions before buying new fashion:")
        c_1 = st.checkbox("Can I pair this with 3+ things I already own?", value=True)
        c_2 = st.checkbox("Will I still wear this proudly 1 year from now?", value=True)
        c_3 = st.checkbox("Is the material breathable, durable, and repairable?")
        c_4 = st.checkbox("Did I check if I could thrift or borrow it first?")

        tot_score = sum([c_1, c_2, c_3, c_4])
        if tot_score == 4:
            st.success("🌟 4/4! Great choice, passes the 30-wear test.")
        elif tot_score >= 2:
            st.warning("⚠️ 2–3/4: Sleep on it for 24 hours before buying.")
        else:
            st.error("🚨 0–1/4: High impulse risk! Better to skip.")

# ==============================================================================
# 9. FOOTER
# ==============================================================================
st.markdown("<hr style='margin-top: 36px; margin-bottom: 20px; border: none; border-top: 1px solid #D5E2D9;'>", unsafe_allow_html=True)
foot_1, foot_2 = st.columns([2, 1])
with foot_1:
    st.caption("🌿 **ShopImpact™** — Conscious Shopping Companion | Designed for Python Summative Assessment.")
with foot_2:
    st.caption(f"📅 Active Date: {date.today().strftime('%B %d, %Y')} | Earth-Friendly Mode Active")
