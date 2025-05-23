import streamlit as st
import requests
import matplotlib.pyplot as plt
from datetime import datetime

# Função para converter código do tempo em emoji
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

# Pegar dados da API Open-Meteo
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

# Avaliar risco de alagamento
def avaliar_risco(chuva_mm, limite=30):
    return "🚨 Risco de alagamento" if chuva_mm > limite else "✅ Sem risco"

# Layout do Streamlit
st.set_page_config(layout="wide")
st.title("🌧️ Previsão do Tempo + Alagamentos – Valinhos/SP")

dados = pegar_previsao()

datas = dados["time"][:6]
chuvas = dados["precipitation_sum"][:6]
temperaturas = dados["temperature_2m_max"][:6]
climas = dados["weathercode"][:6]

col1, col2 = st.columns(2)

# ESQUERDA: PREVISÃO DE HOJE
with col1:
    st.subheader(f"📅 Hoje – {datas[0]}")
    st.markdown(f"**🌡️ Temperatura máxima:** {temperaturas[0]} °C")
    st.markdown(f"**🌧️ Precipitação prevista:** {chuvas[0]} mm")
    st.markdown(f"**Clima:** {emoji_tempo(climas[0])}")

# DIREITA: PRÓXIMOS 5 DIAS
with col2:
    st.subheader("📆 Próximos 5 dias")
    for i in range(1, 6):
        st.markdown(f"**{datas[i]}**")
        st.markdown(f"{emoji_tempo(climas[i])}  {temperaturas[i]}°C, {chuvas[i]} mm")
        st.markdown("---")

# ABAIXO: RISCOS DE ALAGAMENTO
st.subheader("🌊 Avaliação de risco de alagamento")
for i in range(6):
    data_formatada = datetime.strptime(datas[i], "%Y-%m-%d").strftime("%d/%m/%Y")
    risco = avaliar_risco(chuvas[i])
    st.write(f"📅 {data_formatada} → {chuvas[i]} mm → {risco}")
