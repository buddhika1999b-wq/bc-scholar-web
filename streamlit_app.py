import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="BC-scholar", page_icon="☸️")

# Connection එක හදාගැනීම
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("☸️ BC-scholar ලියාපදිංචිය")

with st.form("reg_form", clear_on_submit=True):
    name = st.text_input("නම")
    phone = st.text_input("දුරකථන අංකය")
    batch = st.selectbox("වසර", ["2026", "2027", "2028"])
    district = st.text_input("දිස්ත්‍රික්කය")
    submit = st.form_submit_button("ලියාපදිංචි වන්න")
    
    if submit:
        if name and phone:
            # අලුත් පේළිය හදාගන්නවා
            new_row = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "නම": name,
                "දුරකථන_අංකය": phone,
                "කණ්ඩායම": batch,
                "දිස්ත්‍රික්කය": district,
                "තත්ත්වය": "Pending"
            }])
            
            # පවතින දත්ත කියවීම
            existing_df = conn.read()
            
            # දෙක එකතු කිරීම
            updated_df = pd.concat([existing_df, new_row], ignore_index=True)
            
            # Sheet එකට යැවීම
            conn.update(data=updated_df)
            
            st.success("සාර්ථකයි! Sheet එක චෙක් කරලා බලන්න.")
            st.balloons()
        else:
            st.error("විස්තර ඇතුළත් කරන්න.")
