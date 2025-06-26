import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patches as mpatches

# ─────────────────────────────────────────────
# 1) DATOS DE LOS TRES PARTIDOS
# ─────────────────────────────────────────────
games = [
    dict(Game="G1", Minutes=21 + 20/60, Points=3,
         _2FGM=0, _2FGA=4, _3FGM=1, _3FGA=5, FTM=0, FTA=0,
         OffReb=2, DefReb=4, Assists=3, Steals=1, Turnovers=3),

    dict(Game="G2", Minutes=32 + 27/60, Points=23,
         _2FGM=3, _2FGA=5, _3FGM=5, _3FGA=13, FTM=2, FTA=2,
         OffReb=1, DefReb=3, Assists=8, Steals=0, Turnovers=0),

    dict(Game="G3", Minutes=23 + 8/60, Points=12,
         _2FGM=2, _2FGA=7, _3FGM=0, _3FGA=4, FTM=8, FTA=8,
         OffReb=3, DefReb=2, Assists=2, Steals=0, Turnovers=0),
]
df = pd.DataFrame(games)

# ────────── 2) MÉTRICAS DERIVADAS ──────────
df["FGA"]     = df["_2FGA"] + df["_3FGA"]
df["FGM"]     = df["_2FGM"] + df["_3FGM"]
df["eFG%"]    = (df["FGM"] + 0.5 * df["_3FGM"]) / df["FGA"]
df["TS%"]     = df["Points"] / (2 * (df["FGA"] + 0.44 * df["FTA"]))
df["FT Rate"] = df["FTA"] / df["FGA"]
df["PPM"]     = df["Points"] / df["Minutes"]
df["Reb"]     = df["OffReb"] + df["DefReb"]

# ────────── 3) ESTILO GLOBAL ──────────
sns.set(style="whitegrid", font_scale=1.15)
palette = sns.color_palette("Set2", n_colors=3)

# ════════════════════════════════════
# HEATMAP A ▸ Ratios avanzados
# ════════════════════════════════════
ratio_cols = ["PPM", "eFG%", "TS%", "FT Rate"]
fig_a, ax_a = plt.subplots(figsize=(7, 3))
hm_a = sns.heatmap(
    df.iloc[::-1].set_index("Game")[ratio_cols],
    annot=True, cmap="YlOrBr", fmt=".2f",
    linewidths=.4, cbar_kws={"label": "Valor"}, ax=ax_a
)
ax_a.set_title("Ratios (PPM · eFG% · TS% · FT Rate)", pad=25)
ax_a.set_ylabel("Game", labelpad=20)
hm_a.collections[0].colorbar.ax.set_ylabel("Valor", labelpad=30)

# ════════════════════════════════════
# HEATMAP B ▸ Conteo bruto
# ════════════════════════════════════
count_cols = ["Points", "Reb", "Assists", "Steals", "Turnovers"]
fig_b, ax_b = plt.subplots(figsize=(8, 3))
hm_b = sns.heatmap(
    df.iloc[::-1].set_index("Game")[count_cols],
    annot=True, cmap="BuGn", fmt=".0f",
    linewidths=.4, cbar_kws={"label": "Conteo"}, ax=ax_b
)
ax_b.set_title("Conteo (Pts · Reb · AST · STL · TOV)", pad=25)
ax_b.set_ylabel("Game", labelpad=20)
hm_b.collections[0].colorbar.ax.set_ylabel("Conteo", labelpad=30)

# ════════════════════════════════════
# BARRAS AGRUPADAS ▸ Métricas clave
# ════════════════════════════════════
keys   = ["PPM", "eFG%", "TS%", "FT Rate"]
labels = ["PPM (Pts/min)", "eFG% (Tiro efectivo)",
          "TS% (Tiro real)", "FT Rate (TL/Tiro)"]

x_pos = range(len(keys))
bar_w = 0.25

fig_bar, ax_bar = plt.subplots(figsize=(10, 5))
for idx, row in df.iterrows():
    offs  = [-bar_w, 0, bar_w][idx]
    bar_x = [x + offs for x in x_pos]

    ax_bar.bar(bar_x, [row[k] for k in keys],
               width=bar_w, color=palette[idx], label=row["Game"])

    for j, k in enumerate(keys):
        ax_bar.text(bar_x[j],
                    row[k] + 0.02,
                    f"{row[k]:.2f}",
                    ha="center", va="bottom", fontsize=8)

ax_bar.set_xticks(x_pos)
ax_bar.set_xticklabels(labels)
ax_bar.set_ylabel("Valor", labelpad=15)
ax_bar.set_title("Comparativa de métricas avanzadas", fontsize=13, pad=25)
ax_bar.legend(title="Partido")

# ════════════════════════════════════
# SCATTER ▸ TS % vs PPM (burbujas XL)
# ════════════════════════════════════
fig_scat, ax_scat = plt.subplots(figsize=(6, 6))

bubble_sizes = df["PPM"] * 2100
ax_scat.scatter(df["TS%"], df["PPM"],
                s=bubble_sizes, c=palette, edgecolor="black", alpha=0.85)

for _, r in df.iterrows():
    ax_scat.text(r["TS%"], r["PPM"], f"{r['TS%']:.2f}",
                 ha="center", va="center",
                 color="white", fontweight="bold", fontsize=9)

handles = [mpatches.Patch(color=palette[i], label=df.loc[i, "Game"])
           for i in range(3)]
ax_scat.legend(handles=handles, title="Partido", loc="upper left")

ax_scat.set_title("Eficiencia (TS%) vs Producción (PPM)", pad=25)
ax_scat.set_xlabel("True Shooting % (0–1)", labelpad=15)
ax_scat.set_ylabel("Puntos por minuto", labelpad=15)
ax_scat.grid(True, linestyle="--", alpha=0.3)

# ════════════════════════════════════
# STREAMLIT APP
# ════════════════════════════════════
st.set_page_config(page_title="Jean Montero Dashboard", layout="wide")

st.title("📊 Jean Montero – Final ACB 2025")

st.markdown("### 🔥 Heatmap: Ratios avanzados")
st.pyplot(fig_a)

st.markdown("### 📆 Heatmap: Conteo bruto")
st.pyplot(fig_b)

st.markdown("### 📊 Comparativa de métricas avanzadas")
st.pyplot(fig_bar)

st.markdown("### 🔸 Eficiencia de tiro vs Producción")
st.pyplot(fig_scat)
