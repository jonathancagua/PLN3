# -*- coding: utf-8 -*-
"""
Crea la estructura de carpetas del proyecto (solo directorios).
Se ejecuta dentro del directorio ya generado.
"""

import os
from pathlib import Path

PROJECT_NAME = "{{ cookiecutter.project_name }}"
INTERFACE = "{{ cookiecutter.interface }}"
USE_LANGGRAPH = "{{ cookiecutter.use_langgraph }}"
USE_VECTORSTORE = "{{ cookiecutter.use_vectorstore }}"
USE_MEMORY = "{{ cookiecutter.use_memory }}"
USE_RAG = "{{ cookiecutter.use_rag }}"
USE_TOOLS = "{{ cookiecutter.use_tools }}"
USE_MCP = "{{ cookiecutter.use_mcp }}"
ENABLE_TESTS = "{{ cookiecutter.enable_tests }}"
ADD_EXAMPLES = "{{ cookiecutter.add_examples }}"

ROOT = Path(".")  # ya estás dentro de {{ cookiecutter.project_name }}

def mk(p: Path):
    p.mkdir(parents=True, exist_ok=True)

def main():
    # Base común
    base_dirs = [
        ".github/workflows",
        "infra/docker",
        "infra/k8s",
        "infra/terraform",
        "configs/envs/dev",
        "configs/envs/staging",
        "configs/envs/prod",
        "configs/model",
        "data/raw",
        "data/interim",
        "data/processed",
        "docs/architecture",
        "docs/decisions",
        "docs/api",
        "logs",
        "notebooks",
        "scripts",
        "src/common/io",
        "src/common/utils",
        "src/common/telemetry",
        "src/agents/cores",
        "src/agents/skills",
        "src/agents/orchestration",
        "src/policies",
        "src/tools/builtin",
        "src/tools/external",
        "src/runtime/adapters",
        "src/runtime/providers",
        "src/runtime/pipelines",
        "tmp",
    ]

    # Interface
    if INTERFACE == "fastapi":
        base_dirs.append("src/interfaces/fastapi_app")
    elif INTERFACE == "streamlit":
        base_dirs.append("src/interfaces/streamlit_app")
    else:
        base_dirs.append("src/interfaces/cli")

    # LangGraph
    if USE_LANGGRAPH == "yes":
        base_dirs += [
            "src/graphs/nodes",
            "src/graphs/workflows",
        ]

    # RAG
    if USE_RAG == "yes":
        base_dirs += [
            "src/rag/ingestion",
            "src/rag/retrievers",
            "src/rag/evaluators",
            "src/rag/prompts",
        ]

    # Vectorstore
    if USE_VECTORSTORE != "none":
        if USE_VECTORSTORE == "faiss":
            base_dirs.append("src/vectorstore/faiss")
        elif USE_VECTORSTORE == "chroma":
            base_dirs.append("src/vectorstore/chroma")

    # Memory
    if USE_MEMORY != "none":
        if USE_MEMORY == "langchain":
            base_dirs.append("src/memory/langchain")
        elif USE_MEMORY == "redis":
            base_dirs.append("src/memory/redis")

    # Toolkits
    if USE_TOOLS == "yes":
        base_dirs += [
            "src/toolkits/http",
            "src/toolkits/db",
            "src/toolkits/integrations",
        ]

    # MCP
    if USE_MCP == "yes":
        base_dirs += [
            "src/mcp/servers",
            "src/mcp/clients",
        ]

    # Tests
    if ENABLE_TESTS == "yes":
        base_dirs += [
            "tests/unit",
            "tests/integration",
            "tests/e2e",
        ]

    # Examples
    if ADD_EXAMPLES == "yes":
        base_dirs += [
            "examples/quickstarts",
            "examples/templates",
        ]

    # Crear directorios
    for d in base_dirs:
        mk(ROOT / d)

    print("[cookiecutter][post_gen] Directorios creados:")
    for d in base_dirs:
        print(f" - {d}")

if __name__ == "__main__":
    main()
