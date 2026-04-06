import streamlit as st
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import io

st.set_page_config(page_title="Гранулација", layout="wide")

st.markdown("""
<style>
    h1 { font-size: 1.3rem !important; margin-bottom: 0.3rem !important; }
    h2, h3 { font-size: 1rem !important; margin: 0.3rem 0 0.2rem 0 !important; }
    [data-testid="stWidgetLabel"] p { font-size: 0.72rem !important; margin-bottom: 0 !important; }
    .stTextInput input { font-size: 0.78rem !important; padding: 0.2rem 0.4rem !important; }
    .stSlider { padding-top: 0.1rem !important; padding-bottom: 0.1rem !important; }
    .stSlider [data-testid="stTickBarMin"],
    .stSlider [data-testid="stTickBarMax"] { font-size: 0.65rem !important; }
    [data-testid="stVerticalBlock"] { gap: 0.3rem !important; }
    [data-testid="column"] { padding: 0 0.2rem !important; }
    .block-container { padding-top: 3.5rem !important; padding-bottom: 0.5rem !important; }
    .stDataEditor { font-size: 0.78rem !important; }
    .stDownloadButton button { font-size: 0.78rem !important; padding: 0.2rem 0.8rem !important; }
</style>
""", unsafe_allow_html=True)

st.title("Кривуља Гранулометријског Састава")

SIEVES = [0.063, 0.09, 0.25, 0.71, 2, 4, 8, 11.2, 16, 22.4, 31.5, 45]
SIEVE_LABELS = ["0.063", "", "0.25", "0.71", "2", "4", "8", "11.2", "16", "22.4", "31.5", "45"]
DEFAULT_COLORS = ["#ff0000", "#0000ff", "#008000", "#ff8800", "#8800ff", "#00aaaa"]
DEFAULT_NAMES = ["Мешавина А", "Мешавина Б", "Мешавина В", "Мешавина Г", "Мешавина Д", "Мешавина Ђ"]
EXAMPLE_PASSING = [
    [0, 1, 1.1, 1.3, 1.6, 2, 2.4, 4.5, 15, 99, 100, 100],
    [0, 1, 1.0, 1.0, 2.0, 19, 65, 90, 100, 100, 100, 100],
    [5, 6, 10, 20, 79, 99, 99.5, 100, 100, 100, 100, 100],
    [0, 0, 0.5, 1.0, 5.0, 30, 75, 95, 100, 100, 100, 100],
]

def f(x):
    return np.round(np.power(x, .5), decimals=2).astype('float')

def r(x):
    return np.round(np.emath.logn(.5, x), decimals=2).astype('float')

def make_chart(mix_names, mix_colors, mix_lws, passing_data):
    fig, ax = plt.subplots(figsize=(8, 6), dpi=150)
    ax.set_xscale("function", functions=(f, r))
    ax.set_xlim([0.063, 45])
    ax.set_ylim([0, 100])
    ax.set_xticks(SIEVES)
    ax.set_xticklabels(SIEVE_LABELS, rotation=45, ha='right')
    ax.grid(which='major', axis='both', linewidth=1, color='black')
    ax.set_xlabel("СТРАНА КВАДРАТНОГ ОТВОРА СИТА У mm (d^0,45)", size=11)
    ax.set_ylabel("ПРОЛАЗАК КРОЗ СИТО У % МАСЕ", size=11)

    for i in range(0, len(SIEVES) - 1, 2):
        for j in range(0, 100, 2):
            ax.plot([SIEVES[i], SIEVES[i + 1]], [j, j], color='black', linewidth=0.4)

    for name, color, lw, vals in zip(mix_names, mix_colors, mix_lws, passing_data):
        ax.plot(SIEVES, vals, linewidth=lw, color=color, label=name)

    ax.legend(loc="lower right")
    return fig


# --- Sidebar: number of mixtures ---
with st.sidebar:
    st.header("Подешавања")
    n_mix = st.number_input("Број мешавина", min_value=1, max_value=6, value=4, step=1)

# --- Two-column layout: left = inputs, right = chart ---
left, right = st.columns([1.1, 1])

with left:
    # Mixture metadata
    st.subheader("Мешавине")
    mix_cols = st.columns(n_mix)
    mix_names, mix_colors, mix_lws = [], [], []
    for i, col in enumerate(mix_cols):
        with col:
            name = st.text_input("Назив", value=DEFAULT_NAMES[i], key=f"name_{i}")
            color = st.color_picker("Боја", value=DEFAULT_COLORS[i], key=f"color_{i}")
            lw = st.slider("Дебљина", min_value=0.5, max_value=5.0,
                           value=2.0, step=0.5, key=f"lw_{i}")
            mix_names.append(name)
            mix_colors.append(color)
            mix_lws.append(lw)

    # Passing % table
    st.subheader("Пролазак кроз сито (%)")
    col_keys = [f"mix_{i}" for i in range(n_mix)]
    init_df = pd.DataFrame(
        {col_keys[i]: (EXAMPLE_PASSING[i] if i < len(EXAMPLE_PASSING) else [0.0] * 12)
         for i in range(n_mix)},
        index=[str(s) for s in SIEVES]
    )
    init_df.index.name = "Сито (mm)"

    col_cfg = {
        col_keys[i]: st.column_config.NumberColumn(
            label=mix_names[i],
            min_value=0.0,
            max_value=100.0,
            step=0.1,
            format="%.1f",
        )
        for i in range(n_mix)
    }

    edited_df = st.data_editor(
        init_df,
        key=f"editor_{n_mix}",
        use_container_width=True,
        column_config=col_cfg,
    )

with right:
    st.subheader("Дијаграм")
    passing_data = [edited_df[col_keys[i]].tolist() for i in range(n_mix)]
    fig = make_chart(mix_names, mix_colors, mix_lws, passing_data)
    st.pyplot(fig, use_container_width=True)

    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    st.download_button("Преузми PNG", buf.getvalue(), "granulacija.png", "image/png")
