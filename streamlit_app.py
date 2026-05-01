import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import urllib.parse

# --- 1. පින්තූර වල නිවැරදි links (AI Generated) ---
# ඔයා හොයාගත්තු නිවැරදි links ටික මෙන්න මේ විදියට variable වලට දැම්මා
img_home_url = "https://github.com/buddhika1999b-wq/bc-scholar-web/blob/main/home.png.png?raw=true"
img_reg_url = "https://github.com/buddhika1999b-wq/bc-scholar-web/blob/main/reg.png.png?raw=true"
img_map_url = "https://github.com/buddhika1999b-wq/bc-scholar-web/blob/main/map.png.png?raw=true"
img_class_url = "https://github.com/buddhika1999b-wq/bc-scholar-web/blob/main/class.png.png?raw=true"
img_back_url = "https://github.com/buddhika1999b-wq/bc-scholar-web/blob/main/bg.png?raw=true"

# --- 2. පිටුවේ මූලික සැකසුම් ---
icon_url = "https://media.istockphoto.com/id/1455197782/vector/red-dharmachakra-wheel-of-dhamma-on-lotus-petals-sign-on-yellow-background-vector-design.jpg?s=612x612&w=0&k=20&c=eywlzFMds0xQEgg9FKSnIMcjDIgq4bsV5VysnZmc2d0="
st.set_page_config(page_title="BC-Scholar", page_icon=icon_url, layout="centered")

# --- 3. WhatsApp Group Links ---
WHATSAPP_GROUPS = {
    "2026 A/L": "https://chat.whatsapp.com/ElrGd68bvXDGEYw5XBEb1f",
    "2027 A/L": "https://chat.whatsapp.com/ElrGd68bvXDGEYw5XBEb1f",
    "2028 A/L": "https://chat.whatsapp.com/JZdWvJT6gX6J0uqUFNvTuK"
}

# --- 4. දිස්ත්‍රික්ක වල ඛණ්ඩාංක (Map එක සඳහා) ---
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

# --- 6. CSS (Design & Styles) ---
# මෙතන url() එක ඇතුළට img_back_url එක දාලා background එක transparent කළා
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Kotta+One&family=Yaldevi:wght@300;500;700&display=swap');
    
    /* මුළු App එකේම Background එක (Transparent සහ Fixed) */
    .stApp {{
        background: linear-gradient(rgba(255, 249, 230, 0.85), rgba(255, 249, 230, 0.85)), 
                    url("{img_back_url}");
        background-size: cover;
        background-attachment: fixed;
    }}

    /* ප්‍රධාන මාතෘකාව (BC-Scholar) */
    .main-title {{
        font-family: 'Kotta One', serif;
        color: #800000;
        text-align: center;
        font-size: clamp(35px, 8vw, 65px);
        font-weight: bold;
        margin-top: -20px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }}

    /* උප මාතෘකාව */
    .sub-title {{
        font-family: 'Yaldevi', sans-serif;
        color: #e67e22;
        text-align: center;
        font-size: clamp(16px, 4vw, 24px);
        font-weight: 700;
        margin-bottom: 30px;
    }}

    /* පන්ති සහ ලේබල් වල ෆොන්ට් එක */
    .stMarkdown, p, label, .stSelectbox, .stTextInput {{
        font-family: 'Yaldevi', sans-serif !important;
        font-weight: 500 !important;
        color: #4b2c20 !important;
    }}

    /* Tabs (මුල් පිටුව, ලියාපදිංචිය) */
    .stTabs [data-baseweb="tab-list"] {{
        justify-content: center;
    }}
    .stTabs [data-baseweb="tab"] {{
        background-color: rgba(253, 242, 233, 0.9);
        border-radius: 10px 10px 0px 0px;
        padding: 10px 15px;
        font-family: 'Yaldevi', sans-serif !important;
        font-weight: 700 !important;
    }}

    /* බොත්තම් (Buttons) */
    .stButton>button {{
        width: 100%;
        font-family: 'Yaldevi', sans-serif !important;
        background: linear-gradient(90deg, #800000 0%, #a52a2a 100%);
        color: white;
        border-radius: 15px;
        height: 55px;
        font-weight: 700 !important;
        border: none;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: 0.3s;
    }}
    
    .stButton>button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }}

    /* පින්තූර මැදට ගැනීම සහ Shadow */
    .centered-image {{
        display: flex;
        justify-content: center;
        margin-bottom: 10px;
    }}
    
    img {{
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 7. Header Section ---
st.markdown(f'<div class="centered-image"><img src="{icon_url}" width="70"></div>', unsafe_allow_html=True)
st.markdown('<p class="main-title">BC-Scholar</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">බෞද්ධ ශිෂ්ටාචාරය - අලුත් ගමනක ඇරඹුම...!</p>', unsafe_allow_html=True)

# --- 8. Navigation Tabs ---
menu = st.tabs(["🏠 මුල් පිටුව", "📝 ලියාපදිංචිය", "📊 ශිෂ්‍ය සිතියම", "📚 නිබන්ධන", "🎥 පන්ති"])

with menu[0]:
    # මුල් පිටුවේ පින්තූරය (img_home_url)
    st.image(img_home_url, use_container_width=True)
    st.markdown("""
    <div style='font-family: "Yaldevi", sans-serif; font-size: 18px;'>
    <br><b>ආයුබෝවන්!</b><br>
    බෞද්ධ ශිෂ්ටාචාරය විෂය ඉතාමත් සරලව සහ ක්‍රමානුකූලව ඉගෙන ගැනීමට <b>BC-Scholar</b> ඩිජිටල් පද්ධතිය ඔබට උදව් වනු ඇත.<br><br>
    <b>ගුරු මෙහෙයවීම :</b><br>
    <b>බුද්ධික සම්පත්</b> - B.Sc (Hons) in GIS, University of Peradeniya
    </div>
    """, unsafe_allow_html=True)
    
    # Contact Teacher
    contact_msg = urllib.parse.quote("ආයුබෝවන් සර්, මට පන්ති පිළිබඳ විස්තර දැනගැනීමට අවශ්‍යයි.")
    st.link_button("📞 Contact Teacher (WhatsApp)", f"https://wa.me/94779316692?text={contact_msg}")

with menu[1]:
    # ලියාපදිංචි පිටුවේ පින්තූරය (img_reg_url)
    st.image(img_reg_url, use_container_width=True)
    st.markdown("<h3 style='color: #800000; text-align: center; font-family: \"Yaldevi\", sans-serif;'>නව ශිෂ්‍ය ලියාපදිංචිය</h3>", unsafe_allow_html=True)
    
    with st.form("registration_form", clear_on_submit=True):
        name = st.text_input("සම්පූර්ණ නම")
        phone = st.text_input("WhatsApp දුරකථන අංකය")
        batch_selection = st.selectbox("විභාග වර්ෂය", list(WHATSAPP_GROUPS.keys()))
        district = st.selectbox("දිස්ත්‍රික්කය", list(DISTRICT_DATA.keys()))
        submit = st.form_submit_button("දත්ත ඇතුළත් කරන්න")
        
        if submit:
            if name and phone:
                try:
                    # Google Sheet එක කියවීම
                    df = conn.read(ttl=0)
                    # නව දත්ත
                    new_entry = pd.DataFrame([{
                        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "නම": name, "දුරකථන_අංකය": phone, "කණ්ඩායම": batch_selection,
                        "දිස්ත්‍රික්කය": district, "තත්ත්වය": "Pending", 
                        "lat": DISTRICT_DATA[district]["lat"], "lon": DISTRICT_DATA[district]["lon"]
                    }])
                    # දත්ත එකතු කිරීම
                    updated_df = pd.concat([df, new_entry], ignore_index=True) if df is not None and not df.empty else new_entry
                    # Google Sheet එක Update කිරීම
                    conn.update(data=updated_df)
                    
                    st.balloons()
                    st.success(f"ස්තූතියි {name}! ඔබ සාර්ථකව ලියාපදිංචි වුණා.")
                    
                    st.markdown(f"<div style='font-family: \"Yaldevi\", sans-serif;'><h4>✅ දැන් පහත බටන් එකෙන් ඔබේ {batch_selection} සමූහයට එකතු වන්න:</h4></div>", unsafe_allow_html=True)
                    st.link_button(f"Join {batch_selection} WhatsApp Group", WHATSAPP_GROUPS[batch_selection])
                    
                    # Contact Card (VCF)
                    vcf_data = f"BEGIN:VCARD\nVERSION:3.0\nFN:{name} BC\nTEL;TYPE=CELL:{phone}\nEND:VCARD"
                    st.download_button(label="📥 Contact එක Save කරගන්න", data=vcf_data, file_name=f"{name}_BC.vcf", mime="text/vcard")
                except:
                    st.error("දත්ත ඇතුළත් කිරීමේදී දෝෂයක් ඇති විය.")
            else:
                st.warning("කරුණාකර සියලු විස්තර සම්පූර්ණ කරන්න.")

with menu[2]:
    # සිතියම් පිටුවේ පින්තූරය (img_map_url)
    st.image(img_map_url, use_container_width=True)
    st.markdown("<h3 style='color: #800000; text-align: center; font-family: \"Yaldevi\", sans-serif;'>ශිෂ්‍ය ව්‍යාප්තිය</h3>", unsafe_allow_html=True)
    try:
        # දත්ත කියවා සිතියම පෙන්වීම
        data = conn.read(ttl=0)
        if data is not None and not data.empty:
            st.map(data[['lat', 'lon']].dropna(), color="#800000")
    except:
        st.error("සිතියම පූරණය කළ නොහැක.")

with menu[3]:
    st.markdown("<div style='font-family: \"Yaldevi\", sans-serif;'><h3>📚 නිබන්ධන (Tutes)</h3></div>", unsafe_allow_html=True)
    pw = st.text_input("මුරපදය ඇතුළත් කරන්න", type="password")
    if pw == "BC123":
        st.success("Access Granted!")
        st.link_button("Download Tutes (Google Drive)", "https://drive.google.com/drive/folders/1MoGZVGhnEvv-sBwwivd9mIeU-Tybu8uL?usp=drive_link")

with menu[4]:
    # පන්ති පිටුවේ පින්තූරය (img_class_url)
    st.image(img_class_url, use_container_width=True)
    st.markdown("<div style='font-family: \"Yaldevi\", sans-serif;'><h3>🎥 සජීවී Zoom පන්ති</h3></div>", unsafe_allow_html=True)
    st.info("පන්තිය ආරම්භ වීමට නියමිත වේලාවට පහත බොත්තම භාවිතා කරන්න.")
    st.link_button("සජීවී Zoom පන්තියට මෙතනින්", "https://zoom.us")
