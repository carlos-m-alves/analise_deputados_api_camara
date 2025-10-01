# Consulta Dados Abertos da Câmara dos Deputados

https://deputados.streamlit.app/

Este projeto consiste em uma aplicação web interativa criada com Streamlit que consulta, processa e apresenta dados públicos da Câmara dos Deputados do Brasil, utilizando a API oficial de Dados Abertos da Câmara dos Deputados (https://dadosabertos.camara.leg.br/swagger/api.html).

Através da aplicação, o usuário pode explorar informações atualizadas sobre deputados federais, suas atividades, proposições, comissões e outras informações legislativas diretamente na interface amigável da web, sem a necessidade de consultas complexas ou manipulação manual dos dados.

### Funcionalidades
- Consulta de informações detalhadas sobre deputados federais (nome, partido, estado, foto)
- Interface responsiva criada com Streamlit
- Atualização automática dos dados via API pública
- Filtragem e busca por nome
- Exibição de dados estruturados em tabelas

### Tecnologias e Bibliotecas Utilizadas
- Python
- Streamlit (para a interface web)
- Requests (para consumo da API REST da Câmara dos Deputados)
- Pandas (para manipulação e tratamento de dados)

### Como Rodar o Projeto Localmente

1. Clone este repositório:
```
git clone https://github.com/seuusuario/repositorio.git
cd repositorio
```
2. Crie e ative um ambiente virtual Python (recomendado):
```
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
Instale as dependências:
```
3. Instale as dependências:
```
pip install -r requirements.txt
```
4. Execute o app Streamlit:
```
streamlit run app.py
Acesse a aplicação no navegador pelo endereço:
```
5. Acesse a aplicação no navegador pelo endereço:
```
http://localhost:8501
```