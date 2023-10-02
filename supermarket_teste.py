import dash
from dash import html, dcc 
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

load_figure_template('minty')

app = dash.Dash(
    external_stylesheets=[dbc.themes.MINTY])
#em 'https://bootswatch.com/' podemos ver os temas disponiveis
# em https://hellodash.pythonanywhere.com/ tbem existem temas, em especial para figures, clicando em 'Apply a Bootstrap Theme to Figures
server = app.server

# ================Ingestão de dados ============#
df_data = pd.read_csv(r"C:\Users\luigi\OneDrive\Documentos\DATA\Data_Science\ASIMOV\Dashboards Interativos com Python\Projetos\Dashboards\Supermarket Sales\supermarket_sales.csv")
#df_data.head(5)

#transformando a coluna date de object para datetime
df_data['Date']= pd.to_datetime(df_data["Date"])



# ==================== Layout ================== #
app.layout = html.Div(children=[
      
        dbc.Row([
                dbc.Col([
                     dbc.Card([   
                        html.H2("  SUPER MARKET", style={'font-family': 'Voltaire', "font_size": '30px', 'margin-top': '10px','margin-bottom,': '20px'}), 
                        html.Hr(), #insere uma linha de divisao
                        html.H5("Cidades:",style={'margin-top': '30px'}),
                        dcc.Checklist(df_data['City'].unique(), df_data['City'].unique(), id='check_city', 
                                      inputStyle={'margin-right': "10px", 'margin-left': '10px', 'margin-top': '10px'}), 
                        # o segundo argumento é qual das caixas ja aparecerão marcadas. no caso, todas as cidades

                        html.H5('Variável de análise:', style={'margin-top': '60px'}),
                        dcc.RadioItems(['gross income', 'Rating'], 'gross income', id= 'main_variable',
                                       inputStyle={'margin-right': "10px", 'margin-left': '10px', 'margin-top': '10px'}),
                        ], style= {"height": "880px", "margin":'20px', 'padding': '5px'})
                        # o segundo argumento é qual daos botoes ja aparecerá marcado. no caso, "gross income"
                      ], sm=2),
                dbc.Col([
                      dbc.Row([
                          dbc.Col([dcc.Graph(id='city_fig')], sm=4),  
                          dbc.Col([dcc.Graph(id='gender_fig')], sm=4), 
                          dbc.Col([dcc.Graph(id='pay_fig')], sm=4 , style={'width': '340px'}) 
                      ]),
                      dbc.Row([dcc.Graph(id='income_per_date_fig')], style={'width': '99%'}),
                      dbc.Row([dcc.Graph(id='income_per_product_fig')], style={'width': '99%'})
                #criando gráficos vazios q serão preenchidos pelo callback
                ], sm=10)     
             ])
              
           ]
        )


#====================== Callbacks =================#

@app.callback([
        Output('city_fig', 'figure'),
        Output('pay_fig', 'figure'),
        Output('gender_fig', 'figure'),
        Output('income_per_date_fig', 'figure'),
        Output('income_per_product_fig', 'figure')]
,
        [
            Input('check_city', 'value'),
            Input('main_variable', 'value')
        ]
)

def render_graphs(cities, main_variable):
        operation= np.sum if main_variable == 'gross income' else np.mean
        df_filtered= df_data[df_data['City'].isin(cities)]
        df_city = df_filtered.groupby('City')[main_variable].apply(operation).to_frame().reset_index()
        df_gender = df_filtered.groupby(['Gender', 'City'])[main_variable].apply(operation).to_frame().reset_index()
        df_payment = df_filtered.groupby('Payment')[main_variable].apply(operation).to_frame().reset_index()
        df_income_time = df_filtered.groupby('Date')[main_variable].apply(operation).to_frame().reset_index()
        df_product_income = df_filtered.groupby(['Product line','City'])[main_variable].apply(operation).to_frame().reset_index()
        
        fig_city =px.bar(df_city, x='City', y=main_variable)
        fig_payment =px.bar(df_payment, y='Payment', x=main_variable, orientation='h')
        fig_gender =px.bar(df_gender, x='Gender', y=main_variable, color="City", barmode= 'group')
        fig_product_income =px.bar(df_product_income, x=main_variable, y='Product line', color="City", orientation='h', barmode='group')
        fig_income_date =px.bar(df_income_time, y=main_variable, x='Date')

        for fig in [fig_city, fig_payment, fig_gender, fig_income_date]:
              fig.update_layout(margin=dict(l=0, r=0, t=20, b=20), height=200, template='minty')

        
        fig_product_income.update_layout(margin=dict(l=0, r=0, t=20, b=20), height=500)
        #em plotly.com/python/templates conseguimos ver os templates disponiveis para graficos

        return fig_city, fig_payment, fig_gender, fig_income_date, fig_product_income





#====================== Run server ===============#
if __name__ == "__main__":
    app.run_server(port=8050, debug=True)
