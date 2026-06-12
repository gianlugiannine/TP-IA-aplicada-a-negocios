# decisions.md — Registro de decisiones del proyecto

Formato de cada entrada: **qué decidí · por qué · alternativas descartadas · consecuencias**.
Este archivo es la memoria del proyecto y se puede consultar durante la defensa oral.

---

## D1 — Métrica principal: Recall (con Precision como control)

- **Qué:** optimizar y reportar recall como métrica prioritaria; precision como segunda; accuracy solo como referencia de por qué NO sirve.
- **Por qué:** con 16,8% de churn, "nadie se va" da 83% de accuracy y cero valor. El costo de perder un cliente (5–25x el de retención) supera el de una intervención innecesaria → priorizar no perderse churners.
- **Alternativas descartadas:** accuracy (engañosa con clases desbalanceadas); F1 como única métrica (esconde el trade-off que el gerente necesita ver); precision como prioritaria (solo si el presupuesto de retención fuera el cuello de botella — no es el caso planteado).
- **Consecuencias:** el modelo final se evalúa por "de los que se iban, cuántos detectamos" (96%). Aceptamos 12 falsas alarmas sobre 1.126 clientes.

## D2 — Valores faltantes: imputación por mediana

- **Qué:** 7 columnas numéricas tienen nulos (33% de las filas afectadas). Se imputó con la mediana de cada columna.
- **Por qué:** la mediana es robusta a outliers; eliminar filas perdía un tercio del dataset y podía sesgar (los nulos podrían no ser aleatorios).
- **Alternativas descartadas:** eliminar filas (pérdida masiva de datos); imputar con media (sensible a outliers); imputación por modelo/KNN (complejidad injustificada para el objetivo del TP — primero el baseline simple).
- **Consecuencias:** posible suavizado de patrones extremos. Mejora futura: agregar una columna indicadora "dato_faltante" por variable.

## D3 — Split estratificado 80/20 con random_state=42

- **Qué:** train 4.504 / test 1.126, estratificado por churn.
- **Por qué:** la estratificación mantiene 16,8% de churn en ambos subsets (verificado: 16,8% / 16,9%); random_state fijo hace el trabajo reproducible. Exigido por la consigna.
- **Alternativas descartadas:** split aleatorio sin estratificar (con 16% de positivos, el test podría quedar con una proporción distinta y las métricas no serían comparables); validación cruzada (propuesta como mejora, no reemplaza el hold-out final).
- **Consecuencias:** todas las métricas reportadas son sobre datos que el modelo nunca vio.

## D4 — Baseline doble: "nadie se va" + Regresión Logística

- **Qué:** dos pisos de comparación antes del modelo potente.
- **Por qué:** el dummy demuestra la trampa del accuracy (83% acertando nada); la logística es el modelo simple y explicable que cualquier modelo complejo debe superar para justificarse.
- **Alternativas descartadas:** un solo árbol de decisión como baseline (válido, pero la logística con `class_weight=balanced` da un piso más exigente en recall).
- **Consecuencias:** el Random Forest se justifica: AUC 0,999 vs. 0,886 de la logística, y precision 94% vs. 44%.

## D5 — Modelo potente: Random Forest con class_weight=balanced

- **Qué:** RandomForestClassifier, 300 árboles, class_weight=balanced.
- **Por qué:** maneja no-linealidades (la relación tenure→churn no es lineal), es robusto, da importancia de variables (explicabilidad ante el gerente) y `balanced` compensa el desbalance 84/16 sin inventar datos.
- **Alternativas descartadas:** Gradient Boosting (rendimiento similar esperable, menos directo de explicar; queda como mejora); SMOTE/oversampling (genera clientes sintéticos — difícil de defender ante negocio cuando `class_weight` logra el mismo efecto); red neuronal (caja negra injustificada con datos tabulares).
- **Consecuencias:** recall 0,96, precision 0,94, AUC 0,999 en test.

## D6 — Auditoría de leakage: reentrenar sin `Complain`

- **Qué:** ante la advertencia de la consigna sobre leakage temporal en `Complain`, se entrenó el modelo final con y sin esa variable.
- **Por qué:** el dataset no tiene fechas; no se puede verificar si el reclamo precede al churn. La forma honesta de manejarlo es medir cuánto depende el modelo de la variable sospechosa.
- **Alternativas descartadas:** eliminarla directamente (perdía una señal de negocio real); ignorar el problema (indefendible en la defensa oral).
- **Consecuencias:** sin `Complain`: AUC 0,997 (vs. 0,999), recall 0,93 (vs. 0,96). El modelo no depende de la variable sospechosa; la conclusión de negocio de H2 se mantiene como alerta operativa.

## D7 — `DaySinceLastOrder`: se mantiene, con el riesgo documentado

- **Qué:** la variable resultó tener dirección inversa a la esperada (churners compraron más recientemente) y se mantiene en el modelo.
- **Por qué:** es una señal real para predecir, pero su dirección sugiere que el snapshot del dataset marca el churn poco después de la última compra → posible leakage estructural parecido al de `Complain`.
- **Consecuencias:** la interpretación de negocio de H3 se reformuló ("el gatillo es la experiencia post-compra, no el silencio") y se recomienda capturar fechas en los datos futuros.

## D8 — Inconsistencias de categorías detectadas en el EDA

- **Qué:** el dataset tiene categorías duplicadas: `Phone` vs `Mobile Phone` (PreferredLoginDevice), `CC` vs `Credit Card` y `COD` vs `Cash on Delivery` (PreferredPaymentMode), `Mobile` vs `Mobile Phone` (PreferedOrderCat).
- **Por qué importa:** infla la cardinalidad y reparte la señal de una misma categoría en dos columnas dummy.
- **Decisión:** documentarlo y proponer la unificación como mejora; el impacto en métricas es marginal (el modelo ya satura) pero la limpieza es obligatoria antes de producción.

## D9 — Reporte ejecutivo centrado en las hipótesis refutadas

- **Qué:** H3 y H4 (refutadas) ocupan lugar central en el reporte, no se esconden.
- **Por qué:** evitar inversiones erradas (tablero de satisfacción, monitoreo de inactividad) vale más que confirmar lo obvio. Demuestra que validamos en lugar de asumir — exactamente lo que pide la consigna.
- **Consecuencias:** la recomendación al gerente incluye revisar la encuesta de satisfacción y rediseñar el timing de las intervenciones.
