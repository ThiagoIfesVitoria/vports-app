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

# Definir contato dos supervisores
contato = {
    "ENGENHARIA" : ["Ednaldo Lepaus Baldan", "@vports.com.br", "(27) 99895-****"],
    "PCM/MANUTENÇÃO":["Joao Antonio Oliveira", "jaoliveira@vports.com.br", "(27) 99895-****"],
    "FACILITIES":["Danylo Nunes Barbosa", "@vports.com.br", "(27) 99895-****"],
    "PLANEJAMENTO OP.":["Lucas Bozolan Mendes", "@vports.com.br", "(27) 99895-****"],
    "OPERAÇÃO":["Lucas Bozolan Mendes", "@vports.com.br", "(27) 99895-****"],
    "TI":["Tiago Boldrini de Azevedo", "@vports.com.br", "(27) 99895-****"]
}

df["Responsável"] = np.select(condicoes, valores,"NaN")

# Remover colunas matriz de responsabilidade
df = df.drop(columns = valores)

dicionario_resp = {}
for _, row in df.iterrows():
    chave = (row["DESCRIÇÃO"], row["DEMANDAS/NATUREZA"], row["ORIGEM"])
    dicionario_resp[chave] = row["Responsável"]

st.image("assets/Logo.png",width=100)
st.title("Definição de responsabilidade por atividade :blue[(Gestão de ativos)]")
# Extrair listas únicas
descricoes = sorted(set(chave[0] for chave in dicionario_resp))
descricao = st.selectbox("Escolha o ATIVO/EQUIPAMENTO", descricoes)

# Filtrar as próximas opções com base na anterior
demandas = sorted(set(k[1] for k in dicionario_resp if k[0] == descricao))
demanda = st.selectbox("Escolha a DEMANDA", demandas)

origens = sorted(set(k[2] for k in dicionario_resp if k[0] == descricao and k[1] == demanda))
origem = st.selectbox("Escolha a ORIGEM", origens)

# Exibir o responsável
chave = (descricao, demanda, origem)
responsavel = dicionario_resp.get(chave, "Não encontrado")
st.write("**O Responsável pela ação é:**", f":blue[{responsavel}]")

# Define o dialog como uma função decorada
@st.dialog("Detalhamento do responsável")
def mostrar_detalhes(resp):
    st.title(f"Setor Responsável: :blue[{resp}]")

    st.write("## 📞 Contato do Supervisor responsável")
    st.markdown(f"""
    - Supervisor responsável: {contato[resp][0]} 
    - E-mail: {contato[resp][1]}   
    """)

# Popover com botão que chama o dialog

if st.button(":blue[_mostrar detalhes_]", type="tertiary"):
    mostrar_detalhes(responsavel)

with st.popover("Relatório de Auditoria"):
    st.markdown("**Data do Acordo:** 31/07/****")
    st.markdown("**Supervisores Responsáveis:**")
    st.markdown("- *Lucas Bozolan Mendes* (Gerente de Operações) \n- *Joao Antonio Oliveira* (Supervisor do PCM)  \n- *Tiago Boldrini de Azevedo* (Supervisor de T.I)")
