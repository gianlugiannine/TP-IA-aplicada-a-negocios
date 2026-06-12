# TP IA Aplicada a Negocios — Predicción de Churn

**Materia:** Inteligencia Artificial Aplicada a Negocios (ITBA, 1er Cuatrimestre 2026)
**Grupo 3**

Este repositorio contiene el **avance del trabajo práctico** sobre predicción de churn (fuga de clientes) en una empresa de e-commerce.

---

## El problema

La empresa tiene **5.630 clientes**, de los cuales **948 (16,8%) dejaron de comprar**. Conseguir un cliente nuevo cuesta entre 5 y 25 veces más que retener uno existente, por lo que anticipar quién está por irse tiene impacto directo en la rentabilidad.

**Pregunta del TP:** ¿podemos predecir, con los datos disponibles, qué clientes están por abandonar la empresa?

---

## Avance realizado hasta el momento

1. **Exploración del dataset** (5.630 clientes, 20 variables: antigüedad, reclamos, satisfacción, cashback, etc.).
2. **Limpieza de datos:** tratamiento de valores faltantes (un tercio del dataset tenía algún dato incompleto).
3. **Planteo y prueba de 5 hipótesis de negocio** sobre las posibles causas del churn (2 resultaron refutadas — ver `reports/01_hipotesis.md`).
4. **Entrenamiento y comparación de dos modelos** (Regresión Logística y Random Forest) contra un piso de referencia.
5. **Evaluación sobre datos que el modelo nunca vio** (1.126 clientes de prueba).
6. **Documentación de decisiones técnicas** y elaboración de un reporte ejecutivo.

---

## Resultados preliminares

El modelo final (Random Forest) detectó **96 de cada 100 clientes que efectivamente se iban**, con 12 falsas alarmas sobre 1.126 evaluados.

### Hallazgos principales
- **El primer mes es crítico:** 51,8% de los clientes con menos de 30 días se va.
- **Un reclamo es alerta roja:** quien reclama se va casi 3 veces más.
- **La encuesta de satisfacción no anticipa el churn:** los que puntúan 5 (el máximo) se van más que los que puntúan 1.

---

## Estructura del repositorio

```
├── analisis_churn.py            ← Script principal (análisis + modelos)
├── generar_figuras.py           ← Genera los gráficos
├── E Commerce Dataset...csv     ← Datos crudos
│
├── REPORTE_EJECUTIVO.md/.pdf    ← Reporte ejecutivo (lectura recomendada)
├── PLAN_Y_MEJORAS.md            ← Estado del trabajo y próximos pasos
├── decisions.md                 ← Justificación de cada decisión técnica
│
└── reports/
    ├── 01_hipotesis.md          ← Las 5 hipótesis puestas a prueba
    └── figuras/                 ← Gráficos generados
```

**Para revisar el avance:** sugerimos empezar por `REPORTE_EJECUTIVO.md`.

---

## Cómo reproducir el análisis

```bash
# 1. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# 2. Instalar dependencias
pip install pandas numpy scikit-learn matplotlib seaborn openpyxl

# 3. Ejecutar
python analisis_churn.py
```

---

## Próximos pasos

- Validar el modelo con un experimento piloto sobre un ciclo comercial.
- Eliminar el riesgo de *data leakage* incorporando fechas a la captura de datos.
- Revisar el diseño de la encuesta de satisfacción (a la luz del hallazgo de H4).

---

## Glosario

- **Churn:** abandono o fuga de un cliente.
- **Modelo:** programa que aprende patrones a partir de ejemplos pasados.
- **Random Forest:** modelo de ensamble que combina cientos de árboles de decisión.
- **Recall (96%):** de los clientes que realmente se fueron, qué porcentaje detectamos.
- **Precision (94%):** de los clientes que el modelo marcó como en riesgo, qué porcentaje se fue de verdad.
