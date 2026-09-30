"""
Script: 02_enviar_jobs_HyP3.py
Propósito : Enviar pares SBAS a HyP3 (ASF) para procesamiento interferométrico
            con GAMMA. Genera interferogramas geocodificados listos para MintPy.
Entorno   : conda activate mintpy  →  python 02_enviar_jobs_HyP3.py
Autores   : Adan Saúl Abarca-Abarca & Byron Antonio Bravo-Granda — USGP

REQUISITO: Cuenta activa en https://hyp3-api.asf.alaska.edu  (EarthData Login)
"""

import hyp3_sdk as sdk
import pandas as pd
import time
from pathlib import Path

# =============================================================================
# CREDENCIALES EARTHDATA — REEMPLAZA CON LAS TUYAS
# =============================================================================
USUARIO  = "TU_USUARIO_EARTHDATA"
PASSWORD = "TU_PASSWORD_EARTHDATA"

# =============================================================================
# PARÁMETROS
# =============================================================================
# Archivo CSV con columnas: referencia, secundaria  (generado por Script 01)
CSV_PARES_NORTE = Path(r"AQUI_TU_RUTA_BASE/INTERFEROMETRIA_LOJA/LISTAS_GRANULES/pares_sbas_track116.csv")
CSV_PARES_SUR   = Path(r"AQUI_TU_RUTA_BASE/INTERFEROMETRIA_LOJA/LISTAS_GRANULES/pares_sbas_track142.csv")

# =============================================================================
# LOOKS POR TRACK — resolución geocodificada final: 40 × 40 m (EPSG:32717)
#   Track 116 (Norte/Centro) : 40 range × 8 azimuth  → 40 m geocodificado
#   Track 142 (Sur)          : 20 range × 4 azimuth  → 40 m geocodificado
# Ambas combinaciones producen la misma resolución de salida de 40 m.
# Ajusta LOOKS_RANGE y LOOKS_AZIMUTH según el track que estés enviando.
# Para el estudio Hoya de Loja se usaron los valores del Track 142 (Sur):
LOOKS_RANGE   = 20   # range looks  — Track 142 Sur  (usar 40 para Track 116 Norte)
LOOKS_AZIMUTH = 4    # azimuth looks — Track 142 Sur (usar 8  para Track 116 Norte)
# Resolución geocodificada resultante: ~40 m  (NO 80 m)

# Prefijos para identificar los trabajos en HyP3
PREFIJO_NORTE = "LOJA_N_"
PREFIJO_SUR   = "LOJA_S_"

# =============================================================================
def enviar_jobs(hyp3, df_pares, prefijo, descripcion):
    print(f"\n  Enviando {len(df_pares)} jobs — {descripcion}...")
    jobs = []
    for _, row in df_pares.iterrows():
        job = sdk.Batch()
        job += hyp3.submit_insar_job(
            granule1       = row["referencia"],
            granule2       = row["secundaria"],
            name           = prefijo + row["referencia"][17:25],  # fecha como ID
            looks          = f"{LOOKS_RANGE}x{LOOKS_AZIMUTH}",
            include_dem    = True,
            include_look_vectors = True,
        )
        jobs.append(job)
        time.sleep(0.3)  # respetar límite de tasa de la API

    print(f"  [{descripcion}] {len(jobs)} jobs enviados correctamente.")
    return jobs

# =============================================================================
print("ENVÍO DE JOBS A HyP3")
print("=" * 45)

hyp3 = sdk.HyP3(username=USUARIO, password=PASSWORD)
print(f"[OK] Conectado a HyP3 como: {USUARIO}")
print(f"     Cuota disponible: {hyp3.check_quota()} jobs/mes")

for csv_path, prefijo, desc in [
    (CSV_PARES_NORTE, PREFIJO_NORTE, "Track 116 — Norte/Centro"),
    (CSV_PARES_SUR,   PREFIJO_SUR,   "Track 142 — Sur"),
]:
    if csv_path.exists():
        df = pd.read_csv(csv_path)
        print(f"\n  Leyendo {len(df)} pares de: {csv_path.name}")
        enviar_jobs(hyp3, df, prefijo, desc)
    else:
        print(f"\n  [SKIP] No encontrado: {csv_path.name}")
        print(f"          Ejecuta primero Script 01.")

print("\n[OK] Todos los jobs enviados. Monitorea en:")
print("     https://hyp3-api.asf.alaska.edu/jobs  (o Script 03)")
