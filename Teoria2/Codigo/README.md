```markdown
# Ejemplo básico con Guardrails-AI

Este es un ejemplo **básico y didáctico** que incluye el uso de la librería **guardrails-ai**.  
El objetivo es mostrar de forma clara cómo integrar sanitización de entradas, un modelo de lenguaje y validación de salidas con Guardrails.  

Para configurar la librería, revise las siguientes páginas oficiales:

- [Getting Started – Guardrails Server](https://www.guardrailsai.com/docs/getting_started/guardrails_server)  
- [Guardrails Hub](https://hub.guardrailsai.com/)

> También se puede sustituir la librería por scripts propios, pero aquí se usa Guardrails para simplificar.

---

## Configuración de claves (API Keys)

El ejemplo requiere un archivo `.env` con las siguientes claves:

- **OPENAI_API_KEY** → usada para conectarse al modelo de lenguaje (ejemplo: `gpt-4o-mini`).  
- **GOOGLE_API_KEY** y **GOOGLE_CSE_ID** → necesarias para realizar búsquedas a través de la API oficial de Google.  
- **Guardrails** → se integra mediante `configure` o con constructores como `Guard.for_string(...)`.  
  Se recomienda revisar la documentación oficial para entender cómo definir validaciones y esquemas personalizados.

Todas las claves son cargadas con la librería `python-dotenv`.

---

## ¿Qué hace el código?

1. **Carga las claves** desde `.env` y valida que estén presentes.  
2. **Realiza una búsqueda en Google** usando `GoogleSearchAPIWrapper`.  
3. **Sanitiza los resultados** (escape de HTML, recorte de longitud, eliminación de marcas peligrosas) para reducir riesgos de inyección.  
4. **Construye un prompt seguro** delimitando el bloque de contexto no confiable:  
```

UNTRUSTED CONTEXT START
... contenido de la web sanitizado ...
UNTRUSTED CONTEXT END

```
5. **Invoca el modelo de lenguaje** (`ChatOpenAI`) para generar un JSON con datos estructurados.  
6. **Valida la salida** con Guardrails, garantizando que cumple el esquema definido y bloqueando instrucciones o formatos peligrosos.

En resumen, el script toma resultados de Google, los limpia, se los pasa al modelo y asegura que la respuesta final sea un **JSON válido y seguro**.

---

## Uso en producción

Este ejemplo se mantiene en un solo archivo para **facilitar la lectura**.  
Sin embargo, en un entorno de producción debería **modularizarse** para mejorar mantenibilidad y escalabilidad. Una estructura recomendable sería:

- `config.py` → carga de claves y configuración de librerías.  
- `sanitizer.py` → funciones de sanitización y preprocesamiento de texto.  
- `validators.py` → definición de esquemas JSON y configuración de Guardrails.  
- `llm_agent.py` → funciones que interactúan con el modelo de lenguaje.  
- `search.py` → lógica para búsquedas en Google u otros proveedores.  
- `main.py` → punto de entrada que orquesta el flujo completo.

> Con esta separación, el código resulta más claro, permite pruebas unitarias independientes y facilita reemplazar componentes (por ejemplo, cambiar de motor de búsqueda o de validador).

---

## Referencias

- [Guardrails-AI: Getting Started](https://www.guardrailsai.com/docs/getting_started/guardrails_server)  
- [Guardrails Hub](https://hub.guardrailsai.com/)  
```

