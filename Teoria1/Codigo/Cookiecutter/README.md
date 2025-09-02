# Plantilla Cookiecutter para proyectos de agentes LLM

Este template está pensado para crear, de forma rápida y ordenada, la estructura básica de un proyecto de agentes basados en modelos de lenguaje.  
La idea es que partas de un esqueleto lógico de carpetas, sin tener que inventar la organización cada vez que arrancás algo nuevo.

---

## ¿Qué hace esta plantilla?

Cuando corrés `cookiecutter`, la plantilla te pregunta algunas opciones (ej. si querés FastAPI o Streamlit, si vas a usar RAG, qué vectorstore preferís, etc.).  
En base a esas respuestas, se genera **únicamente la estructura de carpetas** más conveniente para tu caso.

De esta forma, cada proyecto arranca prolijo desde el día uno, con carpetas ya pensadas para:

- Código fuente (`src/`)
- Documentación (`docs/`)
- Configuraciones (`configs/`)
- Infraestructura (`infra/`)
- Datos (`data/`)
- Tests (`tests/`, si activás la opción)
- Ejemplos (`examples/`, si lo pedís)
- Y más (según las features que selecciones)

---

## Cómo usarla

1. Cloná o descargá este repo.
2. Ejecutá:

   ```bash
   cookiecutter path/a/tu-template (Ej: cookiecutter .\cookiecutter-llm-agent\)
````

3. Contestá las preguntas (nombre del proyecto, interfaz, vectorstore, etc.).
4. Se genera la carpeta de tu proyecto con el esqueleto ya armado.

---

## Estructura resultante

El árbol de directorios depende de tus elecciones, pero en general vas a ver algo así:

```
Perfecto 🙌
Acá te armo la versión en `.md` con **esquema de árbol** y **comentarios a la derecha**. Así queda mucho más visual y directo.

---

```markdown
# Estructura del Proyecto de Agentes LLM

Este esqueleto se genera con Cookiecutter y varía según las opciones elegidas.  
Cada carpeta está comentada a la derecha para explicar su propósito.

---

## Esquema de carpetas

```

{{ project\_name }}/
├─ .github/
│  └─ workflows/              # Pipelines de CI/CD con GitHub Actions
│
├─ infra/                     # Infraestructura como código
│  ├─ docker/                 # Dockerfiles y docker-compose
│  ├─ k8s/                    # Configuraciones y manifests de Kubernetes
│  └─ terraform/              # Módulos Terraform para cloud
│
├─ configs/                   # Configuración del proyecto
│  ├─ envs/
│  │  ├─ dev/                 # Config para entorno de desarrollo
│  │  ├─ staging/             # Config para entorno de staging
│  │  └─ prod/                # Config para entorno de producción
│  └─ model/                  # Config de modelos LLM (OpenAI, Anthropic, local)
│
├─ data/                      # Ciclo de vida de datos
│  ├─ raw/                    # Datos crudos (PDF, CSV, JSON)
│  ├─ interim/                # Datos intermedios procesados parcialmente
│  └─ processed/              # Datos listos para indexar o usar
│
├─ docs/                      # Documentación técnica
│  ├─ architecture/           # Diagramas y vistas del sistema
│  ├─ decisions/              # ADRs (registros de decisiones técnicas)
│  └─ api/                    # Especificaciones y contratos de APIs
│
├─ logs/                      # Logs locales o temporales de ejecución
├─ notebooks/                 # Jupyter Notebooks para exploración/prototipos
├─ scripts/                   # Scripts reutilizables (ingesta, seeds, jobs)
│
├─ src/                       # Código principal del proyecto
│  ├─ common/
│  │  ├─ io/                  # Lectura/escritura de datos
│  │  ├─ utils/               # Funciones auxiliares comunes
│  │  └─ telemetry/           # Logging estructurado, métricas y tracing
│  │
│  ├─ agents/
│  │  ├─ cores/               # Clases base de agentes
│  │  ├─ skills/              # Habilidades atómicas (NLP, visión, etc.)
│  │  └─ orchestration/       # Coordinación de múltiples agentes
│  │
│  ├─ interfaces/
│  │  ├─ fastapi\_app/         # Si elegís FastAPI como interfaz
│  │  ├─ streamlit\_app/       # Si elegís Streamlit como interfaz
│  │  └─ cli/                 # Si no usás interfaz gráfica/web
│  │
│  ├─ graphs/                 # (si `use_langgraph=yes`) Flujos LangGraph
│  │  ├─ nodes/               # Nodos reutilizables
│  │  └─ workflows/           # Definiciones de workflows multiagente
│  │
│  ├─ rag/                    # (si `use_rag=yes`) Pipeline RAG
│  │  ├─ ingestion/           # Carga y chunking de documentos
│  │  ├─ retrievers/          # Métodos de recuperación
│  │  ├─ evaluators/          # Métricas y validaciones
│  │  └─ prompts/             # Prompts específicos para RAG
│  │
│  ├─ vectorstore/            # (si `use_vectorstore`) Almacenamiento vectorial
│  │  ├─ faiss/               # Motor FAISS local
│  │  └─ chroma/              # Motor Chroma DB
│  │
│  ├─ memory/                 # (si `use_memory`) Memoria de contexto
│  │  ├─ langchain/           # Memorias incluidas en LangChain
│  │  └─ redis/               # Persistencia distribuida en Redis
│  │
│  ├─ toolkits/               # (si `use_tools=yes`) Conjuntos de herramientas
│  │  ├─ http/                # Wrappers para APIs externas
│  │  ├─ db/                  # Conectores de bases de datos
│  │  └─ integrations/        # Integraciones SaaS (Slack, Gmail, etc.)
│  │
│  ├─ tools/                  # Herramientas atómicas invocables
│  │  ├─ builtin/             # Utilidades internas (fecha, math, etc.)
│  │  └─ external/            # Acceso a servicios externos
│  │
│  ├─ mcp/                    # (si `use_mcp=yes`) Model Context Protocol
│  │  ├─ servers/             # Servidores MCP
│  │  └─ clients/             # Clientes MCP
│  │
│  ├─ policies/               # Guardrails, validación, seguridad
│  └─ runtime/
│     ├─ adapters/            # Adaptadores de entrada/salida
│     ├─ providers/           # Wrappers de proveedores LLM
│     └─ pipelines/           # Preprocesamiento y postprocesamiento
│
├─ tests/                     # (si `enable_tests=yes`) Pruebas automatizadas
│  ├─ unit/                   # Unit tests
│  ├─ integration/            # Integration tests
│  └─ e2e/                    # End-to-end tests
│
├─ examples/                  # (si `add_examples=yes`) Ejemplos de uso
│  ├─ quickstarts/            # Ejemplos mínimos
│  └─ templates/              # Plantillas de módulos comunes
│
└─ tmp/                       # Archivos temporales (cache, staging, etc.)

```


## Resumen
- Las carpetas básicas (`src/`, `configs/`, `infra/`, `docs/`, etc.) se crean siempre.  
- Algunas son condicionales según tus elecciones de Cookiecutter (`rag`, `graphs`, `vectorstore`, `memory`, `toolkits`, `mcp`, `tests`, `examples`).  
- Este esqueleto asegura orden y escalabilidad para proyectos de agentes LLM.


---

## Detalle de decisiones

* **Hooks**

  * `pre_gen_project.py`: valida combinaciones (ej. no podés activar RAG sin vectorstore).
  * `post_gen_project.py`: crea las carpetas condicionalmente, según tus respuestas.

* **Filosofía**

  * No generamos archivos de más.
  * Todo se arma modular.


---

## Resumen

Este Cookiecutter no pretende dar una solución cerrada, sino un **punto de partida** para proyectos de agentes LLM.
Con un par de preguntas iniciales te deja listo un esqueleto de carpetas limpio y ordenado.


