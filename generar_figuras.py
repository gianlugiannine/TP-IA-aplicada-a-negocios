# Genera las figuras de validación de hipótesis (reports/figuras/)
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

CSV = "/Users/gianlucagianninelizarraga/Desktop/TP IA aplicada a negicios/E Commerce Dataset.xlsx - E Comm.csv"
OUT = "/Users/gianlucagianninelizarraga/Desktop/TP IA aplicada a negicios/reports/figuras"
os.makedirs(OUT, exist_ok=True)
df = pd.read_csv(CSV)
plt.rcParams.update({"figure.dpi": 150, "axes.grid": True, "grid.alpha": 0.3})

def guardar(fig, nombre):
    fig.tight_layout()
    fig.savefig(f"{OUT}/{nombre}.png", bbox_inches="tight")
    plt.close(fig)
    print("OK", nombre)

# H1 — churn por antigüedad
bins = pd.cut(df.Tenure, [-1, 1, 6, 12, 24, 70], labels=["0-1", "2-6", "7-12", "13-24", "25+"])
r = df.groupby(bins, observed=True).Churn.mean() * 100
fig, ax = plt.subplots(figsize=(7, 4))
r.plot(kind="bar", ax=ax, color=["#c0392b", "#e67e22", "#f1c40f", "#27ae60", "#2980b9"], rot=0)
ax.axhline(df.Churn.mean() * 100, ls="--", color="gray", label=f"Promedio {df.Churn.mean()*100:.1f}%")
ax.set_xlabel("Antigüedad como cliente (meses)"); ax.set_ylabel("Tasa de churn (%)")
ax.set_title("H1 — Los clientes nuevos se van mucho más (CONFIRMADA)")
for i, v in enumerate(r): ax.text(i, v + 1, f"{v:.1f}%", ha="center", fontweight="bold")
ax.legend(); guardar(fig, "h1_tenure")

# H2 — churn según queja
r = df.groupby("Complain").Churn.mean() * 100
fig, ax = plt.subplots(figsize=(6, 4))
ax.bar(["No reclamó", "Reclamó"], r.values, color=["#2980b9", "#c0392b"])
for i, v in enumerate(r.values): ax.text(i, v + 0.8, f"{v:.1f}%", ha="center", fontweight="bold")
ax.set_ylabel("Tasa de churn (%)")
ax.set_title("H2 — Quien reclama churnea casi 3x más (CONFIRMADA, ojo leakage)")
guardar(fig, "h2_complain")

# H3 — días desde última compra
b3 = pd.cut(df.DaySinceLastOrder, [-1, 1, 3, 7, 15, 50], labels=["0-1", "2-3", "4-7", "8-15", "16+"])
r = df.groupby(b3, observed=True).Churn.mean() * 100
fig, ax = plt.subplots(figsize=(7, 4))
r.plot(kind="bar", ax=ax, color="#8e44ad", rot=0)
ax.axhline(df.Churn.mean() * 100, ls="--", color="gray", label=f"Promedio {df.Churn.mean()*100:.1f}%")
for i, v in enumerate(r): ax.text(i, v + 0.6, f"{v:.1f}%", ha="center", fontweight="bold")
ax.set_xlabel("Días desde la última compra"); ax.set_ylabel("Tasa de churn (%)")
ax.set_title("H3 — REFUTADA: los churners compraron MÁS recientemente")
ax.legend(); guardar(fig, "h3_dias_ultima_compra")

# H4 — churn por score de satisfacción
r = df.groupby("SatisfactionScore").Churn.mean() * 100
fig, ax = plt.subplots(figsize=(7, 4))
r.plot(kind="bar", ax=ax, color=["#2980b9", "#27ae60", "#f1c40f", "#e67e22", "#c0392b"], rot=0)
for i, v in enumerate(r): ax.text(i, v + 0.5, f"{v:.1f}%", ha="center", fontweight="bold")
ax.set_xlabel("Score de satisfacción (1=peor, 5=mejor)"); ax.set_ylabel("Tasa de churn (%)")
ax.set_title("H4 — REFUTADA: el churn SUBE con la satisfacción declarada")
guardar(fig, "h4_satisfaccion")

# H5 — cashback por grupo
fig, ax = plt.subplots(figsize=(7, 4))
datos = [df.loc[df.Churn == 0, "CashbackAmount"].dropna(), df.loc[df.Churn == 1, "CashbackAmount"].dropna()]
bp = ax.boxplot(datos, tick_labels=["Se queda", "Se va"], patch_artist=True, showfliers=False)
for patch, c in zip(bp["boxes"], ["#2980b9", "#c0392b"]): patch.set_facecolor(c)
ax.set_ylabel("Cashback recibido ($)")
ax.set_title("H5 — Los que se van reciben menos cashback (mediana $150 vs $166)")
guardar(fig, "h5_cashback")

# Comparación de modelos
fig, ax = plt.subplots(figsize=(8, 4))
metricas = {"Recall": [0.0, 0.847, 0.963], "Precision": [0.0, 0.441, 0.938], "AUC-ROC": [0.5, 0.886, 0.999]}
x = np.arange(3); w = 0.25
for i, (m, vals) in enumerate(metricas.items()):
    ax.bar(x + i * w, vals, w, label=m)
ax.set_xticks(x + w); ax.set_xticklabels(['Baseline\n"nadie se va"', "Regresión\nLogística", "Random\nForest"])
ax.set_ylim(0, 1.1); ax.legend(); ax.set_title("Comparación de modelos (test, 1.126 clientes)")
guardar(fig, "modelos_comparacion")
