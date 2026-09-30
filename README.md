# InSAR-SBAS Hoya de Loja (2019–2026)

Repositorio reproducible para el procesamiento **InSAR-SBAS (Small Baseline Subset)** orientado a la estimación y zonificación de **velocidades de deformación superficial en la línea de visión del radar (LOS)** en la Hoya de Loja, Ecuador.

---

## Autores

**Byron Antonio Bravo-Granda**  
**Adan Saúl Abarca-Abarca**

**Tutora:** Dra. Liliana Troncoso  
**Institución:** Universidad San Gregorio de Portoviejo (USGP)  
**Programa:** Maestría en Prevención y Gestión de Riesgos

---

## Proyecto

**Título del TFM:**

*Zonificación de deformaciones superficiales mediante análisis InSAR-SBAS (2019–2026) en la Hoya de Loja: una perspectiva preventiva para la gestión del riesgo de desastres.*

---

## Descripción

Este repositorio documenta el flujo de procesamiento InSAR-SBAS utilizado para obtener productos de **velocidad de deformación superficial LOS** a partir de imágenes Sentinel-1 en la Hoya de Loja, Ecuador.

El flujo integra:

1. búsqueda de escenas Sentinel-1;
2. construcción de pares interferométricos SBAS;
3. procesamiento mediante HyP3/GAMMA;
4. descarga y organización de los productos interferométricos;
5. preparación de los datos para MintPy;
6. inversión de la red interferométrica;
7. corrección atmosférica mediante ERA5/PyAPS3;
8. corrección del error topográfico;
9. estimación de velocidad LOS;
10. exportación de los resultados a formato GeoTIFF.

El resultado principal del procesamiento es un producto raster de **velocidad de deformación superficial en la línea de visión del radar (LOS)**.

> **Importante:** InSAR mide deformación proyectada sobre la línea de visión del radar (LOS). Los resultados no deben interpretarse directamente como desplazamiento vertical puro ni como identificación inequívoca del mecanismo geológico o geotécnico responsable.

---

## Alcance del repositorio

El núcleo de este repositorio corresponde al **procesamiento InSAR-SBAS hasta la generación de los productos LOS**.

Los análisis posteriores —por ejemplo:

- relación con unidades geológicas;
- análisis de pendiente;
- análisis pluviométrico;
- exposición de población e infraestructura;
- interpretación territorial y de gestión del riesgo—

constituyen módulos de análisis posteriores al procesamiento InSAR y pueden desarrollarse utilizando los productos LOS generados por este flujo.

Por tanto, el repositorio distingue entre:

**Procesamiento InSAR-SBAS**

```text
Sentinel-1
    ↓
Búsqueda de escenas
    ↓
Pares SBAS
    ↓
HyP3 / GAMMA
    ↓
Interferogramas
    ↓
MintPy
    ↓
Velocidad LOS
    ↓
GeoTIFF