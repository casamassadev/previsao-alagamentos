import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

# 1. Ler os dados
df = pd.read_csv('dados_chuva.csv')

# 2. Verificar as colunas do DataFrame
print("Colunas do DataFrame:", df.columns.tolist())

# 3. Preparar os dados
X = df[['Precipitação (mm)']]  # variável preditora
y = df['Alagamento']         # variável alvo (0 ou 1)

# 4. Dividir em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. Criar e treinar o modelo
modelo = RandomForestClassifier(n_estimators=100, random_state=42)
modelo.fit(X_train, y_train)

# 6. Avaliar o modelo
y_pred = modelo.predict(X_test)
print(classification_report(y_test, y_pred))

# 7. Salvar o modelo treinado
joblib.dump(modelo, 'modelo_alagamento.pkl')
print("✅ Modelo salvo como 'modelo_alagamento.pkl'")

df = pd.read_csv('dados_chuva.csv')
print("Colunas do DataFrame:", df.columns.tolist())  # 👈 linha de teste