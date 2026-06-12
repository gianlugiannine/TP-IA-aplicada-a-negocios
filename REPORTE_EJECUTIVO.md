# Predicción de Churn de Clientes — Reporte Ejecutivo

**Para:** Gerencia Comercial
**Materia:** Inteligencia Artificial Aplicada a Negocios — 1er Cuatrimestre 2026
**Dataset:** 5.630 clientes de e-commerce, 20 variables

---

## 1. El problema en una página

De nuestros **5.630 clientes, 948 (16,8%) dejaron de comprar**. Adquirir un cliente nuevo cuesta entre 5 y 25 veces más que retener uno existente: cada punto de churn que recuperamos va directo a la rentabilidad.

La pregunta que respondimos: **¿podemos saber quién está por irse antes de que se vaya, y por qué?**

La respuesta es sí. Construimos un sistema que, probado sobre 1.126 clientes que nunca había visto, **detectó a 183 de los 190 que efectivamente se fueron (96%)**, con solo 12 falsas alarmas. Esto significa que el equipo comercial puede trabajar con una lista corta y confiable de clientes en riesgo, en lugar de hacer campañas masivas a ciegas.

**Las tres conclusiones más importantes para el negocio:**

1. **El churn es un problema de los primeros 30 días.** Más de la mitad de los clientes con un mes o menos de antigüedad se va. Pasado el año, casi nadie se va.
2. **La encuesta de satisfacción no sirve para anticipar el churn** — los datos muestran lo contrario de lo esperado: los que puntúan 5 se van *más* que los que puntúan 1.
3. **Quien reclama se va casi 3 veces más.** Cada reclamo sin resolver es una alerta roja accionable.

---

## 2. Qué encontramos en los datos (5 hipótesis puestas a prueba)

Antes de construir el modelo planteamos 5 hipótesis de negocio y las validamos con los datos. Dos resultaron **falsas**, y eso vale más que las confirmadas: nos evita gastar plata en acciones que no funcionan.

### ✅ H1 — Los clientes nuevos se van mucho más (CONFIRMADA)

| Antigüedad | Tasa de churn |
|---|---|
| 0–1 mes | **51,8%** |
| 2–6 meses | 8,0% |
| 7–12 meses | 5,7% |
| 13–24 meses | 6,5% |
| Más de 2 años | **0,0%** |

La mitad de los clientes nuevos se va en el primer mes; ningún cliente con más de 2 años se fue. La antigüedad mediana de los que se van es 1 mes, contra 10 meses de los que se quedan (diferencia estadísticamente contundente, p < 0,001).

**Decisión que habilita:** el presupuesto de retención rinde más invertido en *onboarding* (primeros 30–60 días) que repartido en toda la base.

### ✅ H2 — Quien reclama se va casi 3 veces más (CONFIRMADA, con una advertencia)

Churn entre quienes reclamaron: **31,7%**. Entre quienes no: **10,9%**.

*Advertencia metodológica:* no sabemos si el reclamo se registró antes o después de la decisión de irse. Verificamos que el modelo funciona casi igual de bien sin esta variable, así que la conclusión de negocio se sostiene: **un reclamo es una alerta temprana que merece respuesta inmediata**.

### ❌ H3 — "La inactividad anticipa el churn" (REFUTADA)

Esperábamos que los clientes con más días sin comprar estuvieran más cerca de irse. Los datos muestran lo contrario: los que se fueron habían comprado **más recientemente** (mediana 2 días vs. 4 días).

**Lectura de negocio:** muchos clientes hacen una última compra, tienen una mala experiencia y se van enseguida. La señal de riesgo no es el silencio: es **lo que pasa inmediatamente después de una compra** (demora, producto defectuoso, mala atención). La ventana para retener es corta y empieza el día de la compra.

### ❌ H4 — "Baja satisfacción = más churn" (REFUTADA)

La hipótesis más intuitiva resultó falsa:

| Score de satisfacción | Tasa de churn |
|---|---|
| 1 (peor) | 11,5% |
| 3 | 17,2% |
| 5 (mejor) | **23,8%** |

Los clientes que puntúan 5 se van **más del doble** que los que puntúan 1. Posibles explicaciones: la encuesta mide la satisfacción con una compra puntual y no la lealtad; o los clientes ya decididos a irse responden por compromiso.

**Decisión que habilita:** no usar la encuesta de satisfacción como tablero de retención. Hoy nos estaría dando una falsa sensación de seguridad exactamente con los clientes que están por irse.

### ⚠️ H5 — El cashback acompaña la retención, pero no es la causa (MATIZADA)

Los que se quedan reciben más cashback (mediana $166 vs. $150). Pero el cashback crece con la antigüedad, y la antigüedad es el verdadero factor protector: la correlación no prueba que regalar cashback retenga. **Recomendación:** probarlo con un experimento controlado (a un grupo de riesgo se le da cashback extra, a otro no, y se compara) antes de invertir.

---

## 3. El sistema de predicción

Trabajamos en dos etapas, comparando siempre contra un piso:

| Modelo | ¿Detecta a los que se van? (Recall) | ¿Cuántas alarmas son reales? (Precision) | Calidad global (AUC) |
|---|---|---|---|
| Piso: "nadie se va" | 0% | — | 0,50 |
| Modelo simple (Regresión Logística) | 85% | 44% | 0,89 |
| **Modelo final (Random Forest)** | **96%** | **94%** | **0,99** |

Tres aclaraciones en lenguaje claro:

- **Por qué no usamos "accuracy":** como el 83% de los clientes se queda, un modelo inútil que diga "nadie se va" acierta el 83% de las veces. Por eso medimos *de los que se iban, a cuántos detectamos* (recall) y *de los que señalamos, cuántos eran reales* (precision).
- **Por qué priorizamos recall:** perder un cliente cuesta mucho más que llamar de más a uno que no se iba. Preferimos alguna falsa alarma antes que dejar pasar un cliente en riesgo.
- **Qué es el Random Forest:** cientos de "cuestionarios de preguntas sí/no" sobre el cliente que votan en conjunto. Es como consultar a 300 analistas en vez de a uno.

**Qué variables pesan más en la predicción:** la antigüedad explica por lejos la mayor parte (25% de la importancia), seguida por el cashback recibido, los reclamos, la distancia del depósito al domicilio y los días desde la última compra.

**Honestidad sobre los resultados:** un acierto del 96–99% en datos históricos es excelente, pero en el mundo real va a ser menor. El dataset es una foto de un momento; recomendamos un piloto controlado antes de confiar el presupuesto entero al modelo (ver sección 5).

---

## 4. De la predicción a la acción

| Acción | A quién | Por qué (evidencia) |
|---|---|---|
| **Programa de onboarding intensivo** (seguimiento activo los primeros 60 días) | Clientes con < 2 meses | H1: 51,8% de churn en el primer mes |
| **Protocolo de reclamo = alerta roja** (respuesta < 24 hs + compensación) | Cualquier cliente que reclama | H2: el reclamo casi triplica el churn |
| **Encuesta post-compra inmediata sobre la experiencia de entrega** | Compradores recientes | H3: el churn ocurre justo después de una compra |
| **Lista semanal de riesgo generada por el modelo** | Top de probabilidad de churn | El modelo detecta 96 de cada 100 que se van |
| **Experimento A/B de cashback** antes de escalar el beneficio | Muestra del grupo de riesgo | H5: la correlación no prueba causalidad |

**Cuánto está en juego (estimación conservadora):** si el ticket anual promedio de un cliente es $X, los 948 clientes perdidos representan $948·X de facturación anual. Reteniendo solo al 20% de los que el modelo detecta, se recuperan ~180 clientes por ciclo. La bibliografía indica que mejorar 5 puntos la retención puede aumentar las ganancias entre 25% y 95%.

---

## 5. Limitaciones y próximos pasos

**Limitaciones que asumimos abiertamente:**
1. **Foto, no película:** el dataset no tiene fechas; no podemos garantizar que todas las variables se midieron antes del churn (riesgo de "leakage"). Lo mitigamos verificando el modelo sin la variable más sospechosa (reclamos) — sigue funcionando.
2. **Datos faltantes:** un tercio de los clientes tiene algún dato incompleto; los completamos con valores típicos (medianas).
3. **Resultados sobre datos históricos:** el rendimiento real se confirma recién en producción.

**Próximos pasos propuestos:**
1. Piloto de 1 ciclo comercial: el modelo genera la lista de riesgo, el equipo interviene a la mitad (grupo de tratamiento) y a la otra mitad no (control). Se mide el ROI real de la retención.
2. Incorporar fechas a la captura de datos para eliminar el riesgo de leakage.
3. Revisar la encuesta de satisfacción (H4 sugiere que hoy no mide lo que creemos).

---

*Las decisiones técnicas, alternativas evaluadas y descartadas están documentadas en `decisions.md`. Los gráficos de cada hipótesis están en `reports/figuras/`.*
