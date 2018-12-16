import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('train.csv')

app.layout = html.Div([
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        id='year-slider',
        min=df['modelyear'].min(),
        max=df['modelyear'].max(),
        value=df['modelyear'].min(),
        marks={str(modelyear): str(modelyear) for modelyear in df['modelyear'].unique()}
    )
])


@app.callback(
    dash.dependencies.Output('graph-with-slider', 'figure'),
    [dash.dependencies.Input('year-slider', 'value')])
def update_figure(selected_year):
    filtered_df = df[df.modelyear == selected_year]
    traces = []
    for i in filtered_df.company.unique():
        df_by_company = filtered_df[filtered_df['company'] == i]
        traces.append(go.Scatter(
            x=df_by_company['horsepower'],
            y=df_by_company['mpg'],
            text=df_by_company['car name'],
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'title': 'horsepower', 'range': [0, 220]},
            yaxis={'title': 'mpg', 'range': [0, 50]},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)