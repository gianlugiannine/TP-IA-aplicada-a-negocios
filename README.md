# TP IA Aplicada a Negocios — Predicción de Churn de Clientes

Trabajo Práctico para la materia **Inteligencia Artificial Aplicada a Negocios** (1er Cuatrimestre 2026, ITBA).

Sistema de predicción de churn (abandono de clientes) sobre un dataset de **5.630 clientes de e-commerce** con 20 variables. El modelo final (Random Forest) detecta al **96% de los clientes que se van** con solo 12 falsas alarmas sobre 1.126 evaluados.

---

## Resultados principales

| Modelo | Recall | Precision | AUC |
|---|---|---|---|
| Piso ("nadie se va") | 0% | — | 0,50 |
| Regresión Logística | 85% | 44% | 0,89 |
| **Random Forest (final)** | **96%** | **94%** | **0,99** |

### Hallazgos de negocio
- **El churn es un problema de los primeros 30 días:** 51,8% de los clientes con < 1 mes se va.
- **Quien reclama se va casi 3 veces más** (31,7% vs. 10,9%).
- **La encuesta de satisfacción no anticipa el churn** — los que puntúan 5 se van más que los que puntúan 1.

---

## Estructura del repositorio

```
├── analisis_churn.py                 # Pipeline completo (EDA + modelos)
├── generar_figuras.py                # Genera los gráficos de las hipótesis
├── E Commerce Dataset.xlsx - E Comm.csv   # Dataset (5.630 clientes)
├── REPORTE_EJECUTIVO.md/.html/.pdf   # Reporte ejecutivo para gerencia
├── PLAN_Y_MEJORAS.md                 # Plan de trabajo y mejoras
├── decisions.md                      # Decisiones técnicas y alternativas evaluadas
└── reports/
    ├── 01_hipotesis.md               # Detalle de las 5 hipótesis
    └── figuras/                      # Gráficos h1–h5 + comparación de modelos
```

---

## Cómo correrlo

```bash
# 1. Crear y activar entorno virtual
python3 -m venv venv
source venv/bin/activate

# 2. Instalar dependencias
pip install pandas numpy scikit-learn matplotlib seaborn openpyxl

# 3. Ejecutar el análisis
python analisis_churn.py

# 4. (Opcional) Regenerar las figuras
python generar_figuras.py
```

---

## Documentos clave

- **[REPORTE_EJECUTIVO.md](REPORTE_EJECUTIVO.md)** — Lectura recomendada. Resumen para gerencia comercial con hipótesis, métricas y acciones.
- **[decisions.md](decisions.md)** — Decisiones técnicas (por qué Random Forest, por qué recall sobre accuracy, manejo de leakage, etc.).
- **[reports/01_hipotesis.md](reports/01_hipotesis.md)** — Las 5 hipótesis de negocio puestas a prueba.

---

## Autor

Gianluca Gianninelizarraga — ITBA
