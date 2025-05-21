import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuração da página
st.set_page_config(page_title="Formulário de Indicações", layout="wide", page_icon="imagens/vivo4.png")

# Carregando os dados
@st.cache_data
def carregar_dados():
    df = pd.read_excel("basededados.xlsx", sheet_name="Sheet1", engine="openpyxl")
    df.columns = df.columns.str.strip()  # Remove espaços invisíveis
    return df

df = carregar_dados()

# --- BARRA LATERAL ---
st.sidebar.title("Navegação")
pagina = st.sidebar.radio("Ir para:", ["Página Inicial", "Tabela", "Gráficos", "Fomulário"])

# --- PÁGINA INICIAL ---
if pagina == "Página Inicial":
    st.title("Bem-vindo ao Dashboard de Sugestões")
    st.write("Use o menu lateral para navegar entre as páginas.")
    st.image("imagens/data_analitycs.jpg")

# --- TABELA COM FILTROS ---
elif pagina == "Tabela":
    st.title("Tabela de Dados")

    categorias = df['Qual categoria deseja cadrastar'].unique()
    categoria_selecionada = st.selectbox("Filtrar por Categoria (opcional):", ["Todos"] + list(categorias))

    generos = df['Qual o gênero da sua solicitação'].unique()
    genero_selecionado = st.multiselect("Filtrar por Gênero (opcional):", generos)

    df_filtrado = df.copy()
    if categoria_selecionada != "Todos":
        df_filtrado = df_filtrado[df_filtrado['Qual categoria deseja cadrastar'] == categoria_selecionada]
    if genero_selecionado:
        df_filtrado = df_filtrado[df_filtrado['Qual o gênero da sua solicitação'].isin(genero_selecionado)]

    st.metric(label="Total de Registros Exibidos", value=len(df_filtrado))

    

    # Tabela com rolagem horizontal e largura total
    
    colunas_desejadas = {
        'Nome': 'Nome do Usuário',
        'Qual categoria deseja cadrastar': 'Categoria',
        'Qual o gênero da sua solicitação': 'Gênero',
        'Qual indicação você deseja fazer?': 'Indicação',
    }
    
    df_exibicao = df_filtrado[list(colunas_desejadas.keys()) + ['Insira o Link da sua indicação']].rename(columns=colunas_desejadas)
    
    df_exibicao['Link'] = df_filtrado['Insira o Link da sua indicação'].apply(
        lambda x: f'<a href="{x}" target="_blank">Acessar</a>' if pd.notnull(x) else ''
    )
    
    colunas_final = list(colunas_desejadas.values()) + ['Link']


    st.markdown(
        f"""
        <div style="overflow-x: auto; width: 100%;">
            {df_exibicao[colunas_final].to_html(escape=False, index=False)}
        </div>
        """,
        unsafe_allow_html=True
    )

# --- GRÁFICOS INTERATIVOS ---
elif pagina == "Gráficos":
    custom_template = {
        "layout": go.Layout(
            plot_bgcolor='black',
            paper_bgcolor='black',
            font=dict(color='white')
        )
    }

    st.title("Visualizações Gráficas")
    categorias = df['Qual categoria deseja cadrastar'].unique()
    categoria_selecionada = st.selectbox("Filtrar por Categoria (opcional):", ["Todos"] + list(categorias))

    generos = df['Qual o gênero da sua solicitação'].unique()
    genero_selecionado = st.multiselect("Filtrar por Gênero (opcional):", generos)

    df_filtrado = df.copy()
    if categoria_selecionada != "Todos":
        df_filtrado = df_filtrado[df_filtrado['Qual categoria deseja cadrastar'] == categoria_selecionada]
    if genero_selecionado:
        df_filtrado = df_filtrado[df_filtrado['Qual o gênero da sua solicitação'].isin(genero_selecionado)]

    col1, col2 = st.columns(2)

    with col1:
        st.write("Categorias")
        total_id = df_filtrado['Qual categoria deseja cadrastar'].value_counts()
        fig1 = px.bar(
            total_id,
            x=total_id.index,
            y=total_id.values,
            text=total_id.values,
            color_discrete_sequence=["#660099"]
        )
        fig1.update_layout(title="Total por Categoria", template=custom_template)
        fig1.update_traces(textposition='outside')
        st.plotly_chart(fig1)

        st.write("Usuários")
        total_usuario = df_filtrado['Nome'].value_counts()
        fig4 = px.bar(
            total_usuario,
            x=total_usuario.index,
            y=total_usuario.values,
            text=total_usuario.values,
            color_discrete_sequence=["#660099"]
        )
        fig4.update_layout(title="Total por Usuários", template=custom_template)
        fig4.update_traces(textposition='outside')
        st.plotly_chart(fig4)

    with col2:
        st.write("Gênero")
        total_genero = df_filtrado['Qual o gênero da sua solicitação'].value_counts()
        fig2 = px.pie(
            total_genero,
            values=total_genero.values,
            names=total_genero.index,
            hole=0.3,
            color_discrete_sequence=["#660099","#bd4aff","#eb3c7d","#380054","#940099","#C10099","#FF5C7D"]
        )
        fig2.update_layout(title="Distribuição por Gênero", template=custom_template)
        fig2.update_traces(textposition='inside', textinfo='percent+value')
        st.plotly_chart(fig2)

        st.write("Indicações")
        total_titulo = df_filtrado['Qual indicação você deseja fazer?'].value_counts()
        fig3 = px.bar(
            total_titulo,
            x=total_titulo.values,
            y=total_titulo.index,
            text=total_titulo.values,
            orientation='h',
            color_discrete_sequence=["#660099"]
        )
        fig3.update_layout(title="Total de Indicações", template=custom_template)
        fig3.update_traces(textposition='outside')
        st.plotly_chart(fig3)

# --- FORMULÁRIO ---
elif pagina == "Fomulário":
    st.title("Formulário")
    st.write("Para acesso do formulário acesse o link abaixo")
    st.markdown(
        '<a href="https://forms.office.com/Pages/DesignPageV2.aspx?subpage=design&token=e46031f2904444a89e08626ca679ff02&id=DmBElwQ-Lkm6oSXsJFxvENB7dqkvt85AnOAGY2k4IE9UMEFBRktYME0zSjJTQVlLTDhDQUc3QTVUMC4u&topview=Preview" target="_blank">Clique aqui para acessar o formulário</a>',
        unsafe_allow_html=True
    )
