import streamlit as st
import pandas as pd
import altair as alt

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
        - Сокращение затрат на контактный центр (chat-боты, auto-reply)
        - Увеличение конверсии в кредитные продукты через LLM
        - Автоматизация проверок KYC/AML
        - Повышение эффективности риск-оценки заявок
        """)

with col2:
    economy_effect = pd.DataFrame({
        "Год": [2025, 2026, 2027, 2028],
        "Экономия от ИИ, млн ₽": [800, 1_500, 2_500, 4_000],
        "Доп. доход от ИИ, млн ₽": [400, 900, 2_300, 3_200]
    })
    st.altair_chart(
        alt.Chart(economy_effect).transform_fold(
            ["Экономия от ИИ, млн ₽", "Доп. доход от ИИ, млн ₽"],
            as_=["Категория", "Значение"]
        ).mark_line(point=True).encode(
            x=alt.X("Год:O", title="Год"),
            y=alt.Y("Значение:Q", title="млн ₽"),
            color="Категория:N"
        ).properties(width=500, height=300),
        use_container_width=True
    )

# -------------------------------
# 2. Расходы по MECE-структуре
# -------------------------------
st.header("📂 Расходы на AI-проекты по структуре MECE")

spending = pd.DataFrame({
    "Категория": ["ФОТ", "R&D", "Инфраструктура (облако, GPU)", "PM / Support / QA"],
    "2025": [3_200, 2_000, 1_200, 600],
    "2026": [3_500, 2_300, 1_400, 700]
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
# 4. Drill-down до сотрудников
# -------------------------------
st.header("🧑‍💻 Индивидуальные результаты сотрудников")

team_choice = st.selectbox("Выберите команду", ["NLP", "MLOps", "DevOps", "PM"])
mock_employees = {
    "NLP": pd.DataFrame({
        "Сотрудник": ["Иванов", "Петров", "Сидоров"],
        "Precision": [0.91, 0.93, 0.88]
    }),
    "MLOps": pd.DataFrame({
        "Сотрудник": ["Новикова", "Фролов"],
        "% успешных CI/CD": [96, 94]
    }),
    "DevOps": pd.DataFrame({
        "Сотрудник": ["Орлов", "Морозов", "Зайцева"],
        "Аптайм сервисов, %": [99.4, 99.7, 99.5]
    }),
    "PM": pd.DataFrame({
        "Сотрудник": ["Семенов", "Григорьева"],
        "MVP за квартал": [3, 4]
    })
}
st.table(mock_employees[team_choice])

st.markdown("---")
st.caption("© 2025 AI & LLM Business Dashboard для Альфа-Банка. Все данные — демонстрационные (mock).")