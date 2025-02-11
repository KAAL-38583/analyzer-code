import json
import os
from datetime import datetime

def generate_report(language, issues):
    """
    Genera un reporte de seguridad en formato JSON.
    Args:
        language (str): Lenguaje analizado (Python, Java, C++).
        issues (list): Lista de problemas de seguridad detectados.
    """
    # Crear la carpeta de reportes si no existe
    report_dir = 'reports'
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)

    # Construcción del reporte
    report = {
        "language": language,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "issues_detected": issues if issues else ["No se detectaron problemas de seguridad."]
    }

    # Nombre del archivo basado en el lenguaje y la fecha
    report_filename = f"{report_dir}/security_report_{language.lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    # Guardar el reporte en JSON
    with open(report_filename, 'w') as report_file:
        json.dump(report, report_file, indent=4)

    print(f"Reporte de seguridad generado: {report_filename}")
