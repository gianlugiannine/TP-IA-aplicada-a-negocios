# 5 Hipótesis de Negocio — Validación con Datos

Dataset: 5.630 clientes, churn global **16,84%** (948 clientes).
Método exigido por la consigna: cada hipótesis lleva **1 gráfico + 1 test estadístico + interpretación de negocio**.
Figuras en `figuras/`.

---

## H1 — Tenure bajo = mayor riesgo ✅ CONFIRMADA

**Hipótesis:** los clientes nuevos churnean más; no hay lealtad ni costos de cambio.

**Evidencia:**
- Churn por antigüedad: 0–1 mes **51,8%** · 2–6 m 8,0% · 7–12 m 5,7% · 13–24 m 6,5% · 25+ m **0,0%**.
- Mediana de tenure: churners 1 mes vs. retenidos 10 meses.
- Test: Mann-Whitney U, **p = 5,7e-193** → diferencia altamente significativa.
- Gráfico: `figuras/h1_tenure.png`

**Interpretación de negocio:** el churn es esencialmente un problema de onboarding. El presupuesto de retención debe concentrarse en los primeros 60 días.

---

## H2 — Quejas aumentan el churn ✅ CONFIRMADA (con riesgo de leakage documentado)

**Hipótesis:** quien reclamó (Complain=1) churnea más.

**Evidencia:**
- Churn con reclamo **31,7%** vs. sin reclamo **10,9%** (≈ 2,9x).
- Test: chi-cuadrado de independencia, **p = 2,7e-78**.
- Gráfico: `figuras/h2_complain.png`

**Riesgo de leakage temporal:** el dataset no tiene fechas; no sabemos si el reclamo es anterior o posterior a la decisión de irse. Mitigación: entrenamos el modelo final con y sin `Complain` — el AUC pasa de 0,999 a 0,997 y el recall de 0,96 a 0,93. La capacidad predictiva NO depende de esta variable.

**Interpretación de negocio:** tratar cada reclamo como alerta temprana con protocolo de respuesta < 24 hs.

---

## H3 — La inactividad predice el churn ❌ REFUTADA (dirección opuesta)

**Hipótesis:** más días sin comprar (DaySinceLastOrder alto) = más cerca de irse.

**Evidencia:**
- Mediana de días desde la última compra: churners **2 días** vs. retenidos **4 días**. Media: 3,2 vs. 4,8.
- Test: Mann-Whitney U, **p = 3,0e-42** — significativo, pero en la dirección CONTRARIA a la hipótesis.
- Gráfico: `figuras/h3_dias_ultima_compra.png`

**Interpretación de negocio:** el cliente que churnea hace una última compra y se va inmediatamente después — patrón compatible con una mala experiencia de entrega/producto como gatillo. La ventana de retención se abre el día de la compra, no tras semanas de silencio. (También puede reflejar cómo se construyó el snapshot del dataset: el flag de churn se asigna poco después de la última orden.)

---

## H4 — Baja satisfacción = más churn ❌ REFUTADA (dirección opuesta)

**Hipótesis:** menor SatisfactionScore → mayor probabilidad de churn. "La más intuitiva."

**Evidencia:**
- Churn por score: 1→11,5% · 2→12,6% · 3→17,2% · 4→17,1% · 5→**23,8%**.
- Test: chi-cuadrado, **p = 2,4e-14** — la relación existe, pero es CRECIENTE.
- Gráfico: `figuras/h4_satisfaccion.png`

**Interpretación de negocio:** la encuesta de satisfacción no mide lealtad; puntuar alto no protege. Usarla como tablero de retención daría falsa seguridad justo con los clientes que se van. Hipótesis explicativas a investigar: (a) mide satisfacción transaccional de una compra puntual, (b) sesgo de respuesta de clientes ya decididos a irse, (c) escala mal diseñada.

---

## H5 — El cashback no garantiza retención ⚠️ MATIZADA

**Hipótesis:** el cashback no retiene si el cliente ya decidió irse.

**Evidencia:**
- Mediana de cashback: churners **$150** vs. retenidos **$166**.
- Test: Mann-Whitney U, **p = 2,2e-38** → los retenidos reciben significativamente más.
- Gráfico: `figuras/h5_cashback.png`

**Interpretación de negocio:** hay asociación entre más cashback y quedarse, pero está confundida con la antigüedad (los clientes viejos acumulan más cashback y además no se van — H1). Correlación ≠ causalidad: no se puede concluir que aumentar el cashback retenga. Recomendación: experimento A/B sobre el segmento de riesgo antes de invertir en el beneficio.

---

## Resumen

| Hipótesis | Resultado | Test | p-valor |
|---|---|---|---|
| H1 Tenure bajo → churn | ✅ Confirmada | Mann-Whitney | 5,7e-193 |
| H2 Reclamos → churn | ✅ Confirmada (⚠ leakage) | Chi-cuadrado | 2,7e-78 |
| H3 Inactividad → churn | ❌ Refutada (inversa) | Mann-Whitney | 3,0e-42 |
| H4 Baja satisfacción → churn | ❌ Refutada (inversa) | Chi-cuadrado | 2,4e-14 |
| H5 Cashback no retiene | ⚠ Matizada (confundida con tenure) | Mann-Whitney | 2,2e-38 |

Dos hipótesis refutadas no son un fracaso del análisis: son su mayor valor. Evitan invertir en monitoreo de inactividad y en el tablero de satisfacción, que los datos muestran como señales engañosas.
