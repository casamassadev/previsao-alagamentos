import csv

caminho_arquivo = r"C:\Users\Marcio Casamassa\Downloads\dados_chuva_cepagri.csv"

with open(caminho_arquivo, mode="r", encoding="utf-8") as arquivo:
    leitor = csv.DictReader(arquivo)
    for linha in leitor:
        print(linha)
