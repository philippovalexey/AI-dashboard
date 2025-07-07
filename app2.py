import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(layout="wide")
st.image("https://upload.wikimedia.org/wikipedia/commons/2/2d/Alfa-Bank_Logo_2021.svg", width=150)

st.title("AI Operations Dashboard – Альфа-Банк")
st.markdown("### Финансово-операционная панель управления AI-проектами (2025–2028)")

# -------------------------------
# 1. P&L Структура
# -------------------------------
st.header("📊 Экономика ИИ (P&L-структура)")

col1, col2 = st.columns(2)

with col1:
    pnl_data = pd.DataFrame({
        "Год": [2025, 2026, 2027, 2028],
        "Выручка банка, млн ₽": [600_000, 660_000, 730_000, 810_000],
        "AI-выручка, млн ₽": [7_200, 13_860, 25_550, 40_500]
    })
    st.altair_chart(
        alt.Chart(pnl_data).transform_fold(
            ["Выручка банка, млн ₽", "AI-выручка, млн ₽"],
            as_=["Категория", "Значение"]
        ).mark_bar().encode(
            x="Год:O",
            y="Значение:Q",
            color="Категория:N"
        ).properties(width=500, height=300),
        use_container_width=True
    )

with col2:
    economy_effect = pd.DataFrame({
        "Год": [2025, 2026, 2027, 2028],
        "Экономия затрат, млн ₽": [1_200, 2_400, 4_000, 6_000],
        "Доп. доход от LLM, млн ₽": [1_500, 3_000, 5_500, 9_000]
    })
    st.altair_chart(
        alt.Chart(economy_effect).transform_fold(
            ["Экономия затрат, млн ₽", "Доп. доход от LLM, млн ₽"],
            as_=["Метрика", "Значение"]
        ).mark_line(point=True).encode(
            x="Год:O",
            y="Значение:Q",
            color="Метрика:N"
        ).properties(width=500, height=300),
        use_container_width=True
    )

# -------------------------------
# 2. Структура расходов
# -------------------------------
st.header("📂 Структура расходов по MECE-дереву")

spending = pd.DataFrame({
    "Категория": ["R&D", "Фонд оплаты труда", "Инфраструктура", "Управление проектами"],
    "2025": [2_000, 3_500, 1_000, 500],
    "2026": [2_400, 3_800, 1_200, 600]
})

st.dataframe(spending.set_index("Категория"))

# -------------------------------
# 3. KPI по командам (план/факт + RAG)
# -------------------------------
st.header("📌 KPI команд AI (План / Факт / Статус)")

kpi_data = pd.DataFrame({
    "Команда": ["NLP", "MLOps", "DevOps", "PM"],
    "Показатель": ["Precision", "CI/CD %", "Аптайм %", "Кол-во MVP"],
    "План": [0.92, 0.97, 99.9, 8],
    "Факт": [0.89, 0.95, 99.5, 6],
    "RAG": ["Amber", "Amber", "Green", "Red"]
})

def color_rag(val):
    colors = {
        "Red": "background-color: #f8d7da",
        "Amber": "background-color: #fff3cd",
        "Green": "background-color: #d4edda"
    }
    return colors.get(val, "")

st.dataframe(kpi_data.style.applymap(color_rag, subset=["RAG"]))

# -------------------------------
# 4. Провал в сотрудников (mock)
# -------------------------------
st.header("🧑‍💻 Вклад отдельных сотрудников")

team_choice = st.selectbox("Выберите команду", ["NLP", "MLOps", "DevOps", "PM"])
mock_employees = {
    "NLP": pd.DataFrame({
        "Сотрудник": ["Иванов", "Петров", "Сидоров"],
        "Закрыто задач": [25, 30, 28]
    }),
    "MLOps": pd.DataFrame({
        "Сотрудник": ["Новикова", "Фролов"],
        "Закрыто задач": [40, 35]
    }),
    "DevOps": pd.DataFrame({
        "Сотрудник": ["Орлов", "Морозов", "Зайцева"],
        "Закрыто задач": [20, 18, 25]
    }),
    "PM": pd.DataFrame({
        "Сотрудник": ["Семенов", "Григорьева"],
        "Закрыто задач": [10, 12]
    })
}

st.bar_chart(mock_employees[team_choice].set_index("Сотрудник"))

st.markdown("---")
st.caption("© 2025 Финансово-операционный дашборд AI-проектов. Мок-данные для презентационных целей.")