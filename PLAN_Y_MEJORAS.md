# Plan de trabajo y mejoras propuestas

## Estado contra el cronograma de la consigna (hoy: 10/06)

| Semana | Consigna | Estado |
|---|---|---|
| S1 (05/06) — Setup | Entorno, dataset, ¿qué es churn? | ✅ Hecho (falta: repo GitHub + primer commit) |
| S2 (12/06) — EDA e hipótesis | EDA, 5 hipótesis con gráfico+test, split estratificado | ✅ Hecho — `reports/01_hipotesis.md` + `reports/figuras/` |
| S3 (19/06) — Modelado | Baseline + modelo potente + métricas + decisions.md | ✅ Hecho — `analisis_churn.py` + `decisions.md` |
| S3 — Entrega final | Reporte ejecutivo PDF 4-6 pág. + defensa oral 15' | 🔶 Borrador listo (`REPORTE_EJECUTIVO.md`) — falta pasar a PDF y preparar la defensa |

## Qué falta para entregar (checklist)

1. **Repo GitHub**: `git init`, subir código + reports + decisions.md (la consigna lo pide explícitamente como entregable 01).
2. **Notebook**: pasar `analisis_churn.py` a un notebook `.ipynb` con `df.head()` visible y el EDA narrado (la consigna pide notebook, no script).
3. **Skills**: instalar/documentar uso de `grill-me` y `data-science-kit` en Cursor (la consigna las nombra; al menos dejar constancia de cómo se usaron).
4. **PDF**: exportar `REPORTE_EJECUTIVO.md` a PDF de 4-6 páginas (con las figuras embebidas).
5. **Defensa oral (15')**: guion sugerido — 3' problema y costo del churn · 5' hipótesis (énfasis en H3/H4 refutadas) · 4' modelo y métricas (por qué recall y no accuracy) · 3' acciones y limitaciones. Tener `decisions.md` a mano: está permitido consultarlo.

## Mejoras propuestas (de la versión actual a una versión excelente)

### Sobre los datos
1. **Unificar categorías duplicadas** (`Phone`/`Mobile Phone`, `CC`/`Credit Card`, `COD`/`Cash on Delivery`): limpieza obligatoria antes de producción.
2. **Indicadores de faltantes**: además de imputar por mediana, agregar columna binaria `X_faltante` — el hecho de que falte el dato puede ser señal en sí mismo (33% de filas afectadas).
3. **Pedir fechas en la captura de datos**: única forma de eliminar de raíz el riesgo de leakage temporal de `Complain` y `DaySinceLastOrder`.

### Sobre el modelo
4. **Validación cruzada estratificada (5-fold)** además del hold-out: confirma que el resultado no depende de la suerte del split.
5. **SHAP values** (la consigna los menciona): explicación individual por cliente — "este cliente está en riesgo POR su tenure de 1 mes y su reclamo" — oro para el equipo comercial.
6. **Ajuste del umbral de decisión por costos**: hoy el corte es 0,5; con el costo real de retención vs. pérdida se puede mover el umbral y maximizar el ROI esperado en $ (curva precision-recall).
7. **Probar Gradient Boosting (XGBoost/LightGBM)** como segundo modelo potente, ya que la consigna lo menciona y es el estándar de la industria en churn.
8. **Sospechar del AUC 0,999**: en la defensa, decirlo proactivamente — un resultado tan alto en un dataset académico sugiere señal "demasiado fácil" (posible leakage estructural del snapshot). En producción se esperaría 0,80-0,90.

### Sobre el negocio
9. **Cuantificar el ROI con números reales**: pedir ticket promedio anual y costo de una intervención → convertir la matriz de confusión en $ (hoy el reporte lo deja expresado con $X).
10. **Diseñar el piloto A/B**: lista de riesgo del modelo, mitad con intervención, mitad control, 1 ciclo comercial → mide el ROI causal de la retención (y de paso responde H5 sobre el cashback).
11. **Segmentar las acciones por driver**: no todos los clientes en riesgo se tratan igual — el de tenure bajo recibe onboarding, el que reclamó recibe resolución + compensación, el de cashback bajo entra al A/B.
12. **Monitoreo post-despliegue**: medir recall/precision reales cada mes y reentrenar cuando se degraden (data drift).
