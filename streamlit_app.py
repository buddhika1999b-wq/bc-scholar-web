import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# පිටුවේ සැකසුම්
st.set_page_config(page_title="BC-Scholar", page_icon="☸️", layout="centered")

# දිස්ත්‍රික්ක වල ඛණ්ඩාංක (සිතියම සඳහා)
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

# CSS - UI එක ලස්සන කිරීම
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Sinhala:wght@400;700&display=swap');
    html, body, [class*="css"]  { font-family: 'Noto Sans Sinhala', sans-serif; }
    .stButton>button { width: 100%; background-color: #800000; color: white; border-radius: 10px; height: 50px; font-weight: bold; }
    .main-title { color: #800000; text-align: center; font-size: 45px; font-weight: bold; margin-bottom: 0px; }
    .sub-title { color: #ff9933; text-align: center; font-size: 20px; font-weight: bold; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-title">☸️ BC-Scholar</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">බෞද්ධ ශිෂ්ටාචාරය - ඩිජිටල් අධ්‍යාපන පද්ධතිය</p>', unsafe_allow_html=True)

menu = st.tabs(["🏠 මුල් පිටුව", "📝 ලියාපදිංචිය", "📊 ශිෂ්‍ය සිතියම", "📚 නිබන්ධන", "🎥 පන්ති"])

with menu[0]:
    st.image("https://images.unsplash.com/photo-1548013146-72479768bbaa?auto=format&fit=crop&q=80&w=1000", width=700)
    st.write("### ආයුබෝවන්!")
    st.write("බෞද්ධ ශිෂ්ටාචාරය විෂය ඉතාමත් සරලව සහ ක්‍රමානුකූලව ඉගෙන ගැනීමට BC-scholar පද්ධතිය ඔබට උදව් වනු ඇත.")
    st.link_button("Official WhatsApp Group", "https://chat.whatsapp.com/LInK_HeRe")

with menu[1]:
    st.subheader("නව ශිෂ්‍ය ලියාපදිංචිය")
    with st.form("registration_form", clear_on_submit=True):
        name = st.text_input("සම්පූර්ණ නම")
        phone = st.text_input("WhatsApp දුරකථන අංකය (උදා: 07XXXXXXXX)")
        batch = st.selectbox("විභාග වර්ෂය", ["2026 A/L", "2027 A/L", "2028 A/L"])
        district = st.selectbox("දිස්ත්‍රික්කය", list(DISTRICT_DATA.keys()))
        submit = st.form_submit_button("දත්ත ඇතුළත් කරන්න")
        
        if submit:
            if name and phone:
                try:
                    # 1. පවතින දත්ත කියවීම (Cache මකන්න ttl=0 දාලා තියෙන්නේ)
                    df = conn.read(ttl=0)
                    
                    # 2. අලුත් පෙළ සැකසීම
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
                    
                    # 3. දත්ත එකතු කිරීම
                    if df is not None and not df.empty:
                        updated_df = pd.concat([df, new_entry], ignore_index=True)
                    else:
                        updated_df = new_entry
                    
                    # 4. Sheet එකට යැවීම
                    conn.update(data=updated_df)
                    
                    st.success(f"ස්තූතියි {name}! ඔබ සාර්ථකව ලියාපදිංචි වුණා.")
                    
                    # --- AUTO SAVE CONTACT SYSTEM ---
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
    st.subheader("ලියාපදිංචි වී ඇති ශිෂ්‍ය ව්‍යාප්තිය")
    try:
        # Cache එක refresh කරන්න ttl=0
        data = conn.read(ttl=0)
        if data is not None and not data.empty and 'lat' in data.columns:
            # සිතියම ඇඳීමට අවශ්‍ය Columns පමණක් තෝරා ගැනීම
            map_df = data[['lat', 'lon']].dropna()
            st.map(map_df)
        else:
            st.info("තවම සිතියමේ පෙන්වීමට දත්ත නොමැත. කරුණාකර පළමුව ලියාපදිංචි වන්න.")
    except Exception as e:
        st.error(f"සිතියම පෙන්වීමේදී දෝෂයක් ඇති විය: {e}")

with menu[3]:
    st.subheader("නිබන්ධන (Tutes)")
    pw = st.text_input("මුරපදය ඇතුළත් කරන්න", type="password")
    if pw == "BC123":
        st.success("මුරපදය නිවැරදියි!")
        st.link_button("Download Tute (PDF)", "https://docs.google.com/your-tute-link")

with menu[4]:
    st.subheader("සජීවී Zoom පන්ති")
    st.link_button("Zoom පන්තියට සම්බන්ධ වන්න", "https://zoom.us")
