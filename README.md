# GitHub Repo Fetcher

Este proyecto permite extraer repositorios públicos de un usuario u organización de GitHub usando la API REST v3. Incluye:

- Paginación automática
- Límite de extracción configurable
- Barra de progreso en consola (`tqdm`)
- Registro detallado en archivo (`logging`)
- Exportación a CSV

---

## 📦 Requisitos

- Python 3.8 o superior
- Token de acceso personal de GitHub

---

## ⚙️ Instalación

1. **Clona el repositorio o descarga los archivos**

2. **(Opcional) Crea un entorno virtual**

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instala las dependencias**

```bash
pip install -r requirements.txt
```

4. **Agrega tu token de GitHub en un archivo `.env`**

Crea un archivo `.env` en la raíz del proyecto:

```
GITHUB_TOKEN=ghp_tu_token_aqui
```


---

## 📁 Estructura del proyecto

```
eda-github/

├── README.md
├── logs
│   └── github_fetcher.log
├── main.py
├── output
│   └── repos.csv
└── requirements.txt
```

---

## ✅ Dependencias

Incluidas en `requirements.txt`:

```
requests
python-dotenv
tqdm
```