{% if cookiecutter.interface == "fastapi" %}
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello from FastAPI agent!"}
{% elif cookiecutter.interface == "streamlit" %}
import streamlit as st

st.title("Agente LLM")
st.write("¡Hola desde Streamlit!")
{% else %}
print("Interfaz no definida")
{% endif %}
