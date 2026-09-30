# MANUAL DE REPLICACIÓN

## Análisis InSAR-SBAS de Deformaciones Superficiales con MintPy

### Hoya de Loja, Ecuador (2019–2026)

**Autores:** Adan Saúl Abarca-Abarca · Byron Antonio Bravo-Granda
**Institución:** Universidad San Gregorio de Portoviejo (USGP), Ecuador
**Versión:** 1.0 — Junio 2025

\---

## ¿QUÉ CONTIENE ESTE REPOSITORIO?

Este repositorio documenta el flujo de trabajo completo para reproducir el análisis
InSAR-SBAS de deformaciones superficiales de la Hoya de Loja publicado como parte
del TFM de maestría en Prevención y Gestión de Riesgos de la USGP.

El flujo tiene **dos partes diferenciadas**:

1. **Scripts Python** (carpeta `scripts/`) — solo para buscar y descargar imágenes SAR.
2. **Comandos Anaconda Prompt** (`docs/FLUJO\\\\\\\_ANACONDA\\\\\\\_PROMPT.md`) — todo el procesamiento MintPy.

\---

## REQUISITOS DE SOFTWARE

|Software|Versión|Obtención|
|-|-|-|
|Anaconda / Miniconda|cualquiera reciente|https://www.anaconda.com|
|MintPy|1.6.2|vía conda-forge|
|HyP3 SDK|última|vía pip|
|ASF Search|última|vía pip|
|PyAPS3|0.3.7|vía pip|
|ArcMap / QGIS|cualquiera|para mosaico final|

**Sistema operativo probado:** Windows 10/11 (64-bit)
El flujo es compatible con Linux/macOS cambiando las rutas de `\\\\\\\\` a `/`.

\---

## REQUISITOS DE CUENTAS (gratuitas)

Necesitas crear dos cuentas antes de empezar:

**1. NASA EarthData** (para descargar imágenes Sentinel-1 y usar HyP3)
→ https://urs.earthdata.nasa.gov/users/new

**2. ECMWF Copernicus CDS** (para descargar datos ERA5 de corrección troposférica)
→ https://cds.climate.copernicus.eu/user/register
→ Después de registrarte, obtén tu API key en tu perfil de usuario.

\---

## INSTALACIÓN RÁPIDA (10 minutos)

Abre **Anaconda Prompt** y ejecuta:

```
conda create -n mintpy python=3.10 -y
conda activate mintpy
conda install -c conda-forge mintpy -y
pip install hyp3-sdk asf-search pyaps3
```

Verifica:

```
smallbaselineApp.py --version
```

Configura tu API key de ECMWF. Crea el archivo `C:/Users/TU\\\\\\\_USUARIO/.cdsapirc`
con este contenido:

```
url: https://cds.climate.copernicus.eu/api
key: TU\\\\\\\_KEY\\\\\\\_AQUI
```

\---

## ESTRUCTURA DEL REPOSITORIO

```
insar-sbas-hoya-loja/
│
├── scripts/                      ← Scripts Python (búsqueda y descarga)
│   ├── 01\\\\\\\_buscar\\\\\\\_granules\\\\\\\_ASF.py
│   ├── 02\\\\\\\_enviar\\\\\\\_jobs\\\\\\\_HyP3.py
│   └── 03\\\\\\\_descargar\\\\\\\_resultados\\\\\\\_HyP3.py
│
├── configs/                      ← Archivos de configuración MintPy
│   ├── loja\\\\\\\_sbas.cfg             ← Órbita Norte (Track 116)
│   └── loja\\\\\\\_sur.cfg              ← Órbita Sur (Track 142)
│
├── docs/                         ← Documentación
│   ├── FLUJO\\\\\\\_ANACONDA\\\\\\\_PROMPT.md  ← Todos los comandos de procesamiento
│   └── MANUAL\\\\\\\_REPLICACION.md     ← Este archivo
│
├── README.md
├── requirements.txt
└── environment.yml
```

\---

## PARÁMETROS DEL ESTUDIO ORIGINAL

Si quieres replicar exactamente los resultados publicados, usa estos parámetros:

|Parámetro|Valor|
|-|-|
|Satélite|Sentinel-1A/B/C, banda C, modo IW, polarización VV|
|Dirección de vuelo|Descendente|
|Órbita Norte|Track 116 — 215 adquisiciones — 418 interferogramas|
|Órbita Sur|Track 142 — 216 adquisiciones — 389 interferogramas|
|Período|2019-10-07 a 2026-03-10|
|Resolución final|\~80 m (looks 20×4)|
|Sistema de coordenadas|EPSG:32717 (UTM Zona 17S)|
|Δt máximo|120 días|
|Δ⊥ máximo|500 m|
|Coherencia mínima red|0.4|
|Coherencia temporal mínima|0.30 (para mapa final)|
|Corrección troposférica|ERA5 vía PyAPS3|
|Corrección topográfica|DEM error (Fattahi \& Amelung, 2013)|
|Punto de referencia|y=434, x=180 — γ temporal = 0.96|

**Resultados verificados:**

* Píxeles coherentes: 170,975 (γtc ≥ 0.30)
* Velocidad mediana: −16.5 mm/año
* Velocidad mínima: −86.7 mm/año
* Velocidad máxima: +112.2 mm/año
* Kruskal-Wallis entre litologías: H = 28,949.09, p < 0.001

\---

## FLUJO RESUMIDO PASO A PASO

```
\\\\\\\[1] Instalar entorno conda + MintPy
        ↓
\\\\\\\[2] Script 01: buscar granules en ASF Vertex (Python)
        ↓
\\\\\\\[3] Script 02: enviar pares a HyP3 para procesamiento (Python)
        ↓
\\\\\\\[4] Script 03: descargar interferogramas completados (Python)
        ↓
\\\\\\\[5] Anaconda Prompt: smallbaselineApp.py loja\\\\\\\_sbas.cfg  (paso a paso)
    load\\\\\\\_data → modify\\\\\\\_network → reference\\\\\\\_point → invert\\\\\\\_network
    → correct\\\\\\\_troposphere → correct\\\\\\\_topography → velocity
        ↓
\\\\\\\[6] Exportar GeoTIFF con save\\\\\\\_gdal.py
        ↓
\\\\\\\[7] Repetir pasos 5-6 para Órbita Sur
        ↓
\\\\\\\[8] Mosaico en ArcMap/QGIS + corrección de offset
        ↓
\\\\\\\[9] Análisis estadístico: clasificación cinemática, Kruskal-Wallis
```

Para el detalle completo de cada paso, consulta:
`docs/FLUJO\\\\\\\_ANACONDA\\\\\\\_PROMPT.md`

\---

## ADAPTACIÓN A OTRAS ÁREAS DE ESTUDIO

Para aplicar esta metodología a otra región:

1. **Modifica el AOI** en `scripts/01\\\\\\\_buscar\\\\\\\_granules\\\\\\\_ASF.py`:
Cambia `AOI\\\\\\\_WKT` con el polígono WKT de tu área de interés.
2. **Ajusta los tracks**: busca en ASF Vertex (https://search.asf.alaska.edu)
qué órbitas relativas cubren tu área.
3. **Modifica las rutas** en `configs/loja\\\\\\\_sbas.cfg`:
Reemplaza `AQUI\\\\\\\_TU\\\\\\\_RUTA\\\\\\\_BASE` con tu directorio real.
4. **Ajusta el período**: cambia `FECHA\\\\\\\_INICIO` y `FECHA\\\\\\\_FIN` en el Script 01.
5. **Selecciona tu punto de referencia**: elige una zona estable (roca dura,
sin subsidencia conocida) con coherencia temporal alta.

\---

## CITAR ESTE TRABAJO

Si utilizas este repositorio o metodología en tu investigación, cita:

> Abarca-Abarca, A. S., \\\\\\\& Bravo-Granda, B. A. (2025). \\\\\\\*Zonificación de
> deformaciones superficiales mediante análisis InSAR-SBAS (2019–2026)
> en la Hoya de Loja\\\\\\\*. Trabajo de Fin de Máster, Universidad San Gregorio
> de Portoviejo, Ecuador.

\---

## REFERENCIAS METODOLÓGICAS CLAVE

* Berardino, P., Fornaro, G., Lanari, R., \& Sansosti, E. (2002). A new algorithm
for surface deformation monitoring based on small baseline differential SAR
interferograms. *IEEE TGRS*, 40(11), 2375–2383.
https://doi.org/10.1109/TGRS.2002.803792
* Yunjun, Z., Fattahi, H., \& Amelung, F. (2019). Small baseline InSAR time
series analysis: Unwrapping error correction and noise reduction. *Computers
\& Geosciences*, 133, 104331.
https://doi.org/10.1016/j.cageo.2019.104331
* Jolivet, R., Grandin, R., Lasserre, C., Doin, M. P., \& Peltzer, G. (2011).
Systematic InSAR tropospheric phase delay corrections from global meteorological
reanalysis data. *GRL*, 38, L17311.
https://doi.org/10.1029/2011GL048757
* Fattahi, H., \& Amelung, F. (2013). DEM error correction in InSAR time series.
*IEEE TGRS*, 51(7), 4249–4259.
https://doi.org/10.1109/TGRS.2012.2227761

\---

## 

