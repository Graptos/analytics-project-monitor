import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# Заголовок в стиле диссертации
st.set_page_config(page_title="Analytics-Project Monitor", layout="wide")
st.title("📊 Модуль оценки аналитической компетентности (v.1.0)")
st.subheader("Кейс проекта: «If I were a dosimetrist…» (8 класс)")

# 1. Настройка весовых коэффициентов (из вашего ТЗ)
weights = {"Data Mining": 0.1, "Classification": 0.2, "Causality": 0.3, "Prediction": 0.3, "Reflection": 0.1}
categories = list(weights.keys())

# 2. Ввод данных (Интерфейс для эксперта)
st.sidebar.header("📝 Ввод экспертных оценок (0-10)")
col1, col2 = st.sidebar.columns(2)

before_vals = []
after_vals = []

for cat in categories:
    with col1:
        b = st.number_input(f"{cat} (Вход)", 0, 10, 2)
        before_vals.append(b)
    with col2:
        a = st.number_input(f"{cat} (Защита)", 0, 10, 5)
        after_vals.append(a)

# 3. Математическое ядро (Аддитивная свертка)
k_before = sum(v * weights[cat] for v, cat in zip(before_vals, categories))
k_after = sum(v * weights[cat] for v, cat in zip(after_vals, categories))
delta = round(k_after - k_before, 2)

# 4. Визуализация (Лепестковая диаграмма)
fig = go.Figure()

fig.add_trace(go.Scatterpolar(
    r=before_vals + [before_vals[0]],
    theta=categories + [categories[0]],
    fill='toself', name='Входной срез', line_color='silver'
))

fig.add_trace(go.Scatterpolar(
    r=after_vals + [after_vals[0]],
    theta=categories + [categories[0]],
    fill='toself', name='Защита проекта', line_color='blue'
))

fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 10])), showlegend=True)

# 5. Вывод результатов
c1, c2 = st.columns([2, 1])

with c1:
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.metric("Интегральный показатель K (Вход)", round(k_before, 2))
    st.metric("Интегральный показатель K (Финал)", round(k_after, 2))
    st.info(f"**Абсолютный прирост (Δ): {delta}**")
    
    if delta > 1.5:
        st.success("Вывод: Высокая эффективность технологии")
    else:
        st.warning("Вывод: Требуется коррекция траектории")

st.caption("Разработано для диссертационного исследования по спец. 5.8.7 (Ленинградская обл.)")

