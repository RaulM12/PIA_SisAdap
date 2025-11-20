"""
Herramienta de curación para compilar un corpus temático sobre la ZMM.

Uso:
    python scripts/build_corpus.py \
        --sources data/fuentes.csv \
        --raw-dir data/raw \
        --processed-dir data/processed \
        --output data/processed/corpus_mty_total.txt
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import os
import re
import textwrap
from pathlib import Path
from typing import Iterable, List

import requests
from bs4 import BeautifulSoup

DEFAULT_SOURCES = "data/fuentes.csv"
DEFAULT_RAW_DIR = Path("data/raw")
DEFAULT_PROCESSED_DIR = Path("data/processed")
DEFAULT_OUTPUT_FILE = Path("data/processed/corpus_mty_total.txt")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/119.0 Safari/537.36"
    )
}


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"https?://", "", value)
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")[:80]


def fetch_html(url: str, timeout: int = 15) -> str:
    response = requests.get(url, headers=HEADERS, timeout=timeout)
    response.raise_for_status()
    return response.text


def extract_paragraphs(html: str) -> List[str]:
    soup = BeautifulSoup(html, "lxml")
    main = (
        soup.find("article")
        or soup.find("div", class_="entry-content")
        or soup.find("main")
        or soup.body
        or soup
    )
    paragraphs = []
    for element in main.find_all(["p", "li"]):
        text = element.get_text(separator=" ", strip=True)
        if len(text) >= 60:
            paragraphs.append(text)
    return paragraphs


def deduplicate(chunks: Iterable[str]) -> List[str]:
    seen = set()
    result = []
    for chunk in chunks:
        digest = hashlib.sha1(chunk.encode("utf-8")).hexdigest()
        if digest not in seen:
            seen.add(digest)
            result.append(chunk)
    return result


def save_raw(html: str, path: Path) -> None:
    path.write_text(html, encoding="utf-8")


def save_processed(chunks: List[str], path: Path, metadata: dict) -> None:
    header = f"[{metadata['categoria']}] {metadata['descripcion']} ({metadata['url']})"
    wrapped = "\n".join(textwrap.fill(chunk, width=110) for chunk in chunks)
    path.write_text(f"{header}\n{wrapped}\n", encoding="utf-8")


def append_to_corpus(chunks: List[str], metadata: dict, output_file: Path) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with output_file.open("a", encoding="utf-8") as f:
        f.write("\n\n---\n")
        f.write(f"Categoria: {metadata['categoria']} | Subcategoria: {metadata['subcategoria']}\n")
        f.write(f"Fuente: {metadata['url']} | Fecha: {metadata['fecha_consulta']}\n\n")
        for chunk in chunks:
            f.write(chunk + "\n\n")


def process_source(row: dict, args: argparse.Namespace) -> None:
    url = row["url"]
    slug = slugify(row["descripcion"] or url)
    raw_path = Path(args.raw_dir) / f"{slug}.html"
    processed_path = Path(args.processed_dir) / f"{slug}.txt"

    print(f"[INFO] Procesando {row['descripcion']} -> {url}")
    html = fetch_html(url)
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    processed_path.parent.mkdir(parents=True, exist_ok=True)
    save_raw(html, raw_path)

    paragraphs = extract_paragraphs(html)
    if not paragraphs:
        print(f"[WARN] No se extrajeron párrafos útiles de {url}")
        return

    clean_chunks = deduplicate(paragraphs)
    save_processed(clean_chunks, processed_path, row)
    append_to_corpus(clean_chunks, row, Path(args.output))
    print(f"[OK] {len(clean_chunks)} fragmentos agregados al corpus.")


def load_sources(csv_path: str) -> List[dict]:
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Construye el corpus MTY desde fuentes CSV.")
    parser.add_argument("--sources", default=DEFAULT_SOURCES, help="Ruta al CSV de fuentes.")
    parser.add_argument("--raw-dir", default=DEFAULT_RAW_DIR, help="Directorio para HTML bruto.")
    parser.add_argument("--processed-dir", default=DEFAULT_PROCESSED_DIR, help="Directorio para textos limpios.")
    parser.add_argument("--output", default=DEFAULT_OUTPUT_FILE, help="Archivo corpus concatenado.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    sources = load_sources(args.sources)
    if not sources:
        raise SystemExit("No hay fuentes en el CSV.")

    # Limpia corpus previo si existe
    output_path = Path(args.output)
    if output_path.exists():
        os.remove(output_path)
        print(f"[INFO] Corpus previo eliminado: {output_path}")

    for row in sources:
        try:
            process_source(row, args)
        except Exception as exc:
            print(f"[ERROR] Falló {row.get('url')}: {exc}")


if __name__ == "__main__":
    main()

