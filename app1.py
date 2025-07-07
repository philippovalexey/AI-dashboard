import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Создаем примерные данные
pnl = pd.DataFrame({
    'Показатель': ['Общие доходы', 'Издержки (R&D, ФОТ, ИТ)', 'Прибыль'],
    'Сумма, млн руб': [120, 80, 40]
})
llm_effect = pd.DataFrame({
    'Метрика': ['Доп. доход от LLM','Сэкономлено'], 
    'Млн руб': [15, 12]
})
expenses = pd.DataFrame({
    'Категория': ['R&D','ФОТ','Инфраструктура'], 
    'Млн руб': [20, 50, 10]
})
teams = pd.DataFrame({
    'Команда': ['NLP','MLOps','DevOps','PM'],
    'План (шт)': [100, 80, 90, 50],
    'Факт (шт)': [95, 85, 80, 60]
})
employees = {
    'NLP': pd.DataFrame({'Сотрудник':['Иванов','Петров','Сидоров'], 'Выполнено': [30, 25, 40]}),
    'MLOps': pd.DataFrame({'Сотрудник':['Кузнецов','Новикова'], 'Выполнено': [50, 35]}),
    'DevOps': pd.DataFrame({'Сотрудник':['Федоров','Орлов','Морозова'], 'Выполнено': [20, 15, 30]}),
    'PM': pd.DataFrame({'Сотрудник':['Семенов','Зайцева'], 'Выполнено': [10, 12]})
}

app = dash.Dash(__name__)

# Фигуры: P&L, эффект LLM, структура расходов, план/факт
fig_pnl = px.bar(pnl, x='Показатель', y='Сумма, млн руб',
                 title='AI: P&L (млн руб)', text='Сумма, млн руб')
fig_llm = px.bar(llm_effect, x='Метрика', y='Млн руб', color='Метрика',
                 title='Эффект внедрения LLM (млн руб)', text='Млн руб')
fig_exp = px.pie(expenses, names='Категория', values='Млн руб',
                title='Структура расходов (млн руб)')
fig_teams = px.bar(teams, x='Команда', y=['План (шт)','Факт (шт)'], 
                   title='План-Факт по AI-командам', barmode='group')

app.layout = html.Div([
    html.H1("AI Operations Dashboard"),
    html.Div([
        dcc.Graph(figure=fig_pnl),
        dcc.Graph(figure=fig_llm),
        dcc.Graph(figure=fig_exp)
    ], style={'display': 'flex', 'justify-content': 'space-around'}),
    html.Div([
        dcc.Graph(id='team-chart', figure=fig_teams, style={'width': '60%'}),
        dcc.Graph(id='detail-chart', style={'width': '35%'})
    ], style={'display': 'flex'}),
    html.Div("Нажмите на столбец команды, чтобы увидеть вклад сотрудников", style={'padding': '10px'})
])

# Callback для drill-down: при клике на столбец команды обновляем график сотрудников
@app.callback(
    Output('detail-chart', 'figure'),
    Input('team-chart', 'clickData')
)
def update_detail(clickData):
    if clickData and 'points' in clickData:
        team = clickData['points'][0]['x']
        if team in employees:
            df = employees[team]
            fig = px.bar(df, x='Сотрудник', y='Выполнено',
                         title=f'Выполнение задач: {team} (шт)')
            fig.update_layout(showlegend=False)
            return fig
    # По умолчанию пустая фигура
    return px.bar(title="Выберите команду")

if __name__ == '__main__':
    app.run_server(debug=True)
