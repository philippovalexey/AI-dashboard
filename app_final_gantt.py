import streamlit as st
import pandas as pd
import altair as alt
import datetime

st.set_page_config(layout="wide")
st.image("https://upload.wikimedia.org/wikipedia/commons/8/87/Alfabank_logo.png", width=180)

st.title("AI Operations Dashboard – Альфа-Банк")
st.markdown("### Финансово-операционная панель управления AI-проектами (2025–2028)")

# -------------------------------
# 1. Экономика ИИ (P&L-структура)
# -------------------------------
st.header("📊 Экономика ИИ (P&L-структура)")

col1, col2 = st.columns(2)

with col1:
    pnl_data = pd.DataFrame({
        "Год": [2025, 2026, 2027, 2028],
        "Общая прибыль, млн ₽": [29_146, 35_000, 42_000, 49_000],
        "Прибыль, связанная с ИИ, млн ₽": [1_200, 2_400, 4_800, 7_200]
    })
    st.altair_chart(
        alt.Chart(pnl_data).transform_fold(
            ["Общая прибыль, млн ₽", "Прибыль, связанная с ИИ, млн ₽"],
            as_=["Метрика", "Значение"]
        ).mark_bar().encode(
            x=alt.X("Год:O", title="Год"),
            y=alt.Y("Значение:Q", title="млн ₽"),
            color="Метрика:N"
        ).properties(width=500, height=300),
        use_container_width=True
    )
    with st.expander("📌 Из чего формируется прибыль, связанная с ИИ"):
        st.markdown("""
        **Источники прибыли от ИИ:**
        - 💬 Сокращение затрат на контактный центр (chat-боты, auto-reply)
        - 💸 Увеличение конверсии в кредитные продукты через LLM
        - 🛡️ Автоматизация проверок KYC/AML
        - 📈 Повышение эффективности риск-оценки заявок

        **Инвестиции в ИИ: 6 000 млн ₽**  
        **Срок окупаемости: ~3 года**  
        **Доля прибыли от ИИ: 4.1% в 2028**
        """)

with col2:
    economy_effect = pd.DataFrame({
        "Год": [2025, 2026, 2027, 2028],
        "Экономия от ИИ, млн ₽": [800, 1_500, 2_500, 4_000],
        "Доп. доход от ИИ, млн ₽": [400, 900, 2_300, 3_200]
    }).melt(id_vars=["Год"], var_name="Категория", value_name="Значение")

    if not economy_effect.empty:
        chart = alt.Chart(economy_effect).mark_line(point=True).encode(
            x=alt.X("Год:O", title="Год"),
            y=alt.Y("Значение:Q", title="млн ₽"),
            color=alt.Color("Категория:N", title=""),
            tooltip=["Год", "Категория", "Значение"]
        ).properties(width=500, height=300)
        st.altair_chart(chart, use_container_width=True)

# -------------------------------
# 2. Структура расходов (MECE)
# -------------------------------
st.header("📂 Расходы на AI-проекты, млн ₽")

with st.expander("📌 Детализация по MECE"):
    spending = pd.DataFrame({
        "Категория": [
            "ФОТ — NLP (6 чел)", "ФОТ — MLOps (4 чел)", "ФОТ — DevOps (3 чел)", "ФОТ — PM (2 чел)",
            "R&D — эксперименты", "R&D — лицензии LLM", "Инфраструктура — GPU", "Инфраструктура — облако", "PM / Support / QA"
        ],
        "2025": [1_200, 900, 600, 300, 600, 400, 700, 500, 400],
        "2026": [1_400, 1_000, 650, 320, 700, 450, 750, 550, 450]
    })
    st.dataframe(spending.set_index("Категория"))

# -------------------------------
# 3. KPI команд (план / факт / RAG)
# -------------------------------
st.header("📌 KPI команд (план / факт / статус RAG)")

kpi_data = pd.DataFrame({
    "Команда": ["NLP", "MLOps", "DevOps", "PM"],
    "Показатель": ["Precision классификации", "% CI/CD-деплоев", "Аптайм сервисов", "Кол-во MVP за квартал"],
    "План": [0.92, 0.97, 99.9, 8],
    "Факт": [0.89, 0.95, 99.5, 6],
    "RAG": ["🟠", "🟠", "🟢", "🔴"]
})

st.dataframe(kpi_data)

# -------------------------------
# 4. Индивидуальные результаты
# -------------------------------
st.header("🧑‍💻 Индивидуальные результаты сотрудников")

team_choice = st.selectbox("Выберите команду", ["NLP", "MLOps", "DevOps", "PM"])

employee_data = {
    "NLP": pd.DataFrame({
        "Сотрудник": ["Иванов", "Петров", "Сидоров"],
        "План задач": [28, 30, 26],
        "Факт задач": [25, 30, 28]
    }),
    "MLOps": pd.DataFrame({
        "Сотрудник": ["Новикова", "Фролов"],
        "План задач": [38, 36],
        "Факт задач": [40, 35]
    }),
    "DevOps": pd.DataFrame({
        "Сотрудник": ["Орлов", "Морозов", "Зайцева"],
        "План задач": [20, 20, 23],
        "Факт задач": [20, 18, 25]
    }),
    "PM": pd.DataFrame({
        "Сотрудник": ["Семенов", "Григорьева"],
        "План задач": [12, 10],
        "Факт задач": [10, 12]
    })
}

df = employee_data[team_choice]
df["Исполнение, %"] = (df["Факт задач"] / df["План задач"] * 100).round(1)
df = df.sort_values("Исполнение, %", ascending=False).reset_index(drop=True)

st.dataframe(df)

# -------------------------------
# 5. План-график (Gantt)
# -------------------------------
st.header("📅 План-график AI-проектов (Gantt Chart)")

gantt_data = pd.DataFrame({
    "Проект": ["Запуск чат-бота", "Модель оценки риска", "Интеграция CI/CD", "LLM в КЦ", "Облачная миграция"],
    "Начало": [datetime.date(2025, 1, 15), datetime.date(2025, 2, 10), datetime.date(2025, 3, 1),
               datetime.date(2025, 3, 20), datetime.date(2025, 4, 5)],
    "Окончание": [datetime.date(2025, 2, 28), datetime.date(2025, 4, 1), datetime.date(2025, 4, 10),
                  datetime.date(2025, 6, 1), datetime.date(2025, 6, 30)]
})

gantt_chart = alt.Chart(gantt_data).mark_bar().encode(
    x='Начало:T',
    x2='Окончание:T',
    y=alt.Y('Проект:N', sort=None),
    color=alt.value("#007BFF")
).properties(height=300)

st.altair_chart(gantt_chart, use_container_width=True)

st.markdown("---")
st.caption("© 2025 AI & LLM Business Dashboard для Альфа-Банка. Все данные — демонстрационные (mock).")