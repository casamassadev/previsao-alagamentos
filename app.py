import streamlit as st
import requests
from datetime import datetime

# Dicionário para meses em português
meses_pt = {
    "January": "janeiro", "February": "fevereiro", "March": "março", "April": "abril",
    "May": "maio", "June": "junho", "July": "julho", "August": "agosto",
    "September": "setembro", "October": "outubro", "November": "novembro", "December": "dezembro"
}

def emoji_tempo(code):
    if code == 0:
        return "☀️"
    elif code in [1, 2, 3]:
        return "🌤️"
    elif code in [45, 48]:
        return "🌫️"
    elif code in range(51, 68):
        return "🌦️"
    elif code in [80, 81, 82, 95, 96, 99]:
        return "⛈️"
    else:
        return "🌧️"

def pegar_previsao():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": -22.9697,
        "longitude": -46.9979,
        "daily": "precipitation_sum,temperature_2m_max,weathercode",
        "timezone": "America/Sao_Paulo"
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data["daily"]

def avaliar_risco(chuva_mm, limite=30):
    return "🚨 Risco de alagamento" if chuva_mm > limite else "✅ Sem risco"

st.set_page_config(layout="wide")
st.title("🌧️ Previsão do Tempo + Alagamento na Av Invernada – Valinhos/SP")

dados = pegar_previsao()

datas = dados["time"][:6]
chuvas = dados["precipitation_sum"][:6]
temperaturas = dados["temperature_2m_max"][:6]
climas = dados["weathercode"][:6]

col1, col2 = st.columns(2)

with col1:
    # Formata a data de hoje para mostrar no título
    data_hoje_obj = datetime.strptime(datas[0], "%Y-%m-%d")
    data_hoje_formatada = data_hoje_obj.strftime("%d de %B de %Y")
    for en, pt in meses_pt.items():
        data_hoje_formatada = data_hoje_formatada.replace(en, pt)
    
    st.subheader(f"📅 Hoje – {data_hoje_formatada}")
    st.markdown(f"**🌡️ Temperatura máxima:** {temperaturas[0]} °C")
    st.markdown(f"**🌧️ Precipitação prevista:** {chuvas[0]} mm")
    st.markdown(f"**Clima:** {emoji_tempo(climas[0])}")

with col2:
    st.subheader("📆 Próximos 5 dias")
    for i in range(1, 6):
        data_obj = datetime.strptime(datas[i], "%Y-%m-%d")
        data_formatada = data_obj.strftime("%d/%m/%Y")
        st.markdown(f"**{data_formatada}**")
        st.markdown(f"{emoji_tempo(climas[i])}  {temperaturas[i]}°C, {chuvas[i]} mm")
        st.markdown("---")

st.subheader("🌊 Avaliação de risco de alagamento")
for i in range(6):
    data_obj = datetime.strptime(datas[i], "%Y-%m-%d")
    data_formatada = data_obj.strftime("%d de %B de %Y")
    for en, pt in meses_pt.items():
        data_formatada = data_formatada.replace(en, pt)
    risco = avaliar_risco(chuvas[i])
    st.write(f"📅 {data_formatada} → {chuvas[i]} mm → {risco}")
