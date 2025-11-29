import streamlit as st
import pandas as pd
import requests
import time
import plotly.express as px


st.set_page_config(
    page_title="FinGuard Live Monitor",
    page_icon="🛡️",
    layout="wide",
)


API_URL = "http://127.0.0.1:8000"

st.title("🛡️ FinGuard: Real-Time Fraud Detection System")
st.markdown("---")


kpi1, kpi2, kpi3 = st.columns(3)
chart_col1, chart_col2 = st.columns(2)
st.subheader("🚨 Son Tespit Edilen Alarmlar (Canlı Akış)")
table_placeholder = st.empty()

def fetch_data():

    try:
     
        stats_res = requests.get(f"{API_URL}/stats")
        stats_data = stats_res.json()
        
        alerts_res = requests.get(f"{API_URL}/alerts")
        alerts_data = alerts_res.json()
        
        return stats_data, alerts_data
    except Exception as e:
        return None, None


while True:
    stats, alerts = fetch_data()
    
    if stats and alerts:
        df = pd.DataFrame(alerts['data'])
    
        
        kpi1.metric(
            label="Toplam Yakalanan Fraud",
            value=stats['total_fraud_detected'],
            delta=f"+{len(df)} Son saatte" 
        )
        
        last_amount = df.iloc[0]['amount'] if not df.empty else 0
        kpi2.metric(
            label="Son Yakalanan Tutar",
            value=f"{last_amount} TL",
            delta_color="inverse"
        )

        kpi3.metric(
            label="Sistem Durumu",
            value="AKTİF 🟢",
        )

        if not df.empty:
            # 🔧 BURASI DEĞİŞTİ: key'leri her seferinde benzersiz yapıyoruz
            fig_loc = px.bar(df, x='location', y='amount', color='fraud_reason', title="Şehirlere Göre Risk Analizi")
            chart_col1.plotly_chart(
                fig_loc,
                use_container_width=True,
                key=f"loc_chart_{time.time()}"
            )

            fig_pie = px.pie(df, names='fraud_reason', title="Tespit Edilen İhlal Türleri")
            chart_col2.plotly_chart(
                fig_pie,
                use_container_width=True,
                key=f"pie_chart_{time.time()}"
            )

            display_df = df[['timestamp', 'user_id', 'location', 'amount', 'fraud_reason']]
            table_placeholder.dataframe(display_df, use_container_width=True)

    else:
        st.error("API'ye bağlanılamadı! Lütfen 'api.py'nin çalıştığından emin olun.")
        
    time.sleep(2)
