import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import urllib.parse

# --- 1. පින්තූර ලින්ක්ස් (AI Generated) ---
img_home_url = "https://raw.githubusercontent.com/B-Buddika/BC-Scholar-Assets/main/image_0.png"
img_reg_url = "https://raw.githubusercontent.com/B-Buddika/BC-Scholar-Assets/main/image_2.png"
img_map_url = "https://raw.githubusercontent.com/B-Buddika/BC-Scholar-Assets/main/image_4.png"
img_class_url = "https://raw.githubusercontent.com/B-Buddika/BC-Scholar-Assets/main/image_6.png"
img_back_url = "https://raw.githubusercontent.com/B-Buddika/BC-Scholar-Assets/main/image_10.png"

# --- 2. පිටුවේ මූලික සැකසුම් ---
icon_url = "https://media.istockphoto.com/id/1455197782/vector/red-dharmachakra-wheel-of-dhamma-on-lotus-petals-sign-on-yellow-background-vector-design.jpg?s=612x612&w=0&k=20&c=eywlzFMds0xQEgg9FKSnIMcjDIgq4bsV5VysnZmc2d0="
st.set_page_config(page_title="BC-Scholar", page_icon=icon_url, layout="centered")

# --- 3. WhatsApp Group Links ---
WHATSAPP_GROUPS = {
    "2026 A/L": "https://chat.whatsapp.com/ElrGd68bvXDGEYw5XBEb1f",
    "2027 A/L": "https://chat.whatsapp.com/ElrGd68bvXDGEYw5XBEb1f",
    "2028 A/L": "https://chat.whatsapp.com/JZdWvJT6gX6J0uqUFNvTuK"
}

# --- 4. දිස්ත්‍රික්ක වල ඛණ්ඩාංක ---
DISTRICT_DATA = {
    "කොළඹ": {"lat": 6.9271, "lon": 79.8612}, "මහනුවර": {"lat": 7.2906, "lon": 80.6337},
    "ගාල්ල": {"lat": 6.0535, "lon": 80.2210}, "මාතර": {"lat": 5.9549, "lon": 80.5550},
    "කුරුණෑගල": {"lat": 7.4863, "lon": 80.3647}, "අනුරාධපුර": {"lat": 8.3114, "lon": 80.4037},
    "රත්නපුර": {"lat": 6.7056, "lon": 80.3847}, "කළුතර": {"lat": 6.5854, "lon": 79.9607},
    "බදුල්ල": {"lat": 6.9934, "lon": 81.0550}, "නුවරඑළිය": {"lat": 6.9497, "lon": 80.7891},
    "හම්බන්තොට": {"lat": 6.1246, "lon": 81.1185}, "පුත්තලම": {"lat": 8.0330, "lon": 79.8250},
    "කෑගල්ල": {"lat": 7.2513, "lon": 80.3464}, "මාතලේ": {"lat": 7.4675, "lon": 80.6234},
    "පොළොන්නරුව": {"lat": 7.9397, "lon": 81.0036}, "මොනරාගල": {"lat": 6.8724, "lon": 81.3507},
    "අම්පාර": {"lat": 7.2842, "lon": 81.6747}, "ත්‍රිකුණාමලය": {"lat": 8.5711, "lon": 81.2335},
    "මඩකලපුව": {"lat": 7.7302, "lon": 81.6747}, "වවුනියාව": {"lat": 8.7542, "lon": 80.4982},
    "මන්නාරම": {"lat": 8.9810, "lon": 79.9044}, "මුලතිවු": {"lat": 9.2671, "lon": 80.8142},
    "කිලිනොච්චිය": {"lat": 9.3803, "lon": 80.4037}, "යාපනය": {"lat": 9.6615, "lon": 80.0255}
}

# --- 5. Google Sheet Connection ---
conn = st.connection("gsheets", type=GSheetsConnection)

# --- 6. CSS (Fixing Syntax Error) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Kotta+One&family=Yaldevi:wght@300;500;700&display=swap');
    
    .stApp {{
        background: linear-gradient(rgba(255, 249, 230, 0.9), rgba(255, 249, 230, 0.9)), 
                    url("{img_back_url}");
        background-size: cover;
        background-attachment: fixed;
    }}

    .main-title {{
        font-family: 'Kotta One', serif;
        color: #800000;
        text-align: center;
        font-size: 55px; /* Clamp එක වෙනුවට Fix අගයක් දැම්මා Error එක වළක්වන්න */
        font-weight: bold;
        margin-top: -10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }}

    .sub-title {{
        font-family: 'Yaldevi', sans-serif;
        color: #e67e22;
        text-align: center;
        font-size: 22px;
        font-weight: bold;
        margin-bottom: 30px;
    }}

    .stMarkdown, p, label, .stSelectbox, .stTextInput {{
        font-family: 'Yaldevi', sans-serif !important;
        color: #4b2c20 !important;
    }}

    .stTabs [data-baseweb="tab"] {{
        background-color: rgba(253, 242, 233, 0.9);
        font-family: 'Yaldevi', sans-serif !important;
        font-weight: 700 !important;
    }}

    .stButton>button {{
        width: 100%;
        background: linear-gradient(90deg, #800000 0%, #a52a2a 100%);
        color: white;
        border-radius: 15px;
        height: 50px;
    }}

    img {{
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 7. Header Section ---
st.markdown('<p class="main-title">BC-Scholar</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">බෞද්ධ ශිෂ්ටාචාරය - අලුත් ගමනක ඇරඹුම...!</p>', unsafe_allow_html=True)

# --- 8. Navigation Tabs ---
menu = st.tabs(["🏠 මුල් පිටුව", "📝 ලියාපදිංචිය", "📊 ශිෂ්‍ය සිතියම", "📚 නිබන්ධන", "🎥 පන්ති"])

with menu[0]:
    st.image(img_home_url, use_container_width=True)
    st.markdown("### ආයුබෝවන්!")
    st.write("බෞද්ධ ශිෂ්ටාචාරය විෂය සරලව ඉගෙන ගැනීමට BC-Scholar වෙත ඔබව සාදරයෙන් පිළිගනිමු.")
    st.markdown("**ගුරු මෙහෙයවීම : බුද්ධික සම්පත්**")
    
    contact_msg = urllib.parse.quote("ආයුබෝවන් සර්, මට පන්ති පිළිබඳ විස්තර දැනගැනීමට අවශ්‍යයි.")
    st.link_button("📞 Contact Teacher (WhatsApp)", f"https://wa.me/94779316692?text={contact_msg}")

with menu[1]:
    st.image(img_reg_url, use_container_width=True)
    with st.form("reg_form", clear_on_submit=True):
        name = st.text_input("සම්පූර්ණ නම")
        phone = st.text_input("WhatsApp අංකය")
        batch = st.selectbox("විභාග වර්ෂය", list(WHATSAPP_GROUPS.keys()))
        dist = st.selectbox("දිස්ත්‍රික්කය", list(DISTRICT_DATA.keys()))
        if st.form_submit_button("ලියාපදිංචි වන්න"):
            if name and phone:
                df = conn.read(ttl=0)
                new_data = pd.DataFrame([{"Timestamp": datetime.now(), "නම": name, "දුරකථන_අංකය": phone, "කණ්ඩායම": batch, "දිස්ත්‍රික්කය": dist, "lat": DISTRICT_DATA[dist]["lat"], "lon": DISTRICT_DATA[dist]["lon"]}])
                conn.update(data=pd.concat([df, new_data]))
                st.success("සාර්ථකයි!")
                st.link_button(f"Join {batch} Group", WHATSAPP_GROUPS[batch])
            else:
                st.warning("විස්තර ඇතුළත් කරන්න.")

with menu[2]:
    st.image(img_map_url, use_container_width=True)
    data = conn.read(ttl=0)
    if data is not None: st.map(data[['lat', 'lon']].dropna())

with menu[3]:
    st.markdown("### 📚 නිබන්ධන")
    pw = st.text_input("Password", type="password")
    if pw == "BC123":
        st.link_button("Download Tutes", "https://drive.google.com/drive/folders/1MoGZVGhnEvv-sBwwivd9mIeU-Tybu8uL")

with menu[4]:
    st.image(img_class_url, use_container_width=True)
    st.link_button("Join Live Zoom Class", "https://zoom.us")
