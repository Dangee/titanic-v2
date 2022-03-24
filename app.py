######### Import your libraries #######
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly as py
import plotly.graph_objs as go
import plotly.express as px

import random


###### Define your variables #####
tabtitle = 'Titanic down!'
colors = ['#92A5E8','#8E44AD','#FFC300']
sourceurl = 'https://www.kaggle.com/c/titanic'
githublink = 'https://github.com/Dangee/titanic-dropdown'


###### Import a dataframe #######
df = pd.read_csv("https://raw.githubusercontent.com/austinlasseter/plotly_dash_tutorial/master/00%20resources/titanic.csv",
    usecols=['Survived','Pclass','Sex','Age','Fare','Embarked'])

df.rename(columns={'Sex':'Gender'}, inplace=True)
df['Cabin Class'] = df['Pclass'].map({1:'1st class', 2: '2nd class', 3:'3rd class'})
df['1st class'] = df['Pclass'] == '1st class'
df['2nd class'] = df['Pclass'] == '2nd class'
df['3rd class'] = df['Pclass'] == '3rd class'
df['Male'] = df['Gender']=='male'
df['Female'] = df['Gender']=='female'
df['Person Count'] = 1

category_list=['Survived','Male','Female']
continous_variable = ['Average Fare','Average Age','Count']
passenger_class_list=df['Cabin Class'].sort_values().unique()
embark_list=df['Embarked'].sort_values().unique()

df_summary_all = df.groupby(['Embarked','Pclass']).sum()
df_summary_all['Avg Age'] = round(df_summary_all['Age'] / df_summary_all['Person Count'], 1)
df_summary_all['Avg Fare'] = round(df_summary_all['Fare'] / df_summary_all['Person Count'], 2)

df_summary_sum_all = df.groupby(['Embarked']).sum()
df_summary_avg_all = df.groupby(['Embarked']).mean()


########### initialize chart
pie_chart_data = [go.Pie(labels=df_summary_sum_all.index, values=df_summary_sum_all['Survived'], hole=.3)]
pie_fig = go.Figure(pie_chart_data)
pie_fig.update_traces(textinfo='value')

########### Initiate the app
external_stylesheets = ['./assets/my_cWLwgPP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = tabtitle

####### Layout of the app ########
app.layout = html.Div(
    children = [
        html.H1(
                id = 'header-id',
                children = [
                    'TITANIC FINAL VOYAGE',
                    html.Br(),
                    'Analysis by port of embarkment'],
                className = "header"
              ),
        html.Div(
            children = [
                html.Div(
                    children = html.H3("Choose parameters for your analysis:"),
                    className = "row"
                ),
                html.Div(id = "variable-id",
                    children=[
                        html.P("Variable:"),
                        dcc.Dropdown(
                            id='dropdown-variable-id',
                            options=[{'label': i, 'value': i} for i in category_list],
                            value=category_list[0],
                            clearable=False,
                            className="dropdown"
                        )
                    ],
                    className="two columns",
                ),
                html.Div(id="class-id",
                         children=[
                             html.P("Passengers:"),
                             dcc.Dropdown(
                                 id='dropdown-class-id',
                                 options=[{'label': i, 'value': i} for i in passenger_class_list],
                                 value=passenger_class_list[0],
                                 clearable=True,
                                 multi=True,
                                 placeholder="All Passengers",
                                className="dropdown"
                             )
                         ],
                         className="two columns"
                         ),
                html.Div(id="go-button-id",
                         children=[
                             # html.Br(),
                             html.Br(),
                             html.Button(
                                 id='submit-val',
                                 children='Refresh data',
                                 n_clicks=0,
                                 className="button"
                             )
                         ],
                         className="two columns"
                )
            ],
            className="row"
        ),
        html.Br(),
        html.Div(
            children=[
                html.Div(
                    html.Div(
                        children=[
                            html.H5("Count by Port of Embarkment"),
                            dcc.Graph(id='display-pie',
                                      figure=pie_fig)
                        ],
                        className="card"
                    ),
                    className="four columns"
                ),
                html.Div(
                    html.Div(
                        children=dcc.Graph(id='display-bar'),
                        className="card",
                    ),
                    className="eight columns"
                )
            ],
            className="row"
        ),
        html.A('Code on Github', href=githublink),
        html.Br(),
        html.A("Data Source", href=sourceurl),
    ]
)


######### Interactive callbacks go here #########
@app.callback(
    Output('display-pie', 'figure'),
               # Output('display-bar','figure')],
    Input('go-button-id', 'n_clicks'),
    State('dropdown-variable-id', 'value')
)
def display_value(clicks, display_value): # passenger_class):
    pie_chart_data = [go.Pie(labels=df_summary_all.index, values=df_summary_all[display_value], hole=.3)]
    pie_fig = go.Figure(pie_chart_data)
    pie_fig.update_traces(textinfo='value')

    return pie_fig

    # pie_chart_data = px.pie(df_summary_all, values=display_value, names="index", hole=.3)

    # pie_chart_data = [go.Pie({"labels": df_summary_all.index, "values": df_summary_all[display_value]})]

#     grouped_mean=df.groupby(['Cabin Class', 'Embarked'])[display_value].mean()
#     results=pd.DataFrame(grouped_mean)
#
#     # Create a grouped bar chart
#     random_data1=[]
#     for i in range(0,len(embark_list)):
#         random_data.append(random.choice(range(1,20)))
#
#     random_data2=[]
#     for i in range(0,len(embark_list)):
#         random_data.append(random.choice(range(1,20)))
#
#     random_data3=[]
#     for i in range(0,len(embark_list)):
#         random_data.append(random.choice(range(1,20)))
#
    # bar_data1 = go.Bar(
    #     x=passenger_class_list[0],
    #     y=random_data1,
    #     name='First Class',
    #     marker=dict(color=colors[0])
    # )
    # bar_data2 = go.Bar(
    #     x=passenger_class_list[1],
    #     y=random_data2,
    #     name='Second Class',
    #     marker=dict(color=colors[1])
    # )
    # bar_data3 = go.Bar(
    #     x=passenger_class_list[3],
    #     y=random_data1,
    #     name='Third Class',
    #     marker=dict(color=colors[2])
    # )
    #
    # bar_layout = go.Layout(
    #     title='Bar Chart',
    #     xaxis = dict(title = 'Passenger Class'), # x-axis label
    #     yaxis = dict(title = "selected var"), # y-axis label
    #     # yaxis = dict(title = str(continuous_var)), # y-axis label
    # )

    # return pie_fig  # , go.Figure(placeholder_data) # go.Figure(bar_data=[bar_data1, bar_data2, bar_data3], layout=bar_layout)


######### Run the app #########
if __name__ == '__main__':
    app.run_server(debug=True)
