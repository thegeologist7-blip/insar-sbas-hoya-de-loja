"""
Script: 01_buscar_granules_ASF.py
Propósito : Buscar adquisiciones Sentinel-1 en ASF Vertex y generar
            lista de pares SBAS para ambas órbitas (Track 116 y 142).
Entorno   : conda activate mintpy  →  python 01_buscar_granules_ASF.py
Autores   : Adan Saúl Abarca-Abarca & Byron Antonio Bravo-Granda — USGP
"""

import asf_search as asf
import pandas as pd
from itertools import combinations
from datetime import datetime
from pathlib import Path

# =============================================================================
# PARÁMETROS — AJUSTA SEGÚN TU ÁREA DE ESTUDIO
# =============================================================================
AOI_WKT      = "POLYGON((-79.35 -3.75,-78.95 -3.75,-78.95 -4.25,-79.35 -4.25,-79.35 -3.75))"
FECHA_INICIO = "2019-10-01"
FECHA_FIN    = "2026-03-10"
TRACK_NORTE  = 116          # 215 adquisiciones en el estudio original
TRACK_SUR    = 142          # 216 adquisiciones, disponible desde 2022-03-31
MAX_DIAS     = 120          # línea de base temporal máxima

DIR_SALIDA   = Path(r"AQUI_TU_RUTA_BASE/INTERFEROMETRIA_LOJA/LISTAS_GRANULES")
DIR_SALIDA.mkdir(parents=True, exist_ok=True)

# =============================================================================
def buscar_granules(track, fecha_ini, fecha_fin):
    resultados = asf.geo_search(
        intersectsWith  = AOI_WKT,
        platform        = asf.PLATFORM.SENTINEL1,
        processingLevel = asf.PRODUCT_TYPE.SLC,
        beamMode        = asf.BEAMMODE.IW,
        flightDirection = asf.FLIGHT_DIRECTION.DESCENDING,
        relativeOrbit   = track,
        start           = fecha_ini,
        end             = fecha_fin,
    )
    print(f"  Track {track}: {len(resultados)} adquisiciones encontradas")
    return resultados

def generar_pares(granules, max_dias):
    datos = sorted([
        {"nombre": g.properties['sceneName'],
         "fecha" : datetime.strptime(g.properties['startTime'][:10], "%Y-%m-%d")}
        for g in granules
    ], key=lambda x: x["fecha"])

    pares = [
        {"referencia": a["nombre"], "secundaria": b["nombre"],
         "delta_dias": abs((b["fecha"] - a["fecha"]).days)}
        for a, b in combinations(datos, 2)
        if abs((b["fecha"] - a["fecha"]).days) <= max_dias
    ]
    print(f"  Pares SBAS (Δt ≤ {max_dias}d): {len(pares)}")
    return pd.DataFrame(pares)

# =============================================================================
print("BÚSQUEDA GRANULES — ASF Vertex")
print("=" * 45)

configs = [
    (TRACK_NORTE, FECHA_INICIO, FECHA_FIN),
    (TRACK_SUR,   "2022-03-31", FECHA_FIN),
]

for track, fi, ff in configs:
    print(f"\nTrack {track}  ({fi} → {ff}):")
    granules = buscar_granules(track, fi, ff)
    df_pares = generar_pares(granules, MAX_DIAS)

    pd.Series([g.properties['sceneName'] for g in granules]).to_csv(
        DIR_SALIDA / f"escenas_track{track}.csv", index=False, header=["sceneName"])
    df_pares.to_csv(DIR_SALIDA / f"pares_sbas_track{track}.csv", index=False)
    print(f"  Guardado → escenas_track{track}.csv | pares_sbas_track{track}.csv")

print("\n[OK] Búsqueda completada.")
