import streamlit as st
import pandas as pd
import numpy as np

# try:
#     df = pd.read_excel(r"C:\Users\trsantos\OneDrive - Vports\PCM\02_Gestão_Ativos\02_Estrategia_Ativos\Gestão_Ativos - Limites_de_Baterias.xlsx", skiprows=4)
# except:
df = pd.read_excel("assets/limites_de_baterias.xlsx", skiprows=4)

# Defina as condições
condicoes = [
    df["ENGENHARIA"].notna(),
    df["PCM/MANUTENÇÃO"].notna(),
    df["FACILITIES"].notna(),
    df["PLANEJAMENTO OP."].notna(),
    df["OPERAÇÃO"].notna(),
    df["TI"].notna()
]

# Defina os valores correspondentes às condições
valores = ["ENGENHARIA", "PCM/MANUTENÇÃO", "FACILITIES", "PLANEJAMENTO OP.", "OPERAÇÃO", "TI"]

df["Responsável"] = np.select(condicoes, valores,"NaN")

# Remover colunas matriz de responsabilidade
df = df.drop(columns = valores)

dicionario_resp = {}
for _, row in df.iterrows():
    chave = (row["DESCRIÇÃO"], row["DEMANDAS/NATUREZA"], row["ORIGEM"])
    dicionario_resp[chave] = row["Responsável"]

st.image("assets/Logo.png",width=100)
st.title("Definição do Responsável em :blue[_ações de segurança_]")
# Extrair listas únicas
descricoes = sorted(set(chave[0] for chave in dicionario_resp))
descricao = st.selectbox("Escolha a DESCRIÇÃO", descricoes)

# Filtrar as próximas opções com base na anterior
demandas = sorted(set(k[1] for k in dicionario_resp if k[0] == descricao))
demanda = st.selectbox("Escolha a DEMANDA", demandas)

origens = sorted(set(k[2] for k in dicionario_resp if k[0] == descricao and k[1] == demanda))
origem = st.selectbox("Escolha a ORIGEM", origens)

# Exibir o responsável
chave = (descricao, demanda, origem)
responsavel = dicionario_resp.get(chave, "Não encontrado")
st.write("**Responsável:**", responsavel)

with st.popover("Relatório de Auditoria"):
    st.markdown("**Data do Acordo:** 31/07/2003")
    st.markdown("**Supervisores Responsáveis:**")
    st.markdown("- *João Oliveira* (Supervisor do PCM)  \n- *Lucas Teste* (Supervisor de Operações)  \n- *Thiago Nespoli* (Supervisor de T.I)")
