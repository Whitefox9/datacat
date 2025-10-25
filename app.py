# datacat_app.py
import pandas as pd
import openai

# Cargar dataset de ejemplo
df = pd.read_csv("energia.csv")

@app.route("/datacat", methods=["POST"])
def datacat_chat():
    user_message = request.json["message"]

    # Ejemplo: interpretar el mensaje y ejecutar análisis
    if "promedio" in user_message.lower():
        promedio = df["energy_kwh"].mean()
        respuesta_datos = f"El promedio de consumo es {promedio:.2f} kWh."
    elif "máximo" in user_message.lower():
        maximo = df["energy_kwh"].max()
        respuesta_datos = f"El máximo consumo fue {maximo:.2f} kWh."
    else:
        respuesta_datos = "No encontré esa consulta, pero puedo ayudarte a analizar los datos."

    # Generar respuesta natural con IA
    prompt = f"Eres un gato analista llamado DataCat. Responde con tono curioso y amable.\n\nUsuario: {user_message}\nDatos: {respuesta_datos}\nDataCat:"
    completion = openai.ChatCompletion.create(
        model="gpt-5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    return jsonify({"reply": completion.choices[0].message.content})


