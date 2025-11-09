# app.py
import gradio as gr
import torch
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import os # Importamos os para verificar la ruta

# --- 1. Cargar el Modelo Entrenado ---
MODEL_PATH = "./modelo_guia_mty_final"

# Verificamos si el modelo existe ANTES de intentar cargarlo
if not os.path.exists(MODEL_PATH):
    print("="*50)
    print(f"🚨 Error: No se encontró la carpeta del modelo en: {MODEL_PATH}")
    print("Por favor, ejecuta primero el script 'train.py' para entrenar y guardar el modelo.")
    print("Comando: python3 train.py")
    print("="*50)
    exit() # Detiene la ejecución si no hay modelo

try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    model = AutoModelForCausalLM.from_pretrained(MODEL_PATH)
except Exception as e:
    print(f"Error al cargar el modelo: {e}")
    exit()

# Configurar el pipeline
generator = pipeline(
    'text-generation',
    model=model,
    tokenizer=tokenizer,
    device=0 if torch.cuda.is_available() else -1 # Usará GPU si está disponible
)

# --- 2. Funciones del Chatbot ---

def generate_response(prompt):
    """Genera una respuesta de guía a partir del prompt."""
    
    # Formato de prompt
    formatted_prompt = f"Usuario: {prompt} Guía:"

    try:
        output = generator(
            formatted_prompt,
            max_new_tokens=150,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            temperature=0.7,
            num_return_sequences=1,
            eos_token_id=tokenizer.eos_token_id
        )

        response_text = output[0]['generated_text']

        # Limpieza: Extraer solo la parte de la respuesta de la Guía
        start_index = response_text.rfind("Guía:") + len("Guía:")
        clean_response = response_text[start_index:].strip()
        
        if not clean_response or clean_response == prompt:
             return "No pude generar una respuesta sobre eso. ¿Puedes preguntarme de otra forma?"
        
        return clean_response
    except Exception as e:
        print(f"Error durante la generación: {e}")
        return "Disculpa, tuve un problema al generar la respuesta."

def chatbot_interface(user_input, history):
    """Función que maneja la conversación y la interfaz de Gradio."""
    response = generate_response(user_input)
    return response

# --- 3. Lanzar la Interfaz de Gradio ---

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
        # 🤖 Guía Conversacional de Cultura y Gastronomía de Monterrey
        Pregúntame sobre la historia del Paseo Santa Lucía, el cabrito, o cualquier otro dato local.
        """
    )
    # Usamos gr.ChatInterface, que es más simple para un chatbot
    chatbot = gr.ChatInterface(
        fn=chatbot_interface,
        title="Guía Compacta de MTY",
        chatbot=gr.Chatbot(height=500),
        textbox=gr.Textbox(placeholder="Escríbeme tu pregunta sobre MTY", container=False, scale=7),
        submit_btn="Enviar",
        # El argumento 'clear_btn' causaba el error. El botón se incluye automáticamente.
        # Agregamos 'type="messages"' para corregir el UserWarning.
        type="messages",
    )

if __name__ == "__main__":
    print("Iniciando interfaz de Gradio... (Recuerda ejecutar 'train.py' primero si el modelo no existe)")
    demo.launch()