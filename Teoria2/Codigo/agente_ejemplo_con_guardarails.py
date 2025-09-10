import os
import html
from dotenv import load_dotenv
from guardrails import Guard, OnFailAction
from guardrails.hub import ValidJson, RegexMatch
from langchain_openai import ChatOpenAI
from langchain_google_community import GoogleSearchAPIWrapper

# Cargar claves desde el archivo .env
load_dotenv(dotenv_path=r".env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

# Verificar que las claves estén presentes
if not OPENAI_API_KEY:
    raise ValueError("Falta OPENAI_API_KEY en el archivo .env.txt")
if not GOOGLE_API_KEY or not GOOGLE_CSE_ID:
    raise ValueError("Faltan GOOGLE_API_KEY o GOOGLE_CSE_ID en el archivo .env.txt")

# Definición de esquema JSON para validar la salida
OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "valida": {"type": "boolean"},
        "ciudad": {"type": ["string", "null"]},
        "pais": {"type": ["string", "null"]},
        "poblacion": {"type": ["number", "null"], "minimum": 0, "maximum": 1000000000},
        "notas": {"type": "string", "maxLength": 80}
    },
    "required": ["valida", "ciudad", "pais", "poblacion", "notas"],
    "additionalProperties": False
}

# Guardrails con validadores
output_guard = Guard.for_string(
    validators=[
        ValidJson(schema=OUTPUT_SCHEMA, on_fail=OnFailAction.EXCEPTION),
        RegexMatch(
            regex=r"^(?![\s\S]*```)(?![\s\S]*\b(System:|User:|Assistant:)\b)[\s\S]*$",
            on_fail=OnFailAction.EXCEPTION,
        ),
    ]
)

# Inicializar modelo de lenguaje con OpenAI
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=OPENAI_API_KEY)

# Inicializar wrapper de búsqueda de Google
search_wrapper = GoogleSearchAPIWrapper(
    google_api_key=GOOGLE_API_KEY,
    google_cse_id=GOOGLE_CSE_ID
)

# Pequeño ejemplo de sanitización
def sanitize_web_result(text: str, max_len: int = 500) -> str:
    """Escapa HTML y recorta longitud para evitar inyecciones básicas."""
    safe = html.escape(text)           # evita que entren tags/script
    safe = safe.replace("```", "")     # quita code fences
    safe = safe.replace("System:", "").replace("User:", "").replace("Assistant:", "")
    return safe[:max_len]

# Flujo de trabajo del agente
def ejecutar_agente(query: str):
    print("Consulta a Google:", query)
    search_results = search_wrapper.results(query, num_results=1)
    print("Resultados crudos de Google:", search_results)

    snippet = search_results[0].get("snippet", "") if search_results else ""
    sanitized = sanitize_web_result(snippet)

    # Prompt que se envía al modelo de lenguaje
    prompt = f"""
    Basado en la información disponible, devuelve un JSON con:
    - valida: booleano
    - ciudad: string o null
    - pais: string o null
    - poblacion: número mayor o igual a 0
    - notas: resumen en menos de 80 caracteres

    Informacion:
    UNTRUSTED CONTEXT START
    {sanitized}
    UNTRUSTED CONTEXT END
    """
    raw_output = llm.invoke(prompt).content

    try:
        validated_output, validation_result = output_guard.parse(raw_output)
        print("Salida validada:", validated_output)
        return validated_output
    except Exception as e:
        print("Error en validación:", e)
        print("Salida cruda del modelo:", raw_output)
        return None

# Ejecución principal
if __name__ == "__main__":
    ejecutar_agente("Buenos Aires population and country")
