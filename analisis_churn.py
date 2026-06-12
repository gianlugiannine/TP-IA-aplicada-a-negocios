# Análisis de churn — TP IA Aplicada a Negocios
# EDA + validación de 5 hipótesis + baseline + Random Forest
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (recall_score, precision_score, f1_score,
                             roc_auc_score, confusion_matrix, accuracy_score)

pd.set_option("display.width", 200)
CSV = "/Users/gianlucagianninelizarraga/Desktop/TP IA aplicada a negicios/E Commerce Dataset.xlsx - E Comm.csv"
df = pd.read_csv(CSV)

print("=" * 70)
print("1. PERFILADO DEL DATASET")
print("=" * 70)
print(f"Filas: {len(df)} | Columnas: {len(df.columns)}")
print(f"Tasa de churn: {df.Churn.mean():.2%}  ({df.Churn.sum()} de {len(df)})")
print("\nNulos por columna (solo las que tienen):")
nulls = df.isnull().sum()
print(nulls[nulls > 0].to_string())
print(f"\nTotal filas con algún nulo: {df.isnull().any(axis=1).sum()} ({df.isnull().any(axis=1).mean():.1%})")
print("\nDuplicados de CustomerID:", df.CustomerID.duplicated().sum())

print("\nCategóricas y sus valores:")
for c in df.select_dtypes(include="object").columns:
    print(f"  {c}: {sorted(df[c].unique())}")

print("\n" + "=" * 70)
print("2. VALIDACIÓN DE HIPÓTESIS")
print("=" * 70)

# H1: Tenure bajo = mayor churn (Mann-Whitney: tenure de churners vs no churners)
t_churn = df.loc[df.Churn == 1, "Tenure"].dropna()
t_stay = df.loc[df.Churn == 0, "Tenure"].dropna()
u, p = stats.mannwhitneyu(t_churn, t_stay)
print(f"\nH1 Tenure: mediana churners={t_churn.median():.0f}m vs retenidos={t_stay.median():.0f}m | Mann-Whitney p={p:.2e}")
bins = pd.cut(df.Tenure, [-1, 1, 6, 12, 24, 70], labels=["0-1m", "2-6m", "7-12m", "13-24m", "25m+"])
print(df.groupby(bins, observed=True).Churn.agg(["mean", "count"]).rename(columns={"mean": "churn_rate"}).to_string())

# H2: Complain
ct = pd.crosstab(df.Complain, df.Churn)
chi2, p2, _, _ = stats.chi2_contingency(ct)
r_complain = df.groupby("Complain").Churn.mean()
print(f"\nH2 Complain: churn sin queja={r_complain[0]:.1%} | con queja={r_complain[1]:.1%} | chi2 p={p2:.2e}")

# H3: DaySinceLastOrder
d_churn = df.loc[df.Churn == 1, "DaySinceLastOrder"].dropna()
d_stay = df.loc[df.Churn == 0, "DaySinceLastOrder"].dropna()
u3, p3 = stats.mannwhitneyu(d_churn, d_stay)
print(f"\nH3 DaySinceLastOrder: mediana churners={d_churn.median():.0f}d vs retenidos={d_stay.median():.0f}d | Mann-Whitney p={p3:.2e}")
print(f"   media churners={d_churn.mean():.1f}d vs retenidos={d_stay.mean():.1f}d  <-- ojo con la dirección")

# H4: SatisfactionScore
ct4 = pd.crosstab(df.SatisfactionScore, df.Churn)
chi24, p4, _, _ = stats.chi2_contingency(ct4)
print(f"\nH4 SatisfactionScore (churn por score) | chi2 p={p4:.2e}")
print(df.groupby("SatisfactionScore").Churn.agg(["mean", "count"]).rename(columns={"mean": "churn_rate"}).to_string())

# H5: Cashback
c_churn = df.loc[df.Churn == 1, "CashbackAmount"].dropna()
c_stay = df.loc[df.Churn == 0, "CashbackAmount"].dropna()
u5, p5 = stats.mannwhitneyu(c_churn, c_stay)
print(f"\nH5 Cashback: mediana churners=${c_churn.median():.0f} vs retenidos=${c_stay.median():.0f} | Mann-Whitney p={p5:.2e}")

print("\n" + "=" * 70)
print("3. MODELADO")
print("=" * 70)

data = df.drop(columns=["CustomerID"])
# Imputación simple: mediana (numéricas). Decisión documentada en decisions.md
for c in data.select_dtypes(include=[np.number]).columns:
    data[c] = data[c].fillna(data[c].median())
data = pd.get_dummies(data, drop_first=True)

X = data.drop(columns=["Churn"])
y = data["Churn"]
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
print(f"Train: {len(X_tr)} ({y_tr.mean():.1%} churn) | Test: {len(X_te)} ({y_te.mean():.1%} churn)")

def evaluar(nombre, modelo, con_complain=True):
    cols = X_tr.columns if con_complain else [c for c in X_tr.columns if c != "Complain"]
    modelo.fit(X_tr[cols], y_tr)
    pred = modelo.predict(X_te[cols])
    proba = modelo.predict_proba(X_te[cols])[:, 1] if hasattr(modelo, "predict_proba") else pred
    tn, fp, fn, tp = confusion_matrix(y_te, pred).ravel()
    print(f"\n{nombre}")
    print(f"  Accuracy={accuracy_score(y_te, pred):.3f} | Recall={recall_score(y_te, pred, zero_division=0):.3f} | "
          f"Precision={precision_score(y_te, pred, zero_division=0):.3f} | F1={f1_score(y_te, pred, zero_division=0):.3f} | "
          f"AUC={roc_auc_score(y_te, proba):.3f}")
    print(f"  Confusión: TP={tp} FN={fn} FP={fp} TN={tn}")
    return modelo

evaluar('Baseline "nadie se va" (DummyClassifier)', DummyClassifier(strategy="most_frequent"))
evaluar("Baseline Regresión Logística", LogisticRegression(max_iter=2000, class_weight="balanced"))
rf = evaluar("Random Forest (class_weight=balanced)", RandomForestClassifier(
    n_estimators=300, random_state=42, class_weight="balanced", n_jobs=-1))
evaluar("Random Forest SIN Complain (chequeo leakage)", RandomForestClassifier(
    n_estimators=300, random_state=42, class_weight="balanced", n_jobs=-1), con_complain=False)

print("\nTop 10 variables más importantes (Random Forest):")
imp = pd.Series(rf.feature_importances_, index=X.columns).sort_values(ascending=False)
print(imp.head(10).to_string())
