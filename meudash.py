import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State
import pandas_datareader as web
import datetime
from dateutil.relativedelta import relativedelta
import plotly.graph_objs as go

inicio = datetime.datetime.today() - relativedelta(years=1)
termino = datetime.datetime.today()

app = dash.Dash()
app.title = 'Fluxo de Ações'
app.layout = html.Div([
    html.Div([
        html.H1("Fluxo de Ações"),
        html.Img(src="/assets/imgFundo.png")
    ], className="banner"),
    html.Label("Entre com o Código da Ação:"),
    html.Div([
        dcc.Input(
            id="codAcao",
            placeholder="Código da Ação",
            type="text",
            value="AAPL"
        ),
        html.Button(id="submit-button", n_clicks=0, children="Trocar"),
        html.Label("Ex. AAPL, GOOG, TSLA, IBM, MSFT, FB"),
    ]),
    html.Div([
        html.Div([
            dcc.Graph(id="graph_high"),
        ], className="six columns"),
        html.Div([
            dcc.Graph(id="graph_close"),
        ], className="six columns"),
    ], className="row"),
])

@app.callback(Output("graph_high", "figure"),
              [Input("submit-button", "n_clicks")],
              [State("codAcao", "value")])
def alterar_maisAlto(n_clicks, codigo):
    df = web.DataReader(codigo, data_source="yahoo", start=inicio, end=termino)
    trace_high = go.Scatter(x=list(df.index), y=list(df.High), name="Alto", line=dict(color="#46A444"))
    return {
        "data": [trace_high],
        "layout": {"title": "Preço Mais Alto"}
    }

@app.callback(Output("graph_close", "figure"),
                     [Input("submit-button", "n_clicks")],
                     [State("codAcao", "value")])
def alterar_fechamento(n_clicks, codigo):
    df = web.DataReader(codigo, data_source="yahoo", start=inicio, end=termino)
    trace_close = go.Scatter(x=list(df.index), y=list(df.Close), name="Fechamento", line=dict(color="#A4444D"))
    return {
        "data": [trace_close],
        "layout": {"title": "Preço Fechamento"}
    }


if __name__ == "__main__":
    app.run_server(debug=True)
