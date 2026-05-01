import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# පිටුවේ සැකසුම්
st.set_page_config(page_title="BC-Scholar", page_icon="☸️", layout="centered")

# දිස්ත්‍රික්ක වල ඛණ්ඩාංක
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

# Google Sheet Connection
conn = st.connection("gsheets", type=GSheetsConnection)

# CSS - පෙනුම ලස්සන කිරීම (UI/UX)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Abhaya+Libre:wght@700&family=Noto+Sans+Sinhala:wght@400;700&display=swap');
    
    /* මුළු පිටුවේම අකුරු */
    html, body, [class*="css"] {
        font-family: 'Noto Sans Sinhala', sans-serif;
        background-color: #fffaf5;
    }

    /* ප්‍රධාන මාතෘකාව */
    .main-title {
        font-family: 'Abhaya Libre', serif;
        color: #800000;
        text-align: center;
        font-size: 55px;
        font-weight: bold;
        margin-bottom: 0px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }

    /* උප මාතෘකාව */
    .sub-title {
        color: #e67e22;
        text-align: center;
        font-size: 22px;
        font-weight: bold;
        margin-bottom: 30px;
    }

    /* Button ලස්සන කිරීම */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #800000 0%, #a52a2a 100%);
        color: white;
        border-radius: 15px;
        height: 55px;
        font-weight: bold;
        font-size: 18px;
        border: none;
        transition: 0.3s;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .stButton>button:hover {
        background: linear-gradient(90deg, #a52a2a 0%, #800000 100%);
        transform: translateY(-2px);
    }

    /* Tabs ලස්සන කිරීම */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        justify-content: center;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: #fdf2e9;
        border-radius: 10px 10px 0px 0px;
        padding: 10px 20px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Header කොටස
st.markdown('<p class="main-title">☸️ BC-Scholar</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">බෞද්ධ ශිෂ්ටාචාරය - අලුත් ගමනක ඇරඹුම...!</p>', unsafe_allow_html=True)

menu = st.tabs(["🏠 මුල් පිටුව", "📝 ලියාපදිංචිය", "📊 ශිෂ්‍ය සිතියම", "📚 නිබන්ධන", "🎥 පන්ති"])

with menu[0]:
    # වඩාත් ගුණාත්මක පින්තූරයක් (රුවන්වැලිසෑය)
    st.image("https://images.unsplash.com/photo-1625034606410-68196603a95d?q=80&w=1200&auto=format&fit=crop", use_container_width=True)
    st.markdown("""
    ### ආයුබෝවන්!
    බෞද්ධ ශිෂ්ටාචාරය විෂය ඉතාමත් සරලව සහ ක්‍රමානුකූලව ඉගෙන ගැනීමට **BC-Scholar** ඩිජිටල් පද්ධතිය ඔබට උදව් වනු ඇත. 
    අප සමඟ එක්ව විෂය කරුණු ඉතා පැහැදිලිව ඉගෙන ගන්න.
    """)
    st.link_button("Official WhatsApp Group එකට මෙතනින් එක්වන්න", "https://chat.whatsapp.com/LInK_HeRe")

with menu[1]:
    st.markdown("<h3 style='color: #800000; text-align: center;'>නව ශිෂ්‍ය ලියාපදිංචිය</h3>", unsafe_allow_html=True)
    with st.form("registration_form", clear_on_submit=True):
        name = st.text_input("සම්පූර්ණ නම")
        phone = st.text_input("WhatsApp දුරකථන අංකය (උදා: 07XXXXXXXX)")
        batch = st.selectbox("විභාග වර්ෂය", ["2026 A/L", "2027 A/L", "2028 A/L"])
        district = st.selectbox("දිස්ත්‍රික්කය", list(DISTRICT_DATA.keys()))
        submit = st.form_submit_button("ලියාපදිංචි වන්න")
        
        if submit:
            if name and phone:
                try:
                    df = conn.read(ttl=0)
                    new_entry = pd.DataFrame([{
                        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "නම": name, 
                        "දුරකථන_අංකය": phone, 
                        "කණ්ඩායම": batch,
                        "දිස්ත්‍රික්කය": district, 
                        "තත්ත්වය": "Pending", 
                        "lat": DISTRICT_DATA[district]["lat"], 
                        "lon": DISTRICT_DATA[district]["lon"]
                    }])
                    
                    if df is not None and not df.empty:
                        updated_df = pd.concat([df, new_entry], ignore_index=True)
                    else:
                        updated_df = new_entry
                    
                    conn.update(data=updated_df)
                    
                    st.success(f"ස්තූතියි {name}! ඔබ සාර්ථකව ලියාපදිංචි වුණා.")
                    
                    # VCF Contact System
                    vcf_data = f"BEGIN:VCARD\nVERSION:3.0\nFN:{name} BC\nTEL;TYPE=CELL:{phone}\nEND:VCARD"
                    st.download_button(
                        label="📥 ශිෂ්‍යයාගේ Contact එක Save කරගන්න මෙතන ඔබන්න",
                        data=vcf_data, 
                        file_name=f"{name}_BC.vcf", 
                        mime="text/vcard"
                    )
                    st.balloons()
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("කරුණාකර නම සහ දුරකථන අංකය ඇතුළත් කරන්න.")

with menu[2]:
    st.markdown("<h3 style='color: #800000; text-align: center;'>ශිෂ්‍ය ව්‍යාප්තිය (Live Map)</h3>", unsafe_allow_html=True)
    try:
        data = conn.read(ttl=0)
        if data is not None and not data.empty and 'lat' in data.columns:
            map_df = data[['lat', 'lon']].dropna()
            st.map(map_df, color="#800000")
        else:
            st.info("තවම සිතියමේ පෙන්වීමට දත්ත නොමැත.")
    except Exception as e:
        st.error(f"සිතියම පෙන්වීමේදී දෝෂයක් ඇති විය.")

with menu[3]:
    st.subheader("📚 නිබන්ධන (Tutes)")
    pw = st.text_input("මුරපදය ඇතුළත් කරන්න", type="password")
    if pw == "BC123":
        st.success("මුරපදය නිවැරදියි!")
        st.link_button("Download Tute (PDF)", "https://docs.google.com/your-tute-link")

with menu[4]:
    st.subheader("🎥 සජීවී Zoom පන්ති")
    st.info("පන්තිය ආරම්භ වීමට නියමිත වේලාවට ලින්ක් එක සක්‍රීය වේ.")
    st.link_button("සජීවී Zoom පන්තියට මෙතනින් සම්බන්ධ වන්න", "https://zoom.us")
