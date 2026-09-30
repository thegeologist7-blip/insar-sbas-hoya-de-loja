"""
Script: 03_descargar_resultados_HyP3.py
Propósito : Verificar estado de jobs en HyP3 y descargar interferogramas
            completados. Organiza archivos por prefijo (Norte / Sur).
Entorno   : conda activate mintpy  →  python 03_descargar_resultados_HyP3.py
Autores   : Adan Saúl Abarca-Abarca & Byron Antonio Bravo-Granda — USGP
"""

import hyp3_sdk as sdk
import time
from pathlib import Path

# =============================================================================
# CREDENCIALES — REEMPLAZA CON LAS TUYAS
# =============================================================================
USUARIO  = "TU_USUARIO_EARTHDATA"
PASSWORD = "TU_PASSWORD_EARTHDATA"

# =============================================================================
# DIRECTORIOS DE DESCARGA
# =============================================================================
DIR_NORTE = Path(r"AQUI_TU_RUTA_BASE/INTERFEROMETRIA_LOJA/ARTICULO/PROCESO_OK")
DIR_SUR   = Path(r"AQUI_TU_RUTA_BASE/INTERFEROMETRIA_LOJA/ARTICULO/PROCESO_SUR")

DIR_NORTE.mkdir(parents=True, exist_ok=True)
DIR_SUR.mkdir(parents=True, exist_ok=True)

PREFIJO_NORTE = "LOJA_N_"
PREFIJO_SUR   = "LOJA_S_"

# =============================================================================
print("MONITOREO Y DESCARGA — HyP3")
print("=" * 45)

hyp3 = sdk.HyP3(username=USUARIO, password=PASSWORD)
print(f"[OK] Conectado como: {USUARIO}\n")

# Obtener todos los jobs
todos_jobs = hyp3.find_jobs()

pendientes = [j for j in todos_jobs if j.status_code in ("PENDING", "RUNNING")]
completados= [j for j in todos_jobs if j.status_code == "SUCCEEDED"]
fallidos   = [j for j in todos_jobs if j.status_code == "FAILED"]

print(f"  PENDING/RUNNING : {len(pendientes)}")
print(f"  SUCCEEDED       : {len(completados)}")
print(f"  FAILED          : {len(fallidos)}")

if pendientes:
    print(f"\n  Aún hay {len(pendientes)} jobs en proceso.")
    print("  Vuelve a ejecutar este script cuando terminen.")

# Separar por prefijo y descargar
norte_ok = [j for j in completados if j.name and j.name.startswith(PREFIJO_NORTE)]
sur_ok   = [j for j in completados if j.name and j.name.startswith(PREFIJO_SUR)]

print(f"\n  Jobs Norte listos para descargar: {len(norte_ok)}")
print(f"  Jobs Sur   listos para descargar: {len(sur_ok)}")

for jobs_lista, dir_destino, etiqueta in [
    (norte_ok, DIR_NORTE, "Norte (Track 116)"),
    (sur_ok,   DIR_SUR,   "Sur   (Track 142)"),
]:
    if not jobs_lista:
        continue
    print(f"\n  Descargando {etiqueta} → {dir_destino}")
    batch = sdk.Batch(jobs_lista)
    batch.download_files(location=str(dir_destino), create=True)
    print(f"  [OK] {len(jobs_lista)} interferogramas descargados.")
    time.sleep(1)

if fallidos:
    print(f"\n  [AVISO] {len(fallidos)} jobs fallaron:")
    for j in fallidos[:10]:
        print(f"    - {j.name}  |  {j.status_code}")
    print("  Revisa en https://hyp3-api.asf.alaska.edu/jobs")

print("\n[OK] Descarga completada.")
print("     Verifica los archivos .unw.tif, .cor.tif, .dem.tif en los directorios.")
