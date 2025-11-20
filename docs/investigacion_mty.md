## Objetivo
Recopilar información curada sobre cultura, gastronomía y turismo de la zona metropolitana de Monterrey (ZMM) que sirva como base para el corpus de entrenamiento del chatbot compacto.

## Fuentes Priorizadas
- Secretaría de Turismo NL – `https://recursos.digital.nl.gob.mx/conocenl/`
- Travel Report – `https://www.travelreport.mx/destinos/nacionales/lugares-turisticos-de-nuevo-leon/`
- Inner MX – `https://inner.mx/2021/01/14/datos-que-no-sabias-de-la-macroplaza/`
- México Desconocido – `https://www.mexicodesconocido.com.mx`
- Visit Mexico – `https://www.visit-mexico.mx/es/nuevo-leon/`
- Blogs y reseñas locales (Alther, MVS Noticias, TripAdvisor) para lenguaje coloquial.

## Zonas Turísticas y Sitios Clave
- **Macroplaza**: 400 mil m², combina arquitectura moderna y colonial, alberga el Faro del Comercio y conecta con Paseo Santa Lucía. Fuente: Inner MX, Wikipedia.
- **Paseo Santa Lucía**: Canal artificial navegable de 2.5 km que une Macroplaza con Parque Fundidora; ofrece paseos en lancha y murales alusivos a la historia industrial. Fuente: Travel Report, Conoce NL.
- **Parque Fundidora y Museo Horno 3**: Complejo cultural en antiguas instalaciones siderúrgicas, incluye Cineteca, Arena Monterrey, Papalote Museo del Niño y rutas ciclistas. Fuente: Travel Report.
- **Cerro de la Silla**: Icono regiomontano con rutas de senderismo (Pico Norte, Antenas); miradores naturales con vistas de la ZMM. Fuente: Alther.
- **Cañón de la Huasteca**: Formaciones calizas en el Parque Nacional Cumbres; actividades de escalada y ciclismo de montaña. Fuente: Conoce NL.
- **Grutas de García**: Cuevas con estalactitas milenarias accesibles por teleférico; temperaturas frescas todo el año. Fuente: Visit Mexico.
- **Cola de Caballo y Presa La Boca**: En Santiago, ofrecen cascada de ~25 m, paseos a caballo y restaurantes de mariscos alrededor de la presa. Fuente: Conoce NL.
- **Pueblo Mágico de Santiago**: Centro histórico, Plaza Ocampo, quinta Manzanares, festividades gastronómicas. Fuente: MVS Noticias.
- **Valle Oriente / San Pedro**: Zona moderna con museos (Planetario Alfa), centros comerciales y oferta gastronómica cosmopolita. Fuente: Wikipedia.

## Gastronomía Típica
- **Cabrito al Pastor**: Cabrito lechal marinado y asado lentamente en varas horizontales; legado sefardí adaptado a la leña de mezquite. Restaurantes icónicos: El Rey del Cabrito, El Gran Pastor, El Indio Azteca.
- **Machaca con Huevo / Machacado**: Carne seca desmenuzada rehidratada con tomate, chile y huevo; desayuno emblemático.
- **Carne Seca**: Insumo para tacos y guisos; conserva la tradición ganadera del noreste.
- **Frijoles con Veneno**: Frijoles refritos con chorizo, chile piquín y manteca; acompañan carnes asadas.
- **Cortadillo Norteño**: Guiso de res en salsa de jitomate con papas y zanahoria, servido con arroz y tortillas de harina.
- **Tacos de Trompo Regios**: Similar al pastor pero con sazón de chile ancho y comino; se sirven con trompo rojo y piña opcional.
- **Dulces Regionales**: Glorias de Linares (leche quemada y nuez), hojarascas, natillas de Sabinas Hidalgo, pan de Bustamante horneado en leña.

## Restaurantes y Experiencias
- **El Rey del Cabrito (Av. Constitución)**: Tradición familiar desde 1963, carta especializada en cabrito al pastor y riñonada.
- **El Indio Azteca (Centro)**: Fundado en 1920; fama por cabrito tatemado y machaca. Ambiente de cantina clásica.
- **El Gran Pastor (Garza Sada y Lincoln)**: Porciones abundantes, menú de cabrito, arrachera y dulces regionales.
- **La Nacional (Vasconcelos)**: Cocina del noreste reinterpretada; cortes prime, tacos de lechón, mixología.
- **KOLI Cocina de Origen (San Pedro)**: Menú degustación que explora temporadas regiomontanas con técnicas contemporáneas.
- **Tacos Orinoco (Zona Centro, San Pedro, CDMX)**: Tacos estilo Monterrey (chicharrón, bistec, trompo) populares con locales y turistas.
- **Mercado Barrio Antiguo & Mercado del Norte**: Spots para comida callejera, cerveza artesanal y artesanías.

## Eventos y Cultura Viva
- **Festival Internacional Santa Lucía (sept-oct)**: Instalaciones artísticas, conciertos y proyecciones a cielo abierto en Macroplaza y Paseo Santa Lucía.
- **Tecate Pa’l Norte (marzo-abril)**: Festival musical masivo en Parque Fundidora.
- **Feria de la Manzana (Bustamante)** y **Fiestas del Santiago Apóstol**: Enfocadas en gastronomía tradicional, postres y danza folklórica.
- **Ruta del Asado Regio**: Eventos comunales de carnes asadas en colonias y parques con competencias amateur.

## Datos Logísticos Relevantes
- Clima semiárido: veranos >38 °C; conviene recomendar visitas matutinas a exteriores.
- Transporte: sistema Metrorrey (L1-L3), buses Ecovía, taxis de app; Uber y Didi operan ampliamente.
- Seguridad: enfatizar zonas turísticas vigiladas y recomendar horarios diurnos para parajes naturales.
- Moneda y pagos: mayoría de restaurantes aceptan tarjetas, pero mercados tradicionales funcionan mejor con efectivo.

## Propuesta de Curación de Datos
- Etiquetar cada bloque con `categoria` (turismo, gastronomia, evento, consejo), `ubicacion`, `fuente`, `fecha`.
- Capturar fragmentos de 80‑200 palabras por fuente para mantener diversidad estilística.
- Generar pares Pregunta/Respuesta con plantillas:
  - “¿Qué puedo hacer en [lugar]?” → descripción + sugerencias logísticas + recomendación culinaria cercana.
  - “¿Dónde pruebo [platillo]?” → breve historia, restaurantes destacados, precio promedio, horarios.
  - “¿Cuál es la mejor temporada para visitar [sitio natural]?” → clima, recomendaciones de equipo, eventos asociados.
- Complementar con listas tabulares (CSV) para referencias rápidas de direcciones, horarios y rangos de precio.

## Próximos Pasos
1. Expandir scraping con nuevas URLs (turismo, gastronomía, eventos) y registrar metadatos en `data/fuentes.csv`.
2. Diseñar scripts de limpieza que preserven títulos y listados para enriquecer respuestas del chatbot.
3. Preparar conjuntos QA balanceados con foco en turistas nacionales e internacionales, manteniendo tono cordial y experto.

