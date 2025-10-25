# datacat_app.py
import streamlit as st
import pandas as pd
import openai
import os

# --- Configuración inicial ---
st.set_page_config(page_title="🐱 DataCat - Gato Analista de Datos", page_icon="🐾")

openai.api_key = "TU_API_KEY_AQUI"  # Reemplaza con tu clave real

# --- Cargar o crear dataset ---
ruta_csv = os.path.join(os.path.dirname(__file__), "energia.csv")

if not os.path.exists(ruta_csv):
    st.warning("No se encontró 'energia.csv'. Creando un dataset de ejemplo...")
    data = {
        "id": list(range(1, 51)),
        "fecha": pd.date_range(start="2025-01-01", periods=50),
        "energy_kwh": [125 + i * 3 + (i % 5) * 2 for i in range(50)]
    }
    df_temp = pd.DataFrame(data)
    df_temp.to_csv(ruta_csv, index=False)
    st.success("Archivo 'energia.csv' creado automáticamente ✅")

# Cargar el dataset
df = pd.read_csv(ruta_csv)

# --- Interfaz principal ---
st.title("🐱 DataCat - Tu gato analista de datos")
st.markdown("¡Hola humano! 🐾 Puedo ayudarte a explorar tus datos de energía. Pregúntame algo como:")
st.code("¿Cuál es el promedio de consumo?\n¿Y el valor máximo registrado?", language="")

# Entrada del usuario
mensaje = st.text_input("Habla con DataCat:")

if st.button("Enviar") and mensaje.strip() != "":
    # Análisis básico con pandas
    if "promedio" in mensaje.lower():
        promedio = df["energy_kwh"].mean()
        respuesta_datos = f"El consumo promedio es de {promedio:.2f} kWh."
    elif "máximo" in mensaje.lower():
        maximo = df["energy_kwh"].max()
        respuesta_datos = f"El consumo máximo fue de {maximo:.2f} kWh."
    elif "mínimo" in mensaje.lower():
        minimo = df["energy_kwh"].min()
        respuesta_datos = f"El consumo mínimo fue de {minimo:.2f} kWh."
    elif "total" in mensaje.lower():
        total = df["energy_kwh"].sum()
        respuesta_datos = f"El consumo total registrado es de {total:.2f} kWh."
    else:
        respuesta_datos = "Miau... No encontré esa consulta, pero puedo ayudarte a analizar tus datos."

    # --- Generar respuesta natural con IA (opcional) ---
    try:
        prompt = f"""
Eres un gato analista llamado DataCat. Responde con tono curioso y amable.

Usuario: {mensaje}
Datos: {respuesta_datos}

DataCat:
"""
        completion = openai.ChatCompletion.create(
            model="gpt-5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        respuesta_final = completion.choices[0].message.content
    except Exception as e:
        respuesta_final = f"{respuesta_datos}\n\n*(No se pudo conectar con OpenAI: {e})*"

    # Mostrar respuesta del gato
    st.markdown(f"**🐾 DataCat:** {respuesta_final}")

    # Mostrar tabla de ejemplo
    with st.expander("📊 Ver primeros registros del dataset"):
        st.dataframe(df.head())

