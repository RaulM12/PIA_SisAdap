# train.py
import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
import re
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer, DataCollatorForLanguageModeling
import torch

# --- Definiciones Globales ---
MODEL_NAME = "distilgpt2"
CORPUS_FILE = "data/processed/corpus_mty_total.txt"
MODEL_PATH = "./modelo_guia_mty_final" # La carpeta donde se guardará el modelo

# --- 1. Recolección de Datos (Web Scraping) ---
def collect_corpus(url, filename):
    """Función para extraer texto de una URL y guardarlo."""
    print(f"Intentando extraer de: {url}...")
    try:
        respuesta = requests.get(url, timeout=10)
        respuesta.raise_for_status() 
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener la página {url}: {e}")
        return

    if respuesta.status_code == 200:
        soup = BeautifulSoup(respuesta.text, 'lxml')
        # Buscamos clases comunes de contenido
        main_content = soup.find('div', class_='entry-content') or \
                       soup.find('article') or \
                       soup.find('main')
        
        if not main_content:
            main_content = soup 

        textos_extraidos = []
        parrafos = main_content.find_all('p')

        for p in parrafos:
            texto = p.get_text().strip()
            if len(texto) > 50: # Aumentamos el mínimo para mejor calidad
                textos_extraidos.append(texto)

        if textos_extraidos:
            # Usar 'a' para agregar a un corpus general
            with open(filename, 'a', encoding='utf-8') as f: 
                f.write("\n\n---\n\n" + "\n".join(textos_extraidos))
            print(f"✅ Éxito: Se agregó información de {url} a {filename}.")
        else:
            print(f"Advertencia: No se pudo extraer texto relevante de {url}.")

# --- 2. Preparación del Dataset ---
def clean_text_and_format_qa(text):
    """Limpia el texto y lo formatea."""
    soup = BeautifulSoup(text, 'html.parser')
    clean_text = soup.get_text()
    clean_text = re.sub(r'[\n\t\r]+', ' ', clean_text)
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
    
    # NOTA: Como en tu script original, esto es texto plano.
    # Para un chatbot real, idealmente crearías pares Pregunta/Respuesta.
    # Por ahora, usamos el texto limpio.
    
    # Dividimos el texto en trozos más pequeños para un mejor dataset
    # en lugar de un solo documento gigante.
    chunks = [clean_text[i:i+512] for i in range(0, len(clean_text), 512)]
    
    return pd.DataFrame(chunks, columns=["text"])

def tokenize_function(examples):
    return tokenizer(examples["text"], truncation=True, max_length=512, padding="max_length")

# --- 3. Script Principal de Entrenamiento ---
if __name__ == "__main__":
    
    print("--- Iniciando Proceso de Entrenamiento ---")

    # --- Paso 1: Validar Corpus Procesado ---
    if not os.path.exists(CORPUS_FILE):
        print(f"Error: No se encontró el archivo {CORPUS_FILE}.")
        print("Ejecuta primero 'py -3 scripts/build_corpus.py' para generarlo.")
        exit()

    # --- Paso 2: Cargar y Tokenizar Corpus ---
    try:
        with open(CORPUS_FILE, 'r', encoding='utf-8') as f:
            raw_text = f.read()
    except FileNotFoundError:
        print(f"Error: El archivo {CORPUS_FILE} no fue encontrado o no se pudo crear.")
        print("Asegúrate de tener fuentes de datos válidas.")
        exit()

    if len(raw_text) < 100:
        print("Error: El corpus es demasiado pequeño. No se puede entrenar.")
        exit()
        
    print(f"Corpus cargado. Limpiando y formateando...")
    qa_df = clean_text_and_format_qa(raw_text)
    
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    hf_dataset = Dataset.from_pandas(qa_df)
    tokenized_datasets = hf_dataset.map(tokenize_function, batched=True, remove_columns=["text"])
    
    tokenized_datasets = tokenized_datasets.map(
        lambda examples: {"labels": examples["input_ids"]},
        batched=True
    )

    # --- Paso 3: Dividir Dataset ---
    if len(tokenized_datasets) > 1:
        split = tokenized_datasets.train_test_split(test_size=0.1)
        train_dataset = split["train"]
        eval_dataset = split["test"]
    else:
        print("Advertencia: Dataset pequeño. Usando el mismo para entrenamiento y validación.")
        train_dataset = tokenized_datasets
        eval_dataset = tokenized_datasets

    print(f"Dataset listo: {len(train_dataset)} ejemplos de entrenamiento.")

    # --- Paso 4: Configurar Fine-Tuning ---
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

    training_args = TrainingArguments(
        output_dir="./results_mty_guide",      # Directorio temporal de checkpoints
        num_train_epochs=5,                    
        per_device_train_batch_size=4,
        logging_steps=10,
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        fp16=torch.cuda.is_available(),        # fp16 solo funciona en GPU (CUDA)
        report_to="none"
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        data_collator=data_collator,
    )

    # --- Paso 5: Entrenar ---
    print("\nIniciando Fine-Tuning... Esto puede tardar varios minutos.")
    trainer.train()

    # --- Paso 6: Guardar Modelo Final ---
    print(f"\n✅ Fine-Tuning Completo. Guardando modelo final en {MODEL_PATH}.")
    trainer.save_model(MODEL_PATH)
    tokenizer.save_pretrained(MODEL_PATH)
    print("--- Proceso de Entrenamiento Terminado ---")