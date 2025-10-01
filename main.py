from datetime import datetime, date
import streamlit as st
import pandas as pd
import requests

#colocar no arquivo python-dateutil

st.set_page_config(layout="wide", page_title="Análise Exploratória")
st.title("Análise das Despesas dos Deputados do Brasil")

@st.cache_resource
def load_data(type, id):
    url = 'https://dadosabertos.camara.leg.br/api/v2/deputados/'
    if type == 'deputados' and id is None:
        url = "https://dadosabertos.camara.leg.br/api/v2/deputados/"
    elif type == 'info_deputado' and id is not None:
        url = f"https://dadosabertos.camara.leg.br/api/v2/deputados/{id}"
    elif type == 'despesas' and id is not None:
        url = f"https://dadosabertos.camara.leg.br/api/v2/deputados/{id}/despesas"    

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error: {response.status_code} - {response.text}")

def calcula_idade(data_nascimento_deputado):
    # Converte string para objeto date
    data_nascimento = datetime.strptime(data_nascimento_deputado, "%Y-%m-%d").date()
    # Data atual
    hoje = date.today()
    # Calcula idade ajustando se o aniversário já ocorreu neste ano
    idade = hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))
    return idade


dados = load_data('deputados', 0)
df = pd.DataFrame(dados['dados'])

st.session_state['dados'] = dados

nomes = df['nome'].tolist()


# Criar o dropdown (selectbox) usando a coluna
deputado_selecionado = st.selectbox('Selecione uma opção:', nomes)

# Filtrar e pegar o id da pessoa selecionada
id_deputado_selecionado = str(df[df['nome'] == deputado_selecionado]['id'].iloc[0])
    

col1, col2 = st.columns([1, 2])  # Coluna 1 com largura menor que a 2

with col1:
    #info_deputado = load_info_deputado(id_deputado_selecionado)
    info_deputado = load_data('info_deputado',id_deputado_selecionado)
    url_imagem = info_deputado['dados']['ultimoStatus']['urlFoto']
    st.image(url_imagem, caption="Foto do deputado", width=150)


with col2:
    st.write('ID:', id_deputado_selecionado)
    st.write('Partido:', df['siglaPartido'].iloc[0])
    st.write('UF:', df['siglaUf'].iloc[0])

    idade = calcula_idade(info_deputado['dados']['dataNascimento'])
    st.write('Idade:', idade)

despesas = load_data('despesas', id_deputado_selecionado)

despesas = pd.DataFrame(despesas['dados'])

if not despesas.empty:

    # Seleciona apenas as colunas desejadas
    colunas_desejadas = ["dataDocumento", "valorDocumento", "tipoDespesa", "nomeFornecedor"]
    df_filtrado = despesas[colunas_desejadas]

    # Converte a coluna 'Data' para datetime para garantir ordenação correta
    df_filtrado['dataDocumento'] = pd.to_datetime(df_filtrado['dataDocumento'])

    # Formata a coluna 'Data' para o formato dd/mm/yy
    df_filtrado['dataDocumento'] = df_filtrado['dataDocumento'].dt.strftime('%d/%m/%y')

    # Calcula soma das colunas numéricas
    total_gasto = df_filtrado['valorDocumento'].sum()
    total_formatado = f"R$ {total_gasto:,.2f}".replace(',', 'v').replace('.', ',').replace('v', '.')

    # Formata a coluna Preço como dinheiro (R$ xx,xx)
    df_filtrado['valorDocumento'] = df_filtrado['valorDocumento'].apply(lambda x: f'R$ {x:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.'))

    # Ordena o DataFrame pela coluna 'Data'
    df_ordenado = df_filtrado.sort_values(by='dataDocumento')

    # Renomear 4 colunas antigas para novos nomes
    df_ordenado = df_ordenado.rename(columns={
        "dataDocumento": "Data",
        "valorDocumento": "Valor",
        "tipoDespesa": "Tipo de Despesa",
        "nomeFornecedor": "Nome do Fornecedor"
    })

    st.write('Total gasto:', total_formatado)

    st.table(df_ordenado)
else:
    st.write("Nenhuma despesa encontrada para este deputado.")