# -*- coding: utf-8 -*-
"""
Validaciones previas a la generación del proyecto.
Se ejecuta antes de crear el directorio del proyecto.
"""

import sys

USE_RAG = "{{ cookiecutter.use_rag }}"
USE_VECTORSTORE = "{{ cookiecutter.use_vectorstore }}"
INTERFACE = "{{ cookiecutter.interface }}"
USE_MEMORY = "{{ cookiecutter.use_memory }}"
USE_LANGGRAPH = "{{ cookiecutter.use_langgraph }}"
USE_TOOLS = "{{ cookiecutter.use_tools }}"
USE_MCP = "{{ cookiecutter.use_mcp }}"
LLM_PROVIDER = "{{ cookiecutter.llm_provider }}"

def fail(msg: str):
    print(f"[cookiecutter][pre_gen] ERROR: {msg}")
    sys.exit(1)

def warn(msg: str):
    print(f"[cookiecutter][pre_gen] AVISO: {msg}")

# Validaciones cruzadas simples
if USE_RAG == "yes" and USE_VECTORSTORE == "none":
    fail("Seleccionaste use_rag=yes pero use_vectorstore=none. Elegí 'faiss' o 'chroma'.")

if INTERFACE not in {"fastapi", "streamlit", "none"}:
    fail(f"interface inválido: {INTERFACE}")

if LLM_PROVIDER not in {"openai", "local", "anthropic"}:
    fail(f"llm_provider inválido: {LLM_PROVIDER}")

# Recomendaciones no bloqueantes
if USE_LANGGRAPH == "yes" and USE_TOOLS == "no":
    warn("Estás usando LangGraph sin tools. Es válido, pero revisá si querés habilitar tools para casos multi-agente.")

if USE_MEMORY == "redis" and USE_RAG == "no":
    warn("Elegiste memoria 'redis' sin RAG. Es válido, pero confirmá que realmente necesitás estado distribuido.")

print("[cookiecutter][pre_gen] Validaciones OK.")
