import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# පිටුවේ සැකසුම් (Page Settings)
st.set_page_config(page_title="BC-scholar", page_icon="☸️", layout="centered")

# Google Sheet එකට සම්බන්ධ වීම
url = "https://docs.google.com/spreadsheets/d/1p4TNbQ2wAHd9Ug9Uh2YXP3TL_i2NVFNnD0GGchhfAVE/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

# CSS - සිංහල අකුරු සහ Branding ලස්සනට පෙන්වීමට
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Sinhala:wght@400;700&display=swap');
    html, body, [class*="css"]  { font-family: 'Noto Sans Sinhala', sans-serif; }
    .stButton>button { 
        width: 100%; 
        background-color: #800000; 
        color: white; 
        border-radius: 10px;
        height: 50px;
        font-weight: bold;
    }
    .main-title { color: #800000; text-align: center; font-size: 45px; font-weight: bold; margin-bottom: 0px; }
    .sub-title { color: #ff9933; text-align: center; font-size: 20px; font-weight: bold; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_stdio=True)

st.markdown('<p class="main-title">☸️ BC-scholar</p>', unsafe_allow_stdio=True)
st.markdown('<p class="sub-title">බෞද්ධ ශිෂ්ටාචාරය - ඩිජිටල් අධ්‍යාපන පද්ධතිය</p>', unsafe_allow_stdio=True)

# Tabs (මෙනුව)
menu = st.tabs(["🏠 මුල් පිටුව", "📝 ලියාපදිංචිය", "📚 නිබන්ධන", "🎥 පන්ති"])

with menu[0]:
    st.image("https://images.unsplash.com/photo-1590059447767-6f139accf48d?auto=format&fit=crop&q=80&w=1000", caption="BC-scholar - පණ්ඩිතයන්ගේ තේරීම", use_container_width=True)
    st.write("### ආයුබෝවන්!")
    st.write("බෞද්ධ ශිෂ්ටාචාරය විෂය ඉතාමත් සරලව සහ ක්‍රමානුකූලව ඉගෙන ගැනීමට BC-scholar පද්ධතිය ඔබට උදව් වනු ඇත. සියලුම නිබන්ධන සහ Zoom ලින්ක් ලබා ගැනීමට ලියාපදිංචි වන්න.")
    st.info("පහත බොත්තම එබීමෙන් ඔබේ WhatsApp සමූහයට එකතු වන්න.")
    st.link_button("Official WhatsApp Group එකට එකතු වන්න", "https://chat.whatsapp.com/LInK_HeRe")

with menu[1]:
    st.subheader("නව ශිෂ්‍ය ලියාපදිංචිය")
    with st.form("registration_form", clear_on_submit=True):
        name = st.text_input("සම්පූර්ණ නම")
        phone = st.text_input("WhatsApp දුරකථන අංකය")
        batch = st.selectbox("විභාග වර්ෂය", ["2026 A/L", "2027 A/L", "2028 A/L"])
        district = st.selectbox("දිස්ත්‍රික්කය", ["කොළඹ", "මහනුවර", "ගාල්ල", "මාතර", "කුරුණෑගල", "අනුරාධපුර", "රත්නපුර", "කළුතර", "වෙනත්"])
        
        submit = st.form_submit_button("දත්ත ඇතුළත් කරන්න")
        
        if submit:
            if name and phone:
                try:
                    # දැනට තියෙන Data කියවීම
                    existing_data = conn.read(spreadsheet=url, usecols=[0,1,2,3,4,5])
                    
                    # අලුත් Data පේළිය
                    new_entry = pd.DataFrame([{
                        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "නම": name,
                        "දුරකථන_අංකය": phone,
                        "කණ්ඩායම": batch,
                        "දිස්ත්‍රික්කය": district,
                        "තත්ත්වය": "Pending"
                    }])
                    
                    # දෙකම එකතු කිරීම
                    updated_df = pd.concat([existing_data, new_entry], ignore_index=True)
                    
                    # Google Sheet එක Update කිරීම
                    conn.update(spreadsheet=url, data=updated_df)
                    st.success(f"ස්තූතියි {name}! ඔබ සාර්ථකව ලියාපදිංචි වුණා.")
                    st.balloons()
                except Exception as e:
                    st.error(f"දෝෂයක් ඇතිවිය: {e}")
            else:
                st.warning("කරුණාකර නම සහ දුරකථන අංකය ඇතුළත් කරන්න.")

with menu[2]:
    st.subheader("නිබන්ධන (Tutes) බාගත කරගන්න")
    pw = st.text_input("මුරපදය ඇතුළත් කරන්න", type="password")
    if pw == "BC123":
        st.success("මුරපදය නිවැරදියි!")
        st.write("📄 **පළමු ඒකකය - නිබන්ධනය**")
        st.link_button("Download Tute (PDF)", "https://docs.google.com/your-tute-link")
    elif pw != "":
        st.error("වැරදි මුරපදයක්! කරුණාකර ගුරුවරයාගෙන් විමසන්න.")

with menu[3]:
    st.subheader("සජීවී Zoom පන්ති")
    st.warning("සජීවී පන්තිය ආරම්භ වූ පසු Zoom ලින්ක් එක මෙතැන දිස්වේ.")
    st.link_button("Zoom පන්තියට සම්බන්ධ වන්න", "https://zoom.us")
