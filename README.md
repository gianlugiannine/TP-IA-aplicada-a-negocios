# TP IA Aplicada a Negocios — Predicción de Churn

Trabajo Práctico para **Inteligencia Artificial Aplicada a Negocios** (ITBA, 1er Cuatrimestre 2026).

---

## ¿De qué se trata?

Una empresa de e-commerce tiene **5.630 clientes**. De ellos, **948 dejaron de comprar** (el 16,8%). A eso se le llama **churn** (fuga de clientes).

Conseguir un cliente nuevo cuesta entre 5 y 25 veces más que mantener uno que ya compra. Por eso vale la pena anticiparse: si sabemos **quién está por irse antes de que se vaya**, el equipo comercial puede llamarlo, ofrecerle algo, y retenerlo.

Este proyecto construye un sistema que hace justo eso.

---

## ¿Qué hicimos, en palabras simples?

1. **Miramos los datos** de los 5.630 clientes (antigüedad, reclamos, satisfacción, etc.).
2. **Probamos 5 ideas** sobre por qué se va la gente (algunas resultaron ciertas, otras falsas).
3. **Entrenamos un programa** que aprende a reconocer a los clientes que están por irse.
4. **Lo evaluamos** con clientes que el programa nunca había visto, para ver si acertaba.

---

## Resultados

El sistema final acertó **96 de cada 100 clientes** que efectivamente se iban, con apenas 12 falsas alarmas sobre 1.126 personas evaluadas.

### Lo más importante que descubrimos
- **El primer mes es crítico:** más de la mitad de los clientes nuevos (51,8%) se va antes de cumplir 30 días.
- **Un reclamo es una alerta roja:** quien reclama se va casi 3 veces más que quien no.
- **La encuesta de satisfacción engaña:** los clientes que puntúan 5 (el máximo) se van *más* que los que puntúan 1. No sirve para predecir churn.

---

## ¿Cómo está organizada la carpeta?

```
├── analisis_churn.py            ← Script principal (analiza los datos y entrena el modelo)
├── generar_figuras.py           ← Genera los gráficos
├── E Commerce Dataset...csv     ← Los datos de los 5.630 clientes
│
├── REPORTE_EJECUTIVO.md/.pdf    ← Reporte para leer (versión gerencial)
├── PLAN_Y_MEJORAS.md            ← Qué se hizo y qué se podría mejorar
├── decisions.md                 ← Por qué tomamos cada decisión técnica
│
└── reports/
    ├── 01_hipotesis.md          ← Las 5 ideas que pusimos a prueba
    └── figuras/                 ← Gráficos en .png
```

**¿Por dónde empezar?** Por `REPORTE_EJECUTIVO.md` — está escrito para que lo entienda cualquiera.

---

## ¿Cómo correrlo?

Necesitás Python 3 instalado. Después, abrí una terminal en esta carpeta y corré:

```bash
# 1. Crear un "ambiente" aislado para no mezclar librerías
python3 -m venv venv
source venv/bin/activate

# 2. Instalar las librerías necesarias
pip install pandas numpy scikit-learn matplotlib seaborn openpyxl

# 3. Correr el análisis
python analisis_churn.py
```

El script imprime los resultados en pantalla y deja los gráficos en `reports/figuras/`.

---

## Glosario rápido

- **Churn:** que un cliente deje de comprar.
- **Modelo:** un programa que aprende patrones a partir de ejemplos pasados.
- **Random Forest:** el tipo de modelo que usamos. Funciona como si consultáramos a cientos de analistas a la vez y juntáramos sus opiniones.
- **Recall (96%):** de cada 100 clientes que realmente se iban, detectamos 96.
- **Precision (94%):** de cada 100 que el modelo marcó como "en riesgo", 94 efectivamente se iban.

---

**Autor:** Gianluca Gianninelizarraga — ITBA
