import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# ----------- FUNÇÕES AUXILIARES -----------------------------------------

def pegaCombos(d):
  a = []
  for i in range(len(d)):
    if type(d[i]) == str:
      if ',' in d[i]:
        a.append(d[i])
  return a


def PlotarBarChart(a, nome):
    rc = {'figure.figsize':(10,8),
          'axes.facecolor':'white',
          'axes.edgecolor': 'white',
          'axes.labelcolor': 'black',
          'figure.facecolor': 'white',
          'patch.edgecolor': 'white',
          'text.color': 'black',
          'xtick.color': 'black',
          'ytick.color': 'black',
          'grid.color': 'grey',
          'font.size' : 12,
          'axes.labelsize': 12,
          'xtick.labelsize': 12,
          'ytick.labelsize': 12}
    
    plt.rcParams.update(rc)
    
    fig, axes = plt.subplots()
    fig.suptitle(nome)
    plt.xticks(rotation = 0)
    axes.axhline(0, color = 'black')
    sns.barplot(ax=axes, x=a.index, y= list(a), color = '#434141')
    
    for p in axes.patches:
        axes.annotate(format(str(int(p.get_height()))), 
        (p.get_x() + p.get_width() / 2., p.get_height()),
        ha = 'center',
        va = 'center', 
        xytext = (0, 15),
        textcoords = 'offset points')
    
    st.pyplot(fig)
    
def Ordena(a):
    l = a.index.sort_values()
    b = [0]*len(a.index)
    for i in range(len(a.index)):
        for j in range(len(a.index)):
            if l[i] == a.index[j]:
                b[i] = list(a)[j]
    
    return(b)

# ---------- DASHBOARD STREAMLIT ----------------------------------------

st.set_page_config(page_title=("Hidros Consultoria"), layout = 'wide')

st.sidebar.title('Hidros Consultoria')

st.sidebar.subheader('Insira a base de dados aqui no formato .xlsx')

file = st.sidebar.file_uploader('Base de Dados', 'xlsx')

if file is not None:

    df = pd.read_excel(file)


pagina = st.sidebar.selectbox('Selecione a página', ['Página Inicial','Comercial','Marketing','Coordenação'])


# ---------- INICIO DA PAGINA INICIAL ----------------------------------------

if pagina == 'Página Inicial':
    
    st.title("Análise dos Dados da Hidros Consultoria")
    
    st.subheader("1. Informações Iniciais")
    
    st.text("Este aplicativo web foi desenvolvido por Mariana de Oliveira Tito e faz parte do Projeto de Graduação em Engenharia Elétrica da autora")
    st.text("As informaçõs presentes nesta visualização foram cedidas pela Hidros Consultoria - Empresa Júnior de Engenharia da UERJ")
    
    
    st.subheader("2. Dados Utilizados")
    st.text("Os dados utilizados foram extraídos do Pipefy da Hidros Consultoria em setembro de 2022")
    
    


# ---------- LEITURA DA BASE DE DADOS ------------------------------------------

#df = pd.read_excel('base_Hidros.xlsx')


# ---------- AJUSTE NO ATRIBUTO SERVIÇOS ------------------------------------------

pc = df['Serviços PC'].unique()
pamb = df['Serviços PAmb'].unique()
pe = df['Serviços PE'].unique()
pm = df['Serviços PM'].unique()
pp = df['Serviços PP'].unique()

comboPC = pegaCombos(pc)
comboPAmb = pegaCombos(pamb)
comboPE = pegaCombos(pe)
comboPM = pegaCombos(pm)
comboPP = pegaCombos(pp)

baseAjustada = df

baseAjustada.loc[baseAjustada['Serviços PAmb'].isin(comboPAmb), 'Serviços PAmb'] = 'Combo'
baseAjustada.loc[baseAjustada['Serviços PC'].isin(comboPC), 'Serviços PC'] = 'Combo'
baseAjustada.loc[baseAjustada['Serviços PE'].isin(comboPE), 'Serviços PE'] = 'Combo'
baseAjustada.loc[baseAjustada['Serviços PM'].isin(comboPM), 'Serviços PM'] = 'Combo'
baseAjustada.loc[baseAjustada['Serviços PP'].isin(comboPP), 'Serviços PP'] = 'Combo'

# ---------- AJUSTE NO ATRIBUTO ENGENHARIA ------------------------------------------

baseAjustada.loc[baseAjustada['Serviços PM'].notnull() & baseAjustada['Engenharia:'].isnull(), 'Engenharia:'] = 'Mecânica'
baseAjustada.loc[baseAjustada['Serviços PP'].notnull() & baseAjustada['Engenharia:'].isnull(), 'Engenharia:'] = 'Produção'
baseAjustada.loc[baseAjustada['Serviços PE'].notnull() & baseAjustada['Engenharia:'].isnull(), 'Engenharia:'] = 'Elétrica'
baseAjustada.loc[baseAjustada['Serviços PAmb'].notnull() & baseAjustada['Engenharia:'].isnull(), 'Engenharia:'] = 'Ambiental'
baseAjustada.loc[baseAjustada['Serviços PC'].notnull() & baseAjustada['Engenharia:'].isnull(), 'Engenharia:'] = 'Civil/Cartográfica'

baseAjustada.drop(baseAjustada[baseAjustada['Engenharia:'].isnull()].index, inplace=True)

engenharia = df['Engenharia:'].unique()
comboEng = pegaCombos(engenharia)

baseAjustada.loc[baseAjustada['Engenharia:'].isin(comboEng), 'Engenharia:'] = 'Especial'

# ---------- AJUSTE NO ATRIBUTO FORMA DE CHEGADA E PROSPECÇÃO ------------------------------------------

baseAjustada.loc[(baseAjustada['Forma de Chegada'].isnull()) & (baseAjustada['Created at'].dt.year == 2019), 'Forma de Chegada'] = 'Site'
baseAjustada.loc[(baseAjustada['Prospecção'].isnull()) & (baseAjustada['Created at'].dt.year == 2019), 'Prospecção'] = 'Landing Page'

baseAjustada.loc[(baseAjustada['Forma de Chegada'].isnull()), 'Forma de Chegada'] = 'Site'
baseAjustada.loc[(baseAjustada['Prospecção'].isnull()) & (baseAjustada['Forma de Chegada'] == 'Site'), 'Prospecção'] = 'Landing Page'

baseAjustada.loc[(baseAjustada['Prospecção'].isnull()), 'Prospecção'] = 'Outro'

# ----------------------------- AJUSTES DE BASE ------------------------------------------

baseAjustada['Dia da assinatura do contrato'] = pd.to_datetime(baseAjustada['Dia da assinatura do contrato'])

baseProposta = baseAjustada.loc[(baseAjustada['Valor AP'].notnull())]

baseAssinado = baseAjustada.loc[(baseAjustada['Current phase'] == 'ASSINADO') & (baseAjustada['Dia da assinatura do contrato'].notnull())]


# ---------- INICIO DA PAGINA COMERCIAL ----------------------------------------

if pagina == 'Comercial':
    
    relatorio = st.sidebar.radio('Selecione o relatório', ['Propostas & Contratos','Faturamento', 'Motivo de Cancelamento'])

    if relatorio == 'Propostas & Contratos':
    
        st.title("Propostas & Contratos")
            
        col0, col1 = st.columns((5.0,5.0))
        
        with col0:
            
            st.subheader("Distribuição Anual")
            
            propostas_ano = (baseAjustada.loc[(baseAjustada['Valor AP'].notnull())]['Created at'].dt.year.value_counts())
            projetos_ano = (baseAjustada.loc[(baseAjustada['Valor'].notnull()) & (baseAjustada['Current phase'] == 'ASSINADO')]['Dia da assinatura do contrato'].dt.year.value_counts())
                
                
            labels = propostas_ano.index.sort_values()
                
            # ordenando as entradas do gráfico
            propostaOrdem = Ordena(propostas_ano)
            projetosOrdem = Ordena(projetos_ano)
                
                
            x = np.arange(len(labels))
            width = 0.2
                
            rc = {'figure.figsize':(10,4),
                  'axes.facecolor':'white',
                  'axes.edgecolor': 'white',
                  'axes.labelcolor': 'black',
                  'figure.facecolor': 'white',
                  'patch.edgecolor': 'white',
                  'text.color': 'black',
                  'xtick.color': 'black',
                  'ytick.color': 'black',
                  'grid.color': 'grey',
                  'font.size' : 12,
                  'axes.labelsize': 12,
                  'xtick.labelsize': 12,
                  'ytick.labelsize': 12}
                
            plt.rcParams.update(rc)
                
            fig, axes = plt.subplots()
                
            rects2 = axes.bar(x, propostaOrdem, width, label = 'Propostas', color = '#535152')
            rects3 = axes.bar(x+width, projetosOrdem, width, label = 'Contratos', color = '#134338')
                
            axes.set_xticks(x, labels)
            plt.xticks(rotation = 0)
            axes.get_yaxis().set_visible(False)
            axes.axhline(0, color = 'black')
                
            axes.legend()
            axes.bar_label(rects2, padding = 2)
            axes.bar_label(rects3, padding = 2)
            
            st.pyplot(fig)
        
        with col1:
        
            st.subheader("Distribuição Mensal")
            
            baseAjustada['MesCriado'] = baseAjustada['Created at'].dt.month_name()
            baseAjustada['AnoCriado'] = baseAjustada['Created at'].dt.strftime('%Y')
            baseAjustada['MesAnoCriado'] = baseAjustada['MesCriado'].map(str) + baseAjustada['AnoCriado'].map(str)
            
            baseAjustada.sort_values(by='Created at', inplace = True)
            
            propostaMes = baseAjustada['MesAnoCriado'].value_counts(sort=False)
            
            baseAssinado['MesAssinatura'] = baseAssinado['Dia da assinatura do contrato'].dt.month_name()
            baseAssinado['AnoAssinatura'] = baseAssinado['Dia da assinatura do contrato'].dt.strftime('%Y')
            baseAssinado['MesAnoAssinatura'] = baseAssinado['MesAssinatura'].map(str) + baseAssinado['AnoAssinatura'].map(str)
            
            baseAssinado.sort_values(by='Dia da assinatura do contrato', inplace = True)
            
            assinadoMes = baseAssinado['MesAnoAssinatura'].value_counts(sort=False)
        
            rc = {'figure.figsize':(10,4),
                  'axes.facecolor':'white',
                  'axes.edgecolor': 'white',
                  'axes.labelcolor': 'black',
                  'figure.facecolor': 'white',
                  'patch.edgecolor': 'white',
                  'text.color': 'black',
                  'xtick.color': 'black',
                  'ytick.color': 'black',
                  'grid.color': 'grey',
                  'font.size' : 12,
                  'axes.labelsize': 8,
                  'xtick.labelsize': 6,
                  'ytick.labelsize': 6}
            
            plt.rcParams.update(rc)
            
            fig, axes = plt.subplots()
            
            
            
            axes.plot(propostaMes.index, list(propostaMes), color = '#535152', label = 'Propostas')
            axes.plot(assinadoMes.index, list(assinadoMes), color = '#134338', label ='Contratos')
            axes.legend()
            
            plt.xticks(rotation = 90)
            axes.axhline(0, color = 'black')
            
            st.pyplot(fig)
        
        col2, col3 = st.columns((5.0,5.0))
        
        with col2:
        
            a = b = 0;
            
            for i in range(len(propostaOrdem)):
                a = a + propostaOrdem[i]
                b = b + projetosOrdem[i]
            
            txGlobal = b/a
            
            st.text(" ")
            st.markdown("**Informações relevantes sobre Taxa de Conversão**")
            
            st.markdown("A Taxa de Conversão de proposta para contratos, entre 2019 e 2022, foi de **%.1f**" %(txGlobal * 100) + "%")
            
            for i in range(len(propostaOrdem)):
                c = (projetosOrdem[i]/propostaOrdem[i])
                st.markdown("* Em " + str(labels[i]) + ", a taxa de conversão entre propostas e contratos foi de **%.1f**" %(c * 100) + "%")
        
        with col3:
            
            st.markdown("**Alguns insights importantes sobre Propostas e Contratos**")
            
            maximoProposta = max(propostaMes)
            maximoPropostaMes = propostaMes.loc[lambda x : x == maximoProposta]
            
            st.markdown("O máximo de proposta apresentas em um único mês foi " + str(maximoProposta) + ". Isto ocorreu em: ")
            for i in range(len(maximoPropostaMes)):
                st.markdown("* " + maximoPropostaMes.index[i] + "\n")
            
            maximoAssinado = max(assinadoMes)
            maximoAssinadoMes = assinadoMes.loc[lambda x : x == maximoAssinado]
            
            st.markdown("O máximo de contratos assinados em um único mês foi " + str(maximoAssinado) + ". Isto ocorreu em: ")
            for i in range(len(maximoAssinadoMes)):
                st.markdown("* " + maximoAssinadoMes.index[i] + "\n")
    
    if relatorio == 'Faturamento':
    
        st.title("Faturamento")
        

        fat_possivel = baseProposta.groupby(baseProposta['Created at'].dt.year)['Valor AP'].sum()
        fat_real = baseAssinado.groupby(baseAssinado['Dia da assinatura do contrato'].dt.year)['Valor'].sum()
            
    
        x = np.arange(len(fat_possivel.index))
        width = 0.3
            
        rc = {'figure.figsize':(10,2.5),
              'axes.facecolor':'white',
              'axes.edgecolor': 'white',
              'axes.labelcolor': 'black',
              'figure.facecolor': 'white',
              'patch.edgecolor': 'white',
              'text.color': 'black',
              'xtick.color': 'black',
              'ytick.color': 'black',
              'grid.color': 'grey',
              'font.size' : 8,
              'axes.labelsize': 8,
              'xtick.labelsize': 8,
              'ytick.labelsize': 8}
            
        plt.rcParams.update(rc)
            
        fig, axes = plt.subplots()
        t = axes.bar(x, list(fat_real), width, color = '#535152')
            
        axes.set_xticks(x, fat_possivel.index)
        plt.xticks(rotation = 0)
        axes.get_yaxis().set_visible(False)
        axes.axhline(0, color = 'black')
            
        axes.legend()
        axes.bar_label(axes.containers[0], padding = 5, labels=([f'R${x:,.2f}' for x in t.datavalues]))
        st.pyplot(fig)
        
        
        st.text(" ")
        st.text(" ")
        st.markdown("**Faturamento Real x Faturamento Possível**")
            
            
        for i in range(len(list(fat_possivel))):
            z = list(fat_possivel)[i]
            st.markdown("* Em " + str(fat_possivel.index[i]) + " as propostas somaram R$ " f"{z:,}" + ". Ou seja, o faturamento representou %.1f" %((list(fat_real)[i]/list(fat_possivel)[i])*100) + "%")
    
    if relatorio == 'Motivo de Cancelamento':
    
        st.title("Motivo de Cancelamento")
        
        rc = {'figure.figsize':(10,4),
              'axes.facecolor':'white',
              'axes.edgecolor': 'white',
              'axes.labelcolor': 'black',
              'figure.facecolor': 'white',
              'patch.edgecolor': 'white',
              'text.color': 'black',
              'xtick.color': 'black',
              'ytick.color': 'black',
              'grid.color': 'grey',
              'font.size' : 7,
              'axes.labelsize': 8,
              'xtick.labelsize': 8,
              'ytick.labelsize': 8}
                    
        plt.rcParams.update(rc)

        motivoCancel = baseAjustada['Motivo do Cancelamento'].value_counts()
        
        labels = motivoCancel.index
        data = list(motivoCancel)

        def func(pct, allvals):
            absolute = int(np.round(pct/100.*np.sum(allvals)))
            return "{:.0f}%".format(pct)

        fig1, ax1 = plt.subplots()

        ax1.pie(data, autopct=lambda pct: func(pct, data),
                shadow=True, startangle=90, textprops=dict(color="w"))

        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        ax1.legend(labels, loc="lower left")
        
        st.pyplot(fig1)

        


# ---------- INICIO DA PAGINA MARKETING ----------------------------------------

elif pagina == 'Marketing':
    
    relatorio = st.sidebar.radio('Selecione o relatório', ['Novas Oportunidades','Formas de Chegada', 'Prospecção', 'Rentabilidade'])
    
    if relatorio == 'Novas Oportunidades':
    
        st.title("Novas Oportunidades")
        
        col4, col5 = st.columns((5.0,5.0))
        
        with col4:
            
            st.subheader('Distribuição Anual')
            
            leads_ano = baseAjustada['Created at'].dt.year.value_counts()
            PlotarBarChart(leads_ano, nome = '')
        
        with col5:
            
            st.subheader('Distribuição por Engenharia')
            
            leads_eng = baseAjustada['Engenharia:'].value_counts()
            soma_leads = baseAjustada['Engenharia:'].value_counts().sum()
            PlotarBarChart(leads_eng, nome = '')


            maximoEng = leads_eng.loc[lambda x : x == max(leads_eng)]
            pctEng = maximoEng/soma_leads
            st.markdown(' **Insight:** A engenharia com mais leads foi ' + maximoEng.index[0] + '. Suas oportunidades representam **%.1f**' %(pctEng * 100) + '%')

    if relatorio == 'Formas de Chegada':
    
        st.title("Formas de Chegada")
        
        col6, col7 = st.columns((5.0,5.0))
        
        with col6:
            
            st.subheader('Acumulado')
            
            rc = {'figure.figsize':(8,5),
                  'axes.facecolor':'white',
                  'axes.edgecolor': 'white',
                  'axes.labelcolor': 'black',
                  'figure.facecolor': 'white',
                  'patch.edgecolor': 'white',
                  'text.color': 'black',
                  'xtick.color': 'black',
                  'ytick.color': 'black',
                  'grid.color': 'grey',
                  'font.size' : 8,
                  'axes.labelsize': 12,
                  'xtick.labelsize': 12,
                  'ytick.labelsize': 12}
                        
            plt.rcParams.update(rc)

            labels = (baseAjustada['Forma de Chegada'].value_counts()).index
            data = list(baseAjustada['Forma de Chegada'].value_counts())

            def func(pct, allvals):
                absolute = int(np.round(pct/100.*np.sum(allvals)))
                return "{:.0f}%".format(pct)

            fig1, ax1 = plt.subplots()

            ax1.pie(data, autopct=lambda pct: func(pct, data),
                    shadow=True, startangle=90, textprops=dict(color="w"))

            ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

            ax1.legend(labels, loc="lower left")
            
            st.pyplot(fig1)
        
        with col7:
            
            st.subheader('Distribuição por Ano')
            
            ano = st.selectbox('Escolha o ano', [2019, 2020, 2021, 2022])
            
            rc = {'figure.figsize':(4,2.5),
                  'axes.facecolor':'white',
                  'axes.edgecolor': 'white',
                  'axes.labelcolor': 'black',
                  'figure.facecolor': 'white',
                  'patch.edgecolor': 'white',
                  'text.color': 'black',
                  'xtick.color': 'black',
                  'ytick.color': 'black',
                  'grid.color': 'grey',
                  'font.size' : 4,
                  'axes.labelsize': 8,
                  'xtick.labelsize': 8,
                  'ytick.labelsize': 8}
                        
            plt.rcParams.update(rc)

            formaAno = baseAjustada.loc[(baseAjustada['Created at'].dt.year == ano)]['Forma de Chegada'].value_counts()
            
            labels = formaAno.index
            data = list(formaAno)

            def func(pct, allvals):
                absolute = int(np.round(pct/100.*np.sum(allvals)))
                return "{:.0f}%".format(pct)

            fig1, ax1 = plt.subplots()

            ax1.pie(data, autopct=lambda pct: func(pct, data),
                    shadow=True, startangle=90, textprops=dict(color="w"))

            ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

            ax1.legend(labels, loc="lower left")
            
            st.pyplot(fig1)
        
    if relatorio == 'Prospecção':
        
            st.title("Prospecção")
            
            col8, col9 = st.columns((5.0,5.0))
            
            with col8:
                
                st.subheader('Acumulado')
                
                prospec = baseAjustada['Prospecção'].value_counts()
                
                rc = {'figure.figsize':(10,5),
                      'axes.facecolor':'white',
                      'axes.edgecolor': 'white',
                      'axes.labelcolor': 'black',
                      'figure.facecolor': 'white',
                      'patch.edgecolor': 'white',
                      'text.color': 'black',
                      'xtick.color': 'black',
                      'ytick.color': 'black',
                      'grid.color': 'grey',
                      'font.size' : 12,
                      'axes.labelsize': 12,
                      'xtick.labelsize': 12,
                      'ytick.labelsize': 12}
                
                plt.rcParams.update(rc)
                
                fig, axes = plt.subplots()
                plt.xticks(rotation = 90)
                sns.barplot(ax=axes, x=prospec.index, y= list(prospec), color = '#434141')
                
                for p in axes.patches:
                    axes.annotate(format(str(int(p.get_height()))), 
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha = 'center',
                    va = 'center', 
                    xytext = (0, 15),
                    textcoords = 'offset points')
                
                st.pyplot(fig)
                
                
            
            with col9:
                
                st.subheader('Distribuição por Ano')
                
                ano = st.selectbox('Escolha o ano', [2019, 2020, 2021, 2022])
                
                prospec = baseAjustada.loc[(baseAjustada['Created at'].dt.year == ano)]['Prospecção'].value_counts()
                
                rc = {'figure.figsize':(10,5),
                      'axes.facecolor':'white',
                      'axes.edgecolor': 'white',
                      'axes.labelcolor': 'black',
                      'figure.facecolor': 'white',
                      'patch.edgecolor': 'white',
                      'text.color': 'black',
                      'xtick.color': 'black',
                      'ytick.color': 'black',
                      'grid.color': 'grey',
                      'font.size' : 10,
                      'axes.labelsize': 10,
                      'xtick.labelsize': 10,
                      'ytick.labelsize': 10}
                
                plt.rcParams.update(rc)
                
                fig, axes = plt.subplots()
                plt.xticks(rotation = 90)
                sns.barplot(ax=axes, x=prospec.index, y= list(prospec), color = '#434141')
                
                for p in axes.patches:
                    axes.annotate(format(str(int(p.get_height()))), 
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha = 'center',
                    va = 'center', 
                    xytext = (0, 15),
                    textcoords = 'offset points')
                
                st.pyplot(fig)
                
    if relatorio == 'Rentabilidade':
        
        st.title("Formas de Chegada & Faturamento")
        
        ano = st.selectbox('Escolha o ano', [2019, 2020, 2021, 2022])
        
        baseAno = baseAjustada.loc[(baseAjustada['Created at'].dt.year == ano)]
        
        anoFat = baseAno.groupby(baseAno['Forma de Chegada'])['Valor'].sum()
        
        st.subheader('Participação das Formas de Chegada no Faturamento')
        
        rc = {'figure.figsize':(10,3),
              'axes.facecolor':'white',
              'axes.edgecolor': 'white',
              'axes.labelcolor': 'black',
              'figure.facecolor': 'white',
              'patch.edgecolor': 'white',
              'text.color': 'black',
              'xtick.color': 'black',
              'ytick.color': 'black',
              'grid.color': 'grey',
              'font.size' : 4,
              'axes.labelsize': 8,
              'xtick.labelsize': 8,
              'ytick.labelsize': 8}
                    
        plt.rcParams.update(rc)
        
        labels = anoFat.index
        data = list(anoFat)

        def func(pct, allvals):
            absolute = int(np.round(pct/100.*np.sum(allvals)))
            return "{:.0f}%".format(pct)

        fig1, ax1 = plt.subplots()

        ax1.pie(data, autopct=lambda pct: func(pct, data),
                shadow=True, startangle=90, textprops=dict(color="w"))

        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        ax1.legend(labels, loc="lower left")
        
        st.pyplot(fig1)
        
        
                
# ---------- INICIO DA PAGINA COORDENAÇÃO ---------------------------------

elif pagina == "Coordenação":
    
    relatorio = st.sidebar.radio('Selecione o relatório', ['Novas Oportunidades','Faturamento', 'Sucesso por Forma de Chegada'])
    
    st.title("Relatório das Coordenações")
    
    eng = st.selectbox('Escolha a Coordenação que deseja ver', ['Civil/Cartográfica', 'Ambiental', 'Elétrica', 'Mecânica', 'Produção'])
    
    if relatorio == 'Novas Oportunidades':
        
        st.subheader("Oportunidades & Propostas | Coordenação de " + eng)
        
        chegadas_ano = (baseAjustada.loc[(baseAjustada['Engenharia:'] == eng)]['Created at'].dt.year.value_counts())
        propostas_ano = (baseAjustada.loc[(baseAjustada['Valor AP'].notnull()) & (baseAjustada['Engenharia:'] == eng) ]['Created at'].dt.year.value_counts())
        projetos_ano = (baseAjustada.loc[(baseAjustada['Valor'].notnull()) & (baseAjustada['Current phase'] == 'ASSINADO') & (baseAjustada['Engenharia:'] == eng)]['Dia da assinatura do contrato'].dt.year.value_counts())
            
        labels = propostas_ano.index.sort_values()
            
        # ordenando as entradas do gráfico
        chegadaOrdem = Ordena(chegadas_ano)
        propostaOrdem = Ordena(propostas_ano)
        projetosOrdem = Ordena(projetos_ano)
            
            
        x = np.arange(len(labels))
        width = 0.2
            
        rc = {'figure.figsize':(10,3),
              'axes.facecolor':'white',
              'axes.edgecolor': 'white',
              'axes.labelcolor': 'black',
              'figure.facecolor': 'white',
              'patch.edgecolor': 'white',
              'text.color': 'black',
              'xtick.color': 'black',
              'ytick.color': 'black',
              'grid.color': 'grey',
              'font.size' : 12,
              'axes.labelsize': 12,
              'xtick.labelsize': 12,
              'ytick.labelsize': 12}
            
        plt.rcParams.update(rc)
            
        fig, axes = plt.subplots()
        
        
        rects1 = axes.bar(x-width, chegadaOrdem, width, label = 'Chegada', color = '#434141')
        rects2 = axes.bar(x, propostaOrdem, width, label = 'Propostas', color = '#535152')
        #rects3 = axes.bar(x+width, projetosOrdem, width, label = 'Contratos', color = '#134338')
            
        axes.set_xticks(x, labels)
        plt.xticks(rotation = 0)
        axes.get_yaxis().set_visible(False)
        axes.axhline(0, color = 'black')
            
        axes.legend()
        axes.bar_label(rects1, padding = 2)
        axes.bar_label(rects2, padding = 2)
        #axes.bar_label(rects3, padding = 2)
        
        st.pyplot(fig)
        

    
    if relatorio == 'Faturamento':
    
        baseEng = baseAjustada.loc[(baseAjustada['Engenharia:'] == eng)]

    
        col10, col11 = st.columns((5.0,5.0))
    
        with col10:
            
            contratos_eng = baseEng.groupby(baseAssinado['Dia da assinatura do contrato'].dt.year)['Valor'].count()
            
            st.subheader("Contratos por Ano")
    
            x = np.arange(len(contratos_eng.index))
            width = 0.3
            
            rc = {'figure.figsize':(10,5),
                  'axes.facecolor':'white',
                  'axes.edgecolor': 'white',
                  'axes.labelcolor': 'black',
                  'figure.facecolor': 'white',
                  'patch.edgecolor': 'white',
                  'text.color': 'black',
                  'xtick.color': 'black',
                  'ytick.color': 'black',
                  'grid.color': 'grey',
                  'font.size' : 12,
                  'axes.labelsize': 12,
                  'xtick.labelsize': 12,
                  'ytick.labelsize': 12}
            
            plt.rcParams.update(rc)
            
            fig, axes = plt.subplots()
            t = axes.bar(x, list(contratos_eng), width, color = '#535152')
            
            axes.set_xticks(x, contratos_eng.index)
            plt.xticks(rotation = 0)
            axes.get_yaxis().set_visible(False)
            axes.axhline(0, color = 'black')
            
            axes.legend()
            axes.bar_label(axes.containers[0], padding = 5, labels=([f'{x:,.0f}' for x in t.datavalues]))
            st.pyplot(fig)
        
        with col11:
        
            st.subheader("Faturamento Anual")
            
            fat_eng = baseEng.groupby(baseAssinado['Dia da assinatura do contrato'].dt.year)['Valor'].sum()
    
            x = np.arange(len(fat_eng.index))
            width = 0.3
            
            rc = {'figure.figsize':(10,5),
                  'axes.facecolor':'white',
                  'axes.edgecolor': 'white',
                  'axes.labelcolor': 'black',
                  'figure.facecolor': 'white',
                  'patch.edgecolor': 'white',
                  'text.color': 'black',
                  'xtick.color': 'black',
                  'ytick.color': 'black',
                  'grid.color': 'grey',
                  'font.size' : 12,
                  'axes.labelsize': 12,
                  'xtick.labelsize': 12,
                  'ytick.labelsize': 12}
            
            plt.rcParams.update(rc)
            
            fig, axes = plt.subplots()
            t = axes.bar(x, list(fat_eng), width, color = '#535152')
            
            axes.set_xticks(x, fat_eng.index)
            plt.xticks(rotation = 0)
            axes.get_yaxis().set_visible(False)
            axes.axhline(0, color = 'black')
            
            axes.legend()
            axes.bar_label(axes.containers[0], padding = 5, labels=([f'R${x:,.2f}' for x in t.datavalues]))
            st.pyplot(fig)
        
    
        
        
    if relatorio == 'Sucesso por Forma de Chegada':
    
        st.title('Chegada & Contratos por Serviço')
        
        col12, col13 = st.columns((5.0,5.0))
        
        with col12:
        
            ano2 = st.selectbox('Escolha o ano de análise dos serviços', [2019, 2020, 2021, 2022])
        
        with col13:
            
            if eng == 'Civil/Cartográfica':
                
                lista = baseAjustada.loc[baseAjustada['Serviços PC'].notnull()]['Serviços PC'].unique()
            
            elif eng == 'Ambiental':
                lista = baseAjustada.loc[baseAjustada['Serviços PAmb'].notnull()]['Serviços PAmb'].unique()
            
            elif eng == 'Elétrica':
                lista = baseAjustada.loc[baseAjustada['Serviços PE'].notnull()]['Serviços PE'].unique()
            
            elif eng == 'Mecânica':
                lista = baseAjustada.loc[baseAjustada['Serviços PM'].notnull()]['Serviços PM'].unique()
            
            elif eng == 'Produção':
                lista = baseAjustada.loc[baseAjustada['Serviços PP'].notnull()]['Serviços PP'].unique()
            
            
            servico = st.selectbox('Escolha a Serviço que deseja ver', lista)
        
        col14, col15 = st.columns((5.0,5.0))
        
        with col14:
            
            if eng == 'Civil/Cartográfica':
                
                servicos = baseAjustada.loc[(baseAjustada['Created at'].dt.year == ano2)]['Serviços PC'].value_counts()
            
            elif eng == 'Ambiental':
                servicos = baseAjustada.loc[(baseAjustada['Created at'].dt.year == ano2)]['Serviços PAmb'].value_counts()
            
            elif eng == 'Elétrica':
                servicos = baseAjustada.loc[(baseAjustada['Created at'].dt.year == ano2)]['Serviços PE'].value_counts()
            
            elif eng == 'Mecânica':
                servicos = baseAjustada.loc[(baseAjustada['Created at'].dt.year == ano2)]['Serviços PM'].value_counts()
            
            elif eng == 'Produção':
                servicos = baseAjustada.loc[(baseAjustada['Created at'].dt.year == ano2)]['Serviços PP'].value_counts()
            
            rc = {'figure.figsize':(10,4),
                  'axes.facecolor':'white',
                  'axes.edgecolor': 'white',
                  'axes.labelcolor': 'black',
                  'figure.facecolor': 'white',
                  'patch.edgecolor': 'white',
                  'text.color': 'black',
                  'xtick.color': 'black',
                  'ytick.color': 'black',
                  'grid.color': 'grey',
                  'font.size' : 10,
                  'axes.labelsize': 10,
                  'xtick.labelsize': 10,
                  'ytick.labelsize': 10}
            
            plt.rcParams.update(rc)
            
            fig, axes = plt.subplots()
            fig.suptitle('Serviços que mais chegaram em ' + str(ano2))
            plt.xticks(rotation = 90)
            sns.barplot(ax=axes, x= servicos.index, y= list(servicos), color = '#434141')
            
            for p in axes.patches:
                axes.annotate(format(str(int(p.get_height()))), 
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha = 'center',
                va = 'center', 
                xytext = (0, 10),
                textcoords = 'offset points')
            
            st.pyplot(fig)
        
        with col15:
            
            if eng == 'Civil/Cartográfica':
                
                servicos2 = baseAssinado.loc[(baseAssinado['Created at'].dt.year == ano2)]['Serviços PC'].value_counts()
            
            elif eng == 'Ambiental':
                servicos2 = baseAssinado.loc[(baseAssinado['Created at'].dt.year == ano2)]['Serviços PAmb'].value_counts()
            
            elif eng == 'Elétrica':
                servicos2 = baseAssinado.loc[(baseAssinado['Created at'].dt.year == ano2)]['Serviços PE'].value_counts()
            
            elif eng == 'Mecânica':
                servicos2 = baseAssinado.loc[(baseAssinado['Created at'].dt.year == ano2)]['Serviços PM'].value_counts()
            
            elif eng == 'Produção':
                servicos2 = baseAssinado.loc[(baseAssinado['Created at'].dt.year == ano2)]['Serviços PP'].value_counts()
            
            rc = {'figure.figsize':(10,4),
                  'axes.facecolor':'white',
                  'axes.edgecolor': 'white',
                  'axes.labelcolor': 'black',
                  'figure.facecolor': 'white',
                  'patch.edgecolor': 'white',
                  'text.color': 'black',
                  'xtick.color': 'black',
                  'ytick.color': 'black',
                  'grid.color': 'grey',
                  'font.size' : 10,
                  'axes.labelsize': 10,
                  'xtick.labelsize': 10,
                  'ytick.labelsize': 10}
            
            plt.rcParams.update(rc)
            
            fig, axes = plt.subplots()
            fig.suptitle('Serviços que mais fecharam contrato em ' + str(ano2))
            plt.xticks(rotation = 90)
            try:
                sns.barplot(ax=axes, x= servicos2.index, y= list(servicos2), color = '#434141')
            except:
                st.text('')
            
            for p in axes.patches:
                axes.annotate(format(str(int(p.get_height()))), 
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha = 'center',
                va = 'center', 
                xytext = (0, 10),
                textcoords = 'offset points')
            
            st.pyplot(fig)
        
        st.markdown("------------------------------------------------------------------------------------")
        st.title('Análise sobre ' + servico + ' em ' + str(ano2))
         
        st.text(' ')
        st.text(' ')
        st.text(' ')
        
        col16, col17 = st.columns((5.0,5.0))
        
        with col16:
            
            if eng == 'Civil/Cartográfica':
                
                formaChegadaServico = baseAjustada.loc[(baseAjustada['Serviços PC'] == servico) & (baseAjustada['Created at'].dt.year == ano2)]['Forma de Chegada'].value_counts()
            
            elif eng == 'Ambiental':
                
                formaChegadaServico = baseAjustada.loc[(baseAjustada['Serviços PAmb'] == servico) & (baseAjustada['Created at'].dt.year == ano2)]['Forma de Chegada'].value_counts()
            
            elif eng == 'Elétrica':
                
                formaChegadaServico = baseAjustada.loc[(baseAjustada['Serviços PE'] == servico) & (baseAjustada['Created at'].dt.year == ano2)]['Forma de Chegada'].value_counts()
            
            elif eng == 'Mecânica':
                
                formaChegadaServico = baseAjustada.loc[(baseAjustada['Serviços PM'] == servico) & (baseAjustada['Created at'].dt.year == ano2)]['Forma de Chegada'].value_counts()
            
            elif eng == 'Produção':
                
                formaChegadaServico = baseAjustada.loc[(baseAjustada['Serviços PP'] == servico) & (baseAjustada['Created at'].dt.year == ano2)]['Forma de Chegada'].value_counts()
            
            rc = {'figure.figsize':(10,4),
                  'axes.facecolor':'white',
                  'axes.edgecolor': 'white',
                  'axes.labelcolor': 'black',
                  'figure.facecolor': 'white',
                  'patch.edgecolor': 'white',
                  'text.color': 'black',
                  'xtick.color': 'black',
                  'ytick.color': 'black',
                  'grid.color': 'grey',
                  'font.size' : 10,
                  'axes.labelsize': 10,
                  'xtick.labelsize': 10,
                  'ytick.labelsize': 10}
            
            plt.rcParams.update(rc)
            
            fig, axes = plt.subplots()
            fig.suptitle('Forma de Chegada de ' + servico)
            plt.xticks(rotation = 90)
            try:
                sns.barplot(ax=axes, x= formaChegadaServico.index, y= list(formaChegadaServico), color = '#434141')
            except:
                st.text('')
            
            for p in axes.patches:
                axes.annotate(format(str(int(p.get_height()))), 
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha = 'center',
                va = 'center', 
                xytext = (0, 10),
                textcoords = 'offset points')
            
            st.pyplot(fig)
        
        with col17:
            
            if eng == 'Civil/Cartográfica':
                
                formaChegadaServicoFechado = baseAjustada.loc[(baseAjustada['Serviços PC'] == servico) & (baseAjustada['Current phase'] == 'ASSINADO') & (baseAjustada['Created at'].dt.year == ano2)]['Forma de Chegada'].value_counts()
            
            elif eng == 'Ambiental':
                formaChegadaServicoFechado = baseAjustada.loc[(baseAjustada['Serviços PAmb'] == servico) & (baseAjustada['Current phase'] == 'ASSINADO') & (baseAjustada['Created at'].dt.year == ano2)]['Forma de Chegada'].value_counts()
            
            elif eng == 'Elétrica':
                formaChegadaServicoFechado = baseAjustada.loc[(baseAjustada['Serviços PE'] == servico) & (baseAjustada['Current phase'] == 'ASSINADO') & (baseAjustada['Created at'].dt.year == ano2)]['Forma de Chegada'].value_counts()
            
            elif eng == 'Mecânica':
                formaChegadaServicoFechado = baseAjustada.loc[(baseAjustada['Serviços PM'] == servico) & (baseAjustada['Current phase'] == 'ASSINADO') & (baseAjustada['Created at'].dt.year == ano2)]['Forma de Chegada'].value_counts()
                
            elif eng == 'Produção':
                formaChegadaServicoFechado = baseAjustada.loc[(baseAjustada['Serviços PP'] == servico) & (baseAjustada['Current phase'] == 'ASSINADO') & (baseAjustada['Created at'].dt.year == ano2)]['Forma de Chegada'].value_counts()
            
            rc = {'figure.figsize':(10,4),
                  'axes.facecolor':'white',
                  'axes.edgecolor': 'white',
                  'axes.labelcolor': 'black',
                  'figure.facecolor': 'white',
                  'patch.edgecolor': 'white',
                  'text.color': 'black',
                  'xtick.color': 'black',
                  'ytick.color': 'black',
                  'grid.color': 'grey',
                  'font.size' : 10,
                  'axes.labelsize': 10,
                  'xtick.labelsize': 10,
                  'ytick.labelsize': 10}
            
            plt.rcParams.update(rc)
            
            fig, axes = plt.subplots()
            fig.suptitle('Forma de Chegada dos Contratos de ' + servico)
            plt.xticks(rotation = 90)
            try:
                sns.barplot(ax=axes, x= formaChegadaServicoFechado.index, y= list(formaChegadaServicoFechado), color = '#434141')
            except:
                st.text('')
            
            for p in axes.patches:
                axes.annotate(format(str(int(p.get_height()))), 
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha = 'center',
                va = 'center', 
                xytext = (0, 10),
                textcoords = 'offset points')
            
            st.pyplot(fig)
            
        
        st.text(' ')
        st.text(' ')
        st.text(' ')
        
        col9, space5, col10 = st.columns((5.0,0.5,5.0))
        
        with col9:
            
            if eng == 'Civil/Cartográfica':
                
                prospecServico = baseAjustada.loc[(baseAjustada['Serviços PC'] == servico) & (baseAjustada['Created at'].dt.year == ano2)]['Prospecção'].value_counts()
            
            elif eng == 'Ambiental':
                
                prospecServico = baseAjustada.loc[(baseAjustada['Serviços PAmb'] == servico) & (baseAjustada['Created at'].dt.year == ano2)]['Prospecção'].value_counts()
            
            elif eng == 'Elétrica':
                
                prospecServico = baseAjustada.loc[(baseAjustada['Serviços PE'] == servico) & (baseAjustada['Created at'].dt.year == ano2)]['Prospecção'].value_counts()
            
            elif eng == 'Mecânica':
                
                prospecServico = baseAjustada.loc[(baseAjustada['Serviços PM'] == servico) & (baseAjustada['Created at'].dt.year == ano2)]['Prospecção'].value_counts()
            
            elif eng == 'Produção':
                
                prospecServico = baseAjustada.loc[(baseAjustada['Serviços PP'] == servico) & (baseAjustada['Created at'].dt.year == ano2)]['Prospecção'].value_counts()
            
            rc = {'figure.figsize':(10,4),
                  'axes.facecolor':'white',
                  'axes.edgecolor': 'white',
                  'axes.labelcolor': 'black',
                  'figure.facecolor': 'white',
                  'patch.edgecolor': 'white',
                  'text.color': 'black',
                  'xtick.color': 'black',
                  'ytick.color': 'black',
                  'grid.color': 'grey',
                  'font.size' : 10,
                  'axes.labelsize': 10,
                  'xtick.labelsize': 10,
                  'ytick.labelsize': 10}
            
            plt.rcParams.update(rc)
            
            fig, axes = plt.subplots()
            fig.suptitle('Forma de Prospecção de ' + servico)
            plt.xticks(rotation = 90)
            try:
                sns.barplot(ax=axes, x= prospecServico.index, y= list(prospecServico), color = '#434141')
            except:
                st.text('')
            
            for p in axes.patches:
                axes.annotate(format(str(int(p.get_height()))), 
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha = 'center',
                va = 'center', 
                xytext = (0, 10),
                textcoords = 'offset points')
            
            st.pyplot(fig)
        
        with col10:
            
            if eng == 'Civil/Cartográfica':
                
                prospecServicoFechado = baseAjustada.loc[(baseAjustada['Serviços PC'] == servico) & (baseAjustada['Current phase'] == 'ASSINADO') & (baseAjustada['Created at'].dt.year == ano2)]['Prospecção'].value_counts()
            
            elif eng == 'Ambiental':
                prospecServicoFechado = baseAjustada.loc[(baseAjustada['Serviços PAmb'] == servico) & (baseAjustada['Current phase'] == 'ASSINADO') & (baseAjustada['Created at'].dt.year == ano2)]['Prospecção'].value_counts()
            
            elif eng == 'Elétrica':
                prospecServicoFechado = baseAjustada.loc[(baseAjustada['Serviços PE'] == servico) & (baseAjustada['Current phase'] == 'ASSINADO') & (baseAjustada['Created at'].dt.year == ano2)]['Prospecção'].value_counts()
            
            elif eng == 'Mecânica':
                prospecServicoFechado = baseAjustada.loc[(baseAjustada['Serviços PM'] == servico) & (baseAjustada['Current phase'] == 'ASSINADO') & (baseAjustada['Created at'].dt.year == ano2)]['Prospecção'].value_counts()
                
            elif eng == 'Produção':
                prospecServicoFechado = baseAjustada.loc[(baseAjustada['Serviços PP'] == servico) & (baseAjustada['Current phase'] == 'ASSINADO') & (baseAjustada['Created at'].dt.year == ano2)]['Prospecção'].value_counts()
            
            rc = {'figure.figsize':(10,4),
                  'axes.facecolor':'white',
                  'axes.edgecolor': 'white',
                  'axes.labelcolor': 'black',
                  'figure.facecolor': 'white',
                  'patch.edgecolor': 'white',
                  'text.color': 'black',
                  'xtick.color': 'black',
                  'ytick.color': 'black',
                  'grid.color': 'grey',
                  'font.size' : 10,
                  'axes.labelsize': 10,
                  'xtick.labelsize': 10,
                  'ytick.labelsize': 10}
            
            plt.rcParams.update(rc)
            
            fig, axes = plt.subplots()
            fig.suptitle('Forma de Prospecção dos Contratos de ' + servico)
            plt.xticks(rotation = 90)
            try:
                sns.barplot(ax=axes, x= prospecServicoFechado.index, y= list(prospecServicoFechado), color = '#434141')
            except:
                st.text('')
            
            for p in axes.patches:
                axes.annotate(format(str(int(p.get_height()))), 
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha = 'center',
                va = 'center', 
                xytext = (0, 10),
                textcoords = 'offset points')
            
            st.pyplot(fig)
            


        