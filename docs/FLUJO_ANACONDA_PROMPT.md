# FLUJO COMPLETO — ANACONDA PROMPT
## Procesamiento InSAR-SBAS con MintPy v1.6.2
### TFM: Zonificación de deformaciones superficiales — Hoya de Loja (2019–2026)
**Autores:** Adan Saúl Abarca-Abarca & Byron Antonio Bravo-Granda — USGP, Ecuador

---

> **Importante:** Todo lo que está en este documento se ejecuta directamente
> en **Anaconda Prompt** (menú Inicio → buscar "Anaconda Prompt").
> **No uses PowerShell** — los comandos de MintPy no funcionan ahí.

---

## PASO 0 — CREAR EL ENTORNO CONDA

Ejecuta una sola vez al configurar el equipo por primera vez.

```
conda create -n mintpy python=3.10 -y
conda activate mintpy
conda install -c conda-forge mintpy -y
pip install hyp3-sdk asf-search pyaps3
```

Verifica que MintPy quedó instalado:

```
smallbaselineApp.py --version
```

Debe mostrar algo como: `MintPy v1.6.2`

---

## PASO 1 — CONFIGURAR CREDENCIALES

### 1A. Credenciales ECMWF / ERA5 (corrección troposférica)

Crea el archivo `~/.cdsapirc` con este contenido:

```
url: https://cds.climate.copernicus.eu/api
key: TU_KEY_CDS_ECMWF
```

> ⚠️ La URL correcta post-2024 es sin `/v2` al final.
> Obtén tu key en: https://cds.climate.copernicus.eu/user/register

### 1B. Credenciales EarthData (para los scripts Python de descarga)

Regístrate en: https://urs.earthdata.nasa.gov
Usa tu usuario y contraseña en los Scripts 02 y 03.

---

## PASO 2 — DESCARGAR INTERFEROGRAMAS (Scripts Python)

Los únicos pasos que usan scripts Python `.py` son la búsqueda y descarga.
Ejecuta desde Anaconda Prompt:

```
conda activate mintpy
cd AQUI_TU_RUTA_BASE/INTERFEROMETRIA_LOJA

python scripts/01_buscar_granules_ASF.py
python scripts/02_enviar_jobs_HyP3.py
python scripts/03_descargar_resultados_HyP3.py
```

Después de descargar, debes tener en `PROCESO_OK/` y `PROCESO_SUR/`
las carpetas de cada interferograma con los archivos:
- `*.unw.tif`  — fase desenvuelta
- `*.cor.tif`  — coherencia
- `*.dem.tif`  — modelo de elevación
- `*.lv_theta.tif` — ángulo de incidencia
- `*.unw_conncomp.tif` — componentes conectados

---

## PASO 3 — PREPARAR DIRECTORIO DE TRABAJO

```
conda activate mintpy
cd AQUI_TU_RUTA_BASE/INTERFEROMETRIA_LOJA/ARTICULO/PROCESO_OK
```

Copia el archivo de configuración a esta carpeta:

```
copy AQUI_TU_RUTA_BASE/configs/loja_sbas.cfg .
```

> El archivo `loja_sbas.cfg` debe estar en `PROCESO_OK/`, **no** en `inputs/`.

---

## PASO 4 — PROCESAMIENTO MINTPY (Órbita Norte, Track 116)

Todos estos comandos se ejecutan en Anaconda Prompt desde `PROCESO_OK/`.

### 4A. Cargar datos

```
smallbaselineApp.py loja_sbas.cfg --dostep load_data
```

Verifica que se creó `inputs/ifgramStack.h5`. Revisa el UNIT:

```
python -c "import h5py; f=h5py.File('inputs/ifgramStack.h5','r'); print(f['unwrapPhase'].attrs.get('UNIT','NO UNIT'))"
```

Debe decir `radian`. Si dice `meter`, edita el atributo:

```
python -c "import h5py; f=h5py.File('inputs/ifgramStack.h5','a'); f['unwrapPhase'].attrs['UNIT']='radian'; print('Corregido')"
```

### 4B. Modificar red interferométrica

```
smallbaselineApp.py loja_sbas.cfg --dostep modify_network
```

Revisa la figura generada en `pic/` para confirmar conectividad de la red.

### 4C. Punto de referencia

```
smallbaselineApp.py loja_sbas.cfg --dostep reference_point
```

Anota las coordenadas Y/X que aparecen en pantalla. Deben coincidir
con una zona estable y de alta coherencia temporal.
> Estudio original: y=434, x=180 | γ temporal = 0.96

### 4D. Inversión de red SBAS

```
smallbaselineApp.py loja_sbas.cfg --dostep invert_network
```

Tarda entre 30 min y 2 horas según el equipo.
Al terminar verifica: `number of reliable pixels` (estudio: 170,975 px con γtc ≥ 0.30)

### 4E. Corrección troposférica ERA5

```
smallbaselineApp.py loja_sbas.cfg --dostep correct_troposphere
```

Descarga automáticamente archivos ERA5 de ECMWF. Puede tardar varias horas
la primera vez (una descarga por fecha de adquisición).

Si falla con error de URL, verifica `~/.cdsapirc`:

```
python -c "import cdsapi; c=cdsapi.Client(); print('CDS OK')"
```

### 4F. Corrección de error DEM

```
smallbaselineApp.py loja_sbas.cfg --dostep correct_topography
```

### 4G. Estadísticas residuales y fecha de referencia

```
smallbaselineApp.py loja_sbas.cfg --dostep residual_RMS
smallbaselineApp.py loja_sbas.cfg --dostep reference_date
```

### 4H. Calcular velocidad

```
smallbaselineApp.py loja_sbas.cfg --dostep velocity
```

Al terminar existe `velocity.h5` en `PROCESO_OK/`.

### 4I. Geocodificar (si los datos no están ya en coordenadas geográficas)

```
smallbaselineApp.py loja_sbas.cfg --dostep geocode
```

> Con HyP3 los datos ya vienen geocodificados, este paso puede omitirse.

---

## PASO 5 — EXPORTAR GEOTIFF (Norte)

```
save_gdal.py geo_velocity.h5 velocity -o velocidad_norte_mmyr.tif
```

Si `geo_velocity.h5` no existe (datos ya geocodificados por HyP3):

```
save_gdal.py velocity.h5 velocity -o velocidad_norte_mmyr.tif
```

Verifica el resultado:

```
gdalinfo velocidad_norte_mmyr.tif
```

---

## PASO 6 — PROCESAMIENTO ÓRBITA SUR (Track 142)

Repite los Pasos 3 al 5 cambiando a la carpeta `PROCESO_SUR/`
y usando el archivo de configuración `loja_sur.cfg`.

```
cd AQUI_TU_RUTA_BASE/INTERFEROMETRIA_LOJA/ARTICULO/PROCESO_SUR
copy AQUI_TU_RUTA_BASE/configs/loja_sur.cfg .
smallbaselineApp.py loja_sur.cfg --dostep load_data
smallbaselineApp.py loja_sur.cfg --dostep modify_network
smallbaselineApp.py loja_sur.cfg --dostep reference_point
smallbaselineApp.py loja_sur.cfg --dostep invert_network
smallbaselineApp.py loja_sur.cfg --dostep correct_troposphere
smallbaselineApp.py loja_sur.cfg --dostep correct_topography
smallbaselineApp.py loja_sur.cfg --dostep residual_RMS
smallbaselineApp.py loja_sur.cfg --dostep reference_date
smallbaselineApp.py loja_sur.cfg --dostep velocity
save_gdal.py velocity.h5 velocity -o velocidad_sur_mmyr.tif
```

---

## PASO 7 — MOSAICO DE VELOCIDADES

El mosaico se realiza en **ArcMap** o **QGIS**:

1. Carga `velocidad_norte_mmyr.tif` y `velocidad_sur_mmyr.tif`.
2. Calcula la mediana de cada raster en la **zona de solapamiento**
   (Y = 9,542,940 — 9,552,360 m UTM17S).
3. Calcula el offset:
   - Mediana Norte en solap: −19.76 mm/año
   - Mediana Sur en solap:   +10.96 mm/año
   - **Offset = −30.72 mm/año** (aplica a la órbita Sur)
4. Suma el offset al raster Sur y combina con el Norte usando
   Mosaic to New Raster (ArcMap) o Merge (QGIS Raster Calculator).
5. Resultado final: `velocidad_COMPLETA_mmyr.tif`

---

## PASO 8 — VISUALIZACIÓN RÁPIDA EN MINTPY

Ver el mapa de velocidades desde Anaconda Prompt:

```
view.py velocity.h5 velocity --colormap RdBu_r --vlim -0.05 0.015 --save --dpi 300
```

Ver serie de tiempo en un pixel específico (y=434, x=180):

```
tsview.py timeseries_ERA5_demErr.h5 --yx 434 180
```

Ver coherencia temporal:

```
view.py temporalCoherence.h5 --colormap gray --vlim 0 1
```

---

## SOLUCIÓN DE ERRORES FRECUENTES

| Error | Causa | Solución |
|-------|-------|----------|
| `unknown satellite S1C` | MintPy no reconoce Sentinel-1C | Edita `prep_hyp3.py`, agrega `'S1C'` a la lista de satélites |
| `UNIT = meter` en ifgramStack | HyP3 escribe unidades incorrectas | Corrección manual en Paso 4A |
| Error de URL CDS/ECMWF | API URL cambió post-2024 | Usa `https://cds.climate.copernicus.eu/api` (sin /v2) |
| `weightFunc = var` colapsa coherencia | Incompatible con HyP3 geocodificado | Cambia a `weightFunc = no` en el .cfg |
| Gap S1B diciembre 2021 | 102 días sin datos | Normal — `skip_date` = 0 lo cubre automáticamente |
| `smallbaselineApp.py` no reconocido | PATH de entorno conda incorrecto | Usa `conda activate mintpy` primero; no usar PowerShell |

---

*Documento generado como parte del repositorio público del TFM.*
*USGP — Universidad San Gregorio de Portoviejo, Ecuador, 2025.*
