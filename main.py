import os
import requests
import csv
import logging
from typing import List, Dict, Optional
from dotenv import load_dotenv
from tqdm import tqdm

# Configuración global
MAX_REPOS = 10000
CSV_OUTPUT_PATH = "output/repos.csv"
LOG_PATH = "logs/github_fetcher.log"
PER_PAGE = 100

# Setup de logging
def setup_logging(log_file: str = LOG_PATH):
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

# Obtener repos públicos con paginación (endpoint simple)
def get_public_repositories(headers: dict, per_page: int = 100, max_items: Optional[int] = None) -> List[Dict]:
    """
    Extrae repos públicos desde https://api.github.com/repositories
    usando paginación básica.
    """
    all_repos = []
    since = 0
    pbar = tqdm(desc="Fetching public repos", unit="repo")

    while True:
        params = {"per_page": per_page, "since": since}
        response = requests.get("https://api.github.com/repositories", headers=headers, params=params)

        if response.status_code != 200:
            logging.error(f"Request failed: {response.status_code} - {response.text}")
            break

        repos = response.json()
        if not repos:
            break

        all_repos.extend(repos)
        pbar.update(len(repos))

        if max_items and len(all_repos) >= max_items:
            all_repos = all_repos[:max_items]
            break

        # El parámetro `since` es el ID del último repo
        since = repos[-1]["id"]

    pbar.close()
    logging.info(f"Total repos fetched: {len(all_repos)}")
    return all_repos

# Guardado a CSV
def save_repos_to_csv(repos: List[Dict], output_path: str = CSV_OUTPUT_PATH):
    """
    Guarda la lista de repositorios en un archivo CSV.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            "id", "name", "full_name", "html_url", "description", "language",
            "stargazers_count", "forks_count", "created_at", "updated_at"
        ])
        for repo in repos:
            writer.writerow([
                repo.get("id", ""),
                repo.get("name", ""),
                repo.get("full_name", ""),
                repo.get("html_url", ""),
                repo.get("description", ""),
                repo.get("language", ""),
                repo.get("stargazers_count", 0),
                repo.get("forks_count", 0),
                repo.get("created_at", ""),
                repo.get("updated_at", "")
            ])
    logging.info(f"Repos saved to: {output_path}")

# Ejecución principal
if __name__ == "__main__":
    setup_logging()
    load_dotenv()
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

    if not GITHUB_TOKEN:
        raise EnvironmentError("La variable GITHUB_TOKEN no está definida en el archivo .env.")

    HEADERS = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    repos = get_public_repositories(headers=HEADERS, per_page=PER_PAGE, max_items=MAX_REPOS)
    save_repos_to_csv(repos)
