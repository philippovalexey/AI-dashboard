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

st.markdown("#### 📉 Общие расходы банка vs. Экономия от ИИ")
growth_rate = st.slider("Прогнозируемый рост эффекта ИИ (% ежегодно)", min_value=0, max_value=100, value=0, step=5)
relative_toggle = st.checkbox("Показать в долях от общих расходов", value=False)

base_expense = [450_000, 470_000, 495_000, 520_000]
base_ai_saving = [800, 1_500, 2_500, 4_000]
years = [2025, 2026, 2027, 2028]

ai_saving_forecasted = [round(val * (1 + growth_rate / 100) ** i) for i, val in enumerate(base_ai_saving)]
expense_data = pd.DataFrame({
    "Год": years,
    "Расходы банка, млн ₽": base_expense,
    "Экономия от ИИ, млн ₽": ai_saving_forecasted
})
expense_data["Расходы без ИИ, млн ₽"] = expense_data["Расходы банка, млн ₽"] - expense_data["Экономия от ИИ, млн ₽"]

if relative_toggle:
    expense_data["Экономия от ИИ, %"] = round(expense_data["Экономия от ИИ, млн ₽"] / expense_data["Расходы банка, млн ₽"] * 100, 2)
    chart = alt.Chart(expense_data).mark_line(point=True).encode(
        x=alt.X("Год:O", title="Год"),
        y=alt.Y("Экономия от ИИ, %:Q", title="Экономия от ИИ (%)"),
        tooltip=["Год", "Экономия от ИИ, %"]
    ).properties(width=500, height=300)
    st.altair_chart(chart, use_container_width=True)
else:
    base = alt.Chart(expense_data).encode(x=alt.X("Год:O", title="Год"))
    bar_base = base.mark_bar(color="#AEC6CF").encode(
        y=alt.Y("Расходы без ИИ, млн ₽:Q", title="Расходы, млн ₽"),
        tooltip=["Год", "Расходы банка, млн ₽", "Экономия от ИИ, млн ₽"]
    )
    bar_ai = base.mark_bar(color="#FF6961").encode(
        y="Экономия от ИИ, млн ₽:Q"
    )
    chart = (bar_base + bar_ai).properties(width=500, height=300).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    ).configure_view(strokeWidth=0)
    st.altair_chart(chart, use_container_width=True)

with st.expander("📌 Из чего формируется экономия, связанная с ИИ"):
    st.markdown("""
    **Основные направления сокращения затрат:**
    - 🤖 Сокращение затрат на контактный центр (chat-боты, auto-reply) — раньше 10 млн/мес, теперь 2 млн
    - 🔍 Автоматизация проверок KYC/AML и предотвращение мошенничества
    - 🏦 Оптимизация персонала в back office
    - 📉 Снижение стоимости обработки транзакций через LLM

    **Инвестиции в ИИ: 6 000 млн ₽**  
    **Сокращение затрат с 2023: > 20 млн ₽ / мес**  
    **Доля экономии от ИИ: до 6.9% от операционных расходов в 2028 году**
    """)

with st.expander("🗂️ Сравнение с аналогичными банками (peer benchmark)"):
    benchmark = pd.DataFrame({
        "Банк": ["Альфа-Банк", "Тинькофф", "Сбер", "ВТБ"],
        "Экономия от ИИ, % от расходов": [6.9, 5.2, 8.5, 4.4]
    })
    st.bar_chart(benchmark.set_index("Банк"))

with st.expander("📈 Waterfall: Эффект от ИИ по направлениям"):
    waterfall_data = pd.DataFrame({
        "Этап": [
            "Инвестиции в ИИ (CapEx)",
            "Экономия: Контактный центр",
            "Экономия: KYC/AML",
            "Экономия: Бэк-офис",
            "Экономия: Обработка транзакций",
            "Совокупный эффект"
        ],
        "Значение": [-6000, 96, 420, 1800, 350, 0]
    })
    waterfall_data.loc[5, "Значение"] = waterfall_data["Значение"][1:5].sum() - 6000
    waterfall_data["Цвет"] = ["Инвестиции", "Экономия", "Экономия", "Экономия", "Экономия", "Итог"]

    waterfall_chart = alt.Chart(waterfall_data).mark_bar().encode(
        x=alt.X("Этап:N", sort=None, title=""),
        y=alt.Y("Значение:Q", title="млн ₽"),
        color=alt.Color("Цвет:N", scale=alt.Scale(
            domain=["Инвестиции", "Экономия", "Итог"],
            range=["#ff6961", "#77dd77", "#779ecb"]
        )),
        tooltip=["Этап", "Значение"]
    ).properties(width=700, height=400)
    st.altair_chart(waterfall_chart, use_container_width=True)
# -------------------------------
# 2. Структура расходов (MECE)
# -------------------------------
st.header("📂 Расходы на AI-проекты, млн ₽")

with st.expander("📌 Детализация"):
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
st.header("📅 План-график AI-проектов")

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


st.markdown("### Финансово-операционная панель управления AI-проектами (2025–2028)")

# -------------------------------
# -------------------------------
# Проектный дашборд (индивидуальные метрики)
# -------------------------------
st.header("📈 Индивидуальные дашборды проектов")

# -- Основные метрики по кварталам --
project_data = pd.DataFrame({
    "Проект": ["Запуск чат-бота"] * 4 + ["Модель оценки риска"] * 4 + ["Интеграция CI/CD"] * 4 + ["LLM в КЦ"] * 4 + ["Облачная миграция"] * 4,
    "Квартал": ["Q1", "Q2", "Q3", "Q4"] * 5,
    "Прогресс, %": [20, 50, 80, 100, 10, 35, 60, 100, 25, 55, 85, 100, 15, 40, 70, 95, 5, 30, 60, 100],
    "CSAT, %": [87, 89, 90, 91, 82, 85, 88, 90, 80, 82, 85, 87, 88, 89, 91, 93, 83, 84, 86, 88],
    "Отклонение от срока, дней": [0, 1, -2, -3, 5, 3, 0, -1, 2, 0, -2, -4, 1, 0, -1, -2, 7, 5, 1, 0]
})

# -- Новые метрики (по дате) --
voc_data = pd.DataFrame({
    "Проект": ["Запуск чат-бота"] * 3,
    "Дата": pd.to_datetime(["2025-01-31", "2025-02-29", "2025-03-31"]),
    "VOC, %": [72, 75, 78]
})

accuracy_data = pd.DataFrame({
    "Проект": ["Запуск чат-бота"] * 6,
    "Дата": pd.to_datetime(["2025-03-01", "2025-03-08", "2025-03-15", "2025-03-22", "2025-03-29", "2025-04-05"]),
    "Достоверность, %": [87, 88, 90, 91, 92, 91]
})

# -- Выбор проекта --
selected_project = st.selectbox("Выберите проект для анализа:", project_data["Проект"].unique())

# -- Фильтрация по выбранному проекту --
project_subset = project_data[project_data["Проект"] == selected_project]
voc_subset = voc_data[voc_data["Проект"] == selected_project]
accuracy_subset = accuracy_data[accuracy_data["Проект"] == selected_project]
with st.expander("➕ Добавить замер VOC / Достоверности"):
    new_date = st.date_input("Дата замера", datetime.date.today())
    new_voc = st.number_input("VOC, %", min_value=0, max_value=100, step=1)
    new_accuracy = st.number_input("Достоверность, %", min_value=0, max_value=100, step=1)
    if st.button("💾 Добавить замеры"):
        st.warning("🔒 Пока данные не сохраняются. Добавим сохранение позже через базу или session_state.")
# -- Основные графики --
st.subheader(f"📊 Ключевые метрики: {selected_project}")

chart_progress = alt.Chart(project_subset).mark_line(point=True, color="#007BFF").encode(
    x=alt.X("Квартал:O"),
    y=alt.Y("Прогресс, %:Q"),
    tooltip=["Квартал", "Прогресс, %"]
).properties(height=250, title="Динамика прогресса проекта")

chart_csat = alt.Chart(project_subset).mark_line(point=True, color="#00CC88").encode(
    x=alt.X("Квартал:O"),
    y=alt.Y("CSAT, %:Q"),
    tooltip=["Квартал", "CSAT, %"]
).properties(height=250, title="Удовлетворённость (CSAT)")

chart_delay = alt.Chart(project_subset).mark_bar(color="#FF9966").encode(
    x=alt.X("Квартал:O"),
    y=alt.Y("Отклонение от срока, дней:Q"),
    tooltip=["Квартал", "Отклонение от срока, дней"]
).properties(height=250, title="Отклонение от срока (в днях)")

st.altair_chart(chart_progress, use_container_width=True)
st.altair_chart(chart_csat, use_container_width=True)
st.altair_chart(chart_delay, use_container_width=True)

# -- VOC график --
if not voc_subset.empty:
    voc_chart = alt.Chart(voc_subset).mark_line(point=True, color="#6A5ACD").encode(
        x=alt.X("Дата:T", title="Месяц"),
        y=alt.Y("VOC, %:Q"),
        tooltip=["Дата", "VOC, %"]
    ).properties(height=250, title="Оценка голоса клиента (VOC)")
    st.altair_chart(voc_chart, use_container_width=True)

# -- Accuracy график --
if not accuracy_subset.empty:
    acc_chart = alt.Chart(accuracy_subset).mark_line(point=True, color="#DC143C").encode(
        x=alt.X("Дата:T", title="Дата замера"),
        y=alt.Y("Достоверность, %:Q"),
        tooltip=["Дата", "Достоверность, %"]
    ).properties(height=250, title="Точность ответов (достоверность)")
    st.altair_chart(acc_chart, use_container_width=True)

# -- Таймлайн проекта --
st.subheader("📅 Таймлайн проекта")
project_timeline = pd.DataFrame({
    "Проект": ["Запуск чат-бота", "Модель оценки риска", "Интеграция CI/CD", "LLM в КЦ", "Облачная миграция"],
    "Начало": [datetime.date(2025, 1, 15), datetime.date(2025, 2, 10), datetime.date(2025, 3, 1),
               datetime.date(2025, 3, 20), datetime.date(2025, 4, 5)],
    "Окончание": [datetime.date(2025, 2, 28), datetime.date(2025, 4, 1), datetime.date(2025, 4, 10),
                  datetime.date(2025, 6, 1), datetime.date(2025, 6, 30)]
})

timeline_chart = alt.Chart(project_timeline[project_timeline["Проект"] == selected_project]).mark_bar().encode(
    x='Начало:T',
    x2='Окончание:T',
    y=alt.Y('Проект:N', sort=None),
    color=alt.value("#007BFF")
).properties(height=100)

st.altair_chart(timeline_chart, use_container_width=True)

st.markdown("---")
st.caption("© 2025 AI & LLM Business Dashboard для Альфа-Банка. Все данные — демонстрационные (mock).")
