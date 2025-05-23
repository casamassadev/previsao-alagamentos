import pandas as pd
import joblib

import requests

url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": -22.9697,
    "longitude": -46.9979,
    "hourly": "temperature_2m,precipitation",
    "timezone": "America/Sao_Paulo"
}

response = requests.get(url, params=params)
data = response.json()

# Exemplo: mostrar as próximas 5 horas com temperatura e chuva
for i in range(20):
    time = data['hourly']['time'][i]
    temp = data['hourly']['temperature_2m'][i]
    rain = data['hourly']['precipitation'][i]
    print(f"{time} - Temp: {temp}°C - Chuva: {rain} mm")

    # Exemplo: se a chuva acumulada nas próximas 6 horas for maior que 30 mm, tem risco de enchente
def tem_enchente(previsao_chuva):
    acumulado = sum(previsao_chuva[:6])  # soma chuva nas próximas 6 horas
    limite = 30  # mm de chuva
    return acumulado > limite
import requests

def pegar_previsao():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": -22.9697,
        "longitude": -46.9979,
        "hourly": "precipitation",
        "timezone": "America/Sao_Paulo"
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data['hourly']['precipitation']

def tem_enchente(previsao_chuva, limite=30):
    acumulado = sum(previsao_chuva[:6])  # soma das próximas 6 horas
    if acumulado > limite:
        return True
    else:
        return False

chuva_prevista = pegar_previsao()

if tem_enchente(chuva_prevista):
    print("⚠️ Alerta: risco de enchente nas próximas horas!")
else:
    print("Sem risco de enchente previsto.")