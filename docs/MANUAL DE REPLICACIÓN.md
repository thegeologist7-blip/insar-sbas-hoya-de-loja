# MANUAL DE REPLICACIÓN

## Procesamiento InSAR-SBAS de deformaciones superficiales con MintPy

### Hoya de Loja, Ecuador — 2019–2026

**Autores:** Adan Saúl Abarca-Abarca · Byron Antonio Bravo-Granda  
**Institución:** Universidad San Gregorio de Portoviejo (USGP), Ecuador  
**Programa:** Maestría en Prevención y Gestión de Riesgos  
**Versión:** 1.0 — 2026

---

# 1. OBJETIVO DEL MANUAL

Este documento describe paso a paso el procedimiento utilizado para reproducir el procesamiento **InSAR-SBAS (Small Baseline Subset)** aplicado a la Hoya de Loja, Ecuador, durante el periodo 2019–2026.

El flujo permite obtener productos de **velocidad de deformación superficial proyectada sobre la línea de visión del radar (LOS)** a partir de datos Sentinel-1.

El procedimiento comprende:

1. configuración del entorno computacional;
2. configuración de credenciales de servicios externos;
3. búsqueda de escenas Sentinel-1;
4. generación de pares interferométricos;
5. envío de trabajos a HyP3;
6. descarga de productos interferométricos;
7. preparación de los datos para MintPy;
8. construcción y modificación de la red interferométrica;
9. selección del punto de referencia;
10. inversión de la red SBAS;
11. corrección troposférica mediante ERA5/PyAPS3;
12. corrección del error topográfico;
13. cálculo de velocidad LOS;
14. exportación de los resultados a GeoTIFF;
15. procesamiento independiente de las diferentes geometrías de adquisición;
16. integración espacial de los productos cuando corresponde;
17. visualización y control de calidad.

> **Importante:** InSAR mide deformación proyectada sobre la línea de visión del radar (LOS). El producto de velocidad LOS no representa directamente desplazamiento vertical puro ni permite determinar por sí solo el mecanismo geológico o geotécnico responsable de la deformación.

---

# 2. ALCANCE DEL REPOSITORIO

El núcleo del repositorio corresponde al procesamiento InSAR-SBAS hasta la generación de productos de velocidad LOS.

El flujo principal es:

```text
Sentinel-1
      ↓
Búsqueda de escenas
      ↓
Selección de pares SBAS
      ↓
Procesamiento interferométrico HyP3
      ↓
Productos interferométricos
      ↓
MintPy
      ↓
Inversión SBAS
      ↓
Correcciones atmosféricas y topográficas
      ↓
Velocidad LOS
      ↓
GeoTIFF