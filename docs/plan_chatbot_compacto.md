## Objetivo General
Desarrollar un modelo compacto de lenguaje conversacional especializado en cultura y gastronomía de la ZMM que entregue respuestas contextuales en <900 ms en GPU media (<=8 GB) y <2 s en CPU moderna, manteniendo tamaño <1.5 GB.

## Alcance Funcional
- Consultas sobre sitios turísticos, platillos, eventos y consejos logísticos.
- Tono cordial, experto y seguro (evitar recomendaciones de riesgo).
- Capacidad de manejo de historial corto (últimos 3 turnos) para continuidad.

## Arquitectura Propuesta
1. **Capa de Datos**
   - `data/raw/` textos HTML y JSON.
   - `data/processed/` fragmentos limpios + metadatos.
   - `data/qa/` pares pregunta-respuesta (JSONL).
2. **Entrenamiento**
   - Base: TinyLlama-1.1B o Phi-3 Mini (3.8 GB FP16 → <1.5 GB INT4).
   - Adaptación con LoRA (r=16, α=32) para reducir VRAM.
3. **Inferencia**
   - Motor HuggingFace Transformers con `text-generation`.
   - Quantization INT4 + `bitsandbytes` para despliegues CPU/GPU ligeros.
4. **Interfaz**
   - Gradio `ChatInterface` con memoria resumida y logging.

## Plan de Trabajo y Entregables
| Semana | Actividades | Resultado |
|--------|-------------|-----------|
| 1 | Curación de fuentes, scraping y registro en `data/fuentes.csv`. | Corpus bruto categorizado. |
| 2 | Limpieza, segmentación temática, generación QA, control de calidad. | `corpus_mty_total.txt`, `qa_pairs.jsonl`. |
| 3 | Experimentos con modelos compactos, LoRA + cuantización, ajuste hiperparámetros. | Checkpoints evaluados, métricas (perplexity, latencia). |
| 4 | Entrenamiento final, validación manual, ajuste de prompts, integración en app. | Modelo final `modelo_guia_mty_final`. |
| 5 | Pruebas de estrés, documentación, handoff y roadmap de mejora. | Informe técnico + guía de uso. |

## Detalle de Fases
### 1. Adquisición y Curación de Datos
- Extender `collect_corpus` para admitir selectores CSS específicos.
- Añadir mecanismo de deduplicación (hash SHA1) y control de fecha.
- Registrar permisos/licencias en `data/fuentes.csv`.

### 2. Generación de QA y Contexto
- Plantillas específicas por categoría (turismo, gastronomía, eventos, logística).
- Incluir campos `tags` (ej. `["turismo","macroplaza"]`) para control de balance.
- Validar manualmente 10 % de los pares para asegurar factualidad.

### 3. Entrenamiento y Optimización
- Evaluar bases: DistilGPT2 (baseline), TinyLlama-1.1B (objetivo), Phi-3 Mini (stretch).
- Aplicar LoRA + `peft` y cuantización QLoRA (NF4) para entrenamiento en GPU <=12 GB.
- Ajustar `TrainingArguments`: `num_train_epochs=3`, `lr≈2e-4`, `warmup_ratio=0.05`, `weight_decay=0.01`.
- Monitorizar perplexity en set de validación y métricas cualitativas (BLEU/cobertura).

### 4. Validación
- Banco de 60 preguntas reales: 20 turismo, 20 gastronomía, 10 eventos, 10 logística.
- Criterios: exactitud factual, contexto, seguridad, tono.
- Registro de fallas para retroalimentar corpus.

### 5. Despliegue e Integración
- Exportar modelo en formatos: HF estándar (`fp16`), `gguf` cuantizado (opcional).
- Añadir memoria conversacional y logging en `app.py`.
- Crear script `serve.py` con argumentos CLI para CPU/GPU, temperatura y top_p dinámicos.

## Riesgos y Mitigaciones
- **Corpus insuficiente**: priorizar fuentes oficiales y ampliar con reseñas verificadas.
- **Hallucinations**: reforzar con facts tabulares y prompts estructurados.
- **Latencia alta**: usar cuantización y limitar `max_new_tokens`.
- **Actualización de datos**: calendarizar refresh trimestral del corpus.

## Próximos Pasos Inmediatos
1. Crear estructura `data/` y plantilla `data/fuentes.csv`.
2. Actualizar scripts de scraping/limpieza.
3. Definir baseline de evaluación con el modelo actual (`distilgpt2` fine-tuned) para medir mejoras.

