import streamlit as st
import pandas as pd
from datetime import date, datetime
import random
import html
from pathlib import Path

# ShopImpact: conscious shopping dashboard
st.set_page_config(page_title="ShopImpact | Shop smarter, live greener",
                   page_icon="🌿", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
html, body, [class*="css"] {font-family:'DM Sans',sans-serif;}
.stApp {background:linear-gradient(180deg,#f5f8f1 0%,#fbfcf8 48%,#f5f8f1 100%);}
.block-container {padding-top:1.6rem;padding-bottom:3rem;max-width:1250px;}
h1,h2,h3 {font-family:'Manrope',sans-serif;color:#183c2d;}
.hero {background:linear-gradient(120deg,#153f30,#23664a 58%,#77a66e);padding:2.2rem 2.3rem;border-radius:25px;color:white;margin-bottom:1.3rem;box-shadow:0 12px 35px rgba(27,76,54,.13);}
.hero h1 {color:white;font-size:2.55rem;margin:0 0 .35rem;letter-spacing:-1.2px;}
.hero p {color:#e7f3e9;font-size:1.05rem;margin:0;max-width:700px;}
.pill {display:inline-block;background:#e5f3e7;color:#236342;padding:6px 12px;border-radius:30px;font-size:.78rem;font-weight:700;margin-bottom:12px;}
.metric-card {background:white;border:1px solid #e5ece2;border-radius:18px;padding:18px 20px;box-shadow:0 5px 18px rgba(31,66,45,.045);min-height:118px;}
.metric-label {color:#718174;font-size:.83rem;font-weight:600;}
.metric-value {color:#193d2d;font-family:'Manrope';font-size:1.8rem;font-weight:800;margin-top:5px;}
.metric-note,.small-muted {color:#718174;font-size:.85rem;}
.panel {background:white;border:1px solid #e5ece2;border-radius:20px;padding:20px 22px;box-shadow:0 5px 18px rgba(31,66,45,.04);margin-bottom:14px;}
.tip {background:#edf6e9;border-left:5px solid #6b9f63;padding:15px 17px;border-radius:12px;color:#31553b;}
.badge {display:inline-block;background:#fff4d9;color:#795516;border:1px solid #f4dfaa;border-radius:14px;padding:11px 14px;margin:5px 5px 5px 0;font-weight:700;}
div.stButton>button {border-radius:12px;font-weight:700;min-height:2.7rem;}
div[data-testid="stFormSubmitButton"] button {background:#1d6546;color:white;border:0;}
[data-testid="stSidebar"] {background:#edf4e9;}
</style>
""", unsafe_allow_html=True)

PRODUCT_MULTIPLIERS = {
    "Clothing": 0.025, "Electronics": 0.018, "Food & groceries": 0.012,
    "Beauty & personal care": 0.010, "Home & lifestyle": 0.015,
    "Footwear": 0.022, "Books & stationery": 0.006, "Other": 0.012
}
ALTERNATIVES = {
    "Clothing":["Choose second-hand clothing","Look for durable fabrics and repair items","Check whether a brand shares clear sustainability information"],
    "Electronics":["Repair devices when possible","Consider refurbished devices","Recycle old electronics through approved e-waste collection"],
    "Food & groceries":["Choose seasonal produce when practical","Plan meals to reduce food waste","Try more plant-based meals"],
    "Beauty & personal care":["Choose refill packs where available","Look for minimal packaging","Use products fully before replacing them"],
    "Home & lifestyle":["Reuse or upcycle items","Choose durable products","Consider recycled or responsibly sourced materials"],
    "Footwear":["Repair shoes instead of replacing them","Choose durable footwear","Explore verified second-hand options"],
    "Books & stationery":["Borrow or buy used books","Use refillable stationery","Choose recycled paper when available"],
    "Other":["Pause and check whether you need the item","Choose reusable options","Look for durable products"]
}
ECO_TIPS = [
    "A product used for years can be a better choice than one replaced often.",
    "Planning purchases can help reduce waste and unnecessary spending.",
    "Repairing, reusing and sharing are simple ways to reduce your footprint.",
    "Buying less, but choosing carefully, can make a positive difference."
]

if "purchases" not in st.session_state:
    st.session_state.purchases = []
if "tip" not in st.session_state:
    st.session_state.tip = random.choice(ECO_TIPS)

def estimate_impact(product_type, price):
    """Calculate an illustrative CO2e estimate from price and category multiplier."""
    return round(float(price) * PRODUCT_MULTIPLIERS.get(product_type, 0.012), 2)

def get_badges(purchases):
    """Use conditions and loops to award badges."""
    badges = []
    if len(purchases) >= 1:
        badges.append(("🌱", "First Green Step", "You logged your first purchase."))
    if len(purchases) >= 5:
        badges.append(("🛍️", "Mindful Tracker", "You logged five or more purchases."))
    total = sum(item["impact"] for item in purchases)
    if purchases and total <= 2:
        badges.append(("🍃", "Low Impact Start", "Your recorded estimated impact is 2 kg CO2e or less."))
    for item in purchases:
        if item["choice"] == "More sustainable choice":
            badges.append(("💚", "Conscious Choice", "You recorded a more sustainable choice."))
            break
    return badges

def turtle_fallback_svg():
    """Cloud-safe turtle-inspired illustration; see turtle_graphics.py for real Turtle drawing."""
    st.markdown("""
    <div style="display:flex;justify-content:center;padding:8px 0">
    <svg width="230" height="150" viewBox="0 0 230 150" role="img" aria-label="Green turtle illustration">
      <ellipse cx="112" cy="91" rx="63" ry="38" fill="#77a96e"/>
      <path d="M67 88 Q112 25 158 88 Q147 127 111 128 Q76 126 67 88" fill="#3f8056"/>
      <path d="M83 89 Q112 54 142 89 Q135 112 112 114 Q90 112 83 89" fill="#a8c98a" stroke="#d9edc6" stroke-width="3"/>
      <path d="M112 57 L112 113 M84 88 L141 88 M96 65 L96 108 M128 65 L128 108" stroke="#6e9f63" stroke-width="3" fill="none"/>
      <circle cx="177" cy="82" r="22" fill="#8dbd76"/>
      <circle cx="184" cy="77" r="3.5" fill="#183c2d"/><circle cx="169" cy="77" r="3.5" fill="#183c2d"/>
      <path d="M170 89 Q177 97 185 89" fill="none" stroke="#183c2d" stroke-width="2.5" stroke-linecap="round"/>
      <ellipse cx="68" cy="125" rx="15" ry="10" fill="#8dbd76"/><ellipse cx="151" cy="125" rx="15" ry="10" fill="#8dbd76"/>
      <path d="M112 22 Q125 -1 149 13 Q143 37 112 38 Q105 31 112 22" fill="#a7c987"/>
      <path d="M112 37 Q127 23 143 16" stroke="#4e8a58" stroke-width="2" fill="none"/>
    </svg></div>
    """, unsafe_allow_html=True)

def safe(value):
    return html.escape(str(value))

with st.sidebar:
    st.markdown("## 🌿 ShopImpact")
    st.caption("Small choices. Greener tomorrows.")
    page = st.radio("YOUR SPACE", ["🏡 Dashboard","➕ Add a purchase","📚 My purchase history","🌍 Green guide"])
    st.divider()
    st.markdown("**Your mindful shopping reminder**")
    st.info("You do not need to be perfect. Every thoughtful choice is a step forward.")
    st.caption("ShopImpact • Python + Streamlit")

st.markdown("""
<div class="hero">
 <div class="pill">YOUR FRIENDLY CONSCIOUS-SHOPPING COMPANION</div>
 <h1>Shop better. Feel greener. 🌿</h1>
 <p>Track planned purchases, understand their estimated carbon impact, and discover simple ways to make more mindful choices.</p>
</div>
""", unsafe_allow_html=True)

purchases = st.session_state.purchases
df = pd.DataFrame(purchases)
if not df.empty:
    # datetime is used to parse saved timestamps and group entries by calendar month.
    df["created_at"] = pd.to_datetime(df["created_at"])
    this_month = datetime.now().strftime("%Y-%m")
    month_df = df[df["created_at"].dt.strftime("%Y-%m") == this_month]
else:
    month_df = pd.DataFrame()

spend = float(month_df["price"].sum()) if not month_df.empty else 0.0
impact = float(month_df["impact"].sum()) if not month_df.empty else 0.0
count = len(month_df)

if page == "🏡 Dashboard":
    st.markdown("### Your impact at a glance")
    st.markdown("<p class='small-muted'>A quick look at purchases you have logged this month.</p>", unsafe_allow_html=True)
    a,b,c = st.columns(3)
    for col, label, value, note in [
        (a,"💸 MONTHLY SPENDING",f"₹{spend:,.0f}",f"Across {count} logged purchase(s)"),
        (b,"☁️ ESTIMATED CO₂e",f"{impact:.2f} kg","Illustrative estimate this month"),
        (c,"🧺 PURCHASES TRACKED",str(count),"Every entry builds awareness")
    ]:
        with col:
            st.markdown(f"<div class='metric-card'><div class='metric-label'>{label}</div><div class='metric-value'>{value}</div><div class='metric-note'>{note}</div></div>",unsafe_allow_html=True)

    left,right = st.columns([1.25,.85],gap="large")
    with left:
        st.markdown("<div class='panel'>",unsafe_allow_html=True)
        st.markdown("#### 📊 Your monthly shopping snapshot")
        if not month_df.empty:
            chart = month_df.groupby("product_type",as_index=False).agg({"price":"sum","impact":"sum"})
            st.bar_chart(chart.set_index("product_type")[["price"]],use_container_width=True)
            st.caption("Spending by product category (₹).")
            st.dataframe(month_df[["created_at","product_type","brand","price","impact"]].rename(columns={
                "created_at":"Added at","product_type":"Category","brand":"Brand","price":"Price (₹)","impact":"Estimated CO₂e (kg)"
            }),use_container_width=True,hide_index=True)
        else:
            st.info("Your dashboard is ready! Add your first purchase to see your monthly chart.")
        st.markdown("</div>",unsafe_allow_html=True)
    with right:
        st.markdown("<div class='panel'>",unsafe_allow_html=True)
        st.markdown("#### 🏅 Your eco badges")
        badges = get_badges(purchases)
        if badges:
            for emoji,title,description in badges:
                st.markdown(f"<div class='badge'>{emoji} {safe(title)}</div><div class='small-muted'>{safe(description)}</div><br>",unsafe_allow_html=True)
        else:
            st.write("Your first badge is waiting for you.")
        turtle_fallback_svg()
        st.markdown("</div>",unsafe_allow_html=True)
    st.markdown("<div class='tip'>💡 <b>A little green thought:</b> "+safe(st.session_state.tip)+"</div>",unsafe_allow_html=True)
    if st.button("✨ Give me another eco tip"):
        st.session_state.tip = random.choice(ECO_TIPS)
        st.rerun()

elif page == "➕ Add a purchase":
    st.markdown("### Add a planned purchase 🛍️")
    st.markdown("<p class='small-muted'>Add an item to estimate its impact and get a greener idea.</p>",unsafe_allow_html=True)
    with st.form("purchase_form",clear_on_submit=True):
        x,y = st.columns(2)
        with x:
            product_type = st.selectbox("What are you shopping for?",list(PRODUCT_MULTIPLIERS))
            brand = st.text_input("Brand or store name",placeholder="e.g. Brand name")
        with y:
            price = st.number_input("Planned price (₹)",min_value=1.0,max_value=1000000.0,value=500.0,step=50.0)
            planned_date = st.date_input("Planned purchase date",value=date.today())
        choice = st.radio("How would you describe this choice?",["Regular choice","More sustainable choice"],horizontal=True)
        submitted = st.form_submit_button("🌱 Calculate my impact",use_container_width=True)
    if submitted:
        if not brand.strip():
            st.error("Please enter a brand or store name.")
        else:
            estimate = estimate_impact(product_type,price)
            # Keep planned date and exact creation time as datetime values.
            created_at = datetime.combine(planned_date, datetime.now().time()).isoformat(timespec="seconds")
            st.session_state.purchases.append({
                "product_type":product_type,"brand":brand.strip(),"price":float(price),
                "planned_date":planned_date.isoformat(),"created_at":created_at,
                "impact":estimate,"choice":choice
            })
            st.success("Purchase added! Your dashboard has been updated.")
            st.markdown(f"<div class='metric-card'><div class='metric-label'>YOUR ESTIMATED IMPACT</div><div class='metric-value'>{estimate:.2f} kg CO₂e</div><div class='metric-note'>For {safe(product_type)} • ₹{price:,.0f} • {safe(brand)}</div></div>",unsafe_allow_html=True)
            st.markdown("#### 🌿 A greener idea")
            for suggestion in ALTERNATIVES[product_type]:
                st.markdown(f"- {suggestion}")
            if choice == "More sustainable choice":
                st.success("🌱 Great! Your conscious-choice badge is ready to celebrate.")
                turtle_fallback_svg()
            st.caption("These suggestions are general ideas, not endorsements of specific brands.")
            st.balloons()
    st.markdown("<div class='tip'>CO₂e values are simplified classroom estimates, not verified product life-cycle assessments.</div>",unsafe_allow_html=True)

elif page == "📚 My purchase history":
    st.markdown("### Your shopping journal 📚")
    if purchases:
        history = pd.DataFrame(purchases)
        history["created_at"] = pd.to_datetime(history["created_at"])
        st.dataframe(history.rename(columns={
            "planned_date":"Planned date","created_at":"Added at","product_type":"Product type",
            "brand":"Brand","price":"Price (₹)","impact":"Estimated CO₂e (kg)","choice":"Choice"
        }),use_container_width=True,hide_index=True)
        st.download_button("⬇️ Download my purchase history (CSV)",
                           data=history.to_csv(index=False).encode("utf-8"),
                           file_name="shopimpact_purchases.csv",mime="text/csv")
        if st.button("🗑️ Clear all purchase history"):
            st.session_state.purchases = []
            st.rerun()
    else:
        st.info("No purchases yet. Add one to start your shopping journal.")

elif page == "🌍 Green guide":
    st.markdown("### Your simple green-shopping guide 🌍")
    st.write("You do not have to change everything at once. Start with one small action.")
    for category,ideas in ALTERNATIVES.items():
        with st.expander(f"🌱 {category}"):
            for idea in ideas:
                st.markdown(f"- {idea}")
    st.markdown("#### 💚 Five friendly habits")
    for habit in ["Make a short list before shopping.","Ask whether you can reuse something.","Choose products made to last.","Repair, borrow, share or buy second-hand when practical.","Dispose of electronics and packaging responsibly."]:
        st.markdown(f"- {habit}")
    st.markdown("<div class='tip'>ShopImpact encourages awareness—not guilt. Progress matters more than perfection.</div>",unsafe_allow_html=True)

st.divider()
st.markdown("<p style='text-align:center;color:#819082;font-size:.82rem;'>Made with 🌿 for more mindful shopping • ShopImpact</p>",unsafe_allow_html=True)
