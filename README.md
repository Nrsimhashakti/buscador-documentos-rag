# AI Document Searcher (RAG System) 📑🤖

Aplicación web interactiva que implementa un sistema de **Generación Aumentada por Recuperación (RAG)**. Permite a los usuarios cargar archivos en formato PDF, procesar y segmentar su contenido en una base de datos vectorial de manera local, y realizar consultas inteligentes utilizando modelos de lenguaje avanzados sin riesgo de alucinaciones.

## 🚀 Características
* **Extracción de Texto:** Lectura automática y segmentación de archivos PDF mediante `pypdf`.
* **Base de Datos Vectorial:** Almacenamiento e indexación de fragmentos de texto usando `ChromaDB` en memoria.
* **Procesamiento de IA:** Integración con la API de Google Gemini utilizando el modelo de última generación `gemini-3.6-flash`.
* **Interfaz Gráfica:** Interfaz de usuario limpia, moderna e interactiva desarrollada con `Streamlit`.

## 📦 Tecnologías y Librerías utilizadas
* **Python 3**
* **Streamlit** (Frontend e Interfaz de Usuario)
* **ChromaDB** (Base de datos de vectores)
* **Pypdf** (Procesamiento de documentos)
* **Google GenAI SDK** (Inteligencia Artificial)
* **Python-dotenv** (Seguridad de variables de entorno)
