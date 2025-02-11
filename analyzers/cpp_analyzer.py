import re
from utils.report_generator import generate_report

def analyze_cpp_file(file_path):
    issues = []
    with open(file_path, 'r') as file:
        code = file.read()

    # Detectar métodos públicos
    public_methods = re.findall(r'public:\s*.*?(\w+)\(.*?\)\s*\{', code, re.DOTALL)
    for method in public_methods:
        issues.append(f"Método público '{method}' sin encapsulamiento detectado.")

    # Detectar atributos públicos
    public_attributes = re.findall(r'public:\s*.*?(\w+);', code)
    for attr in public_attributes:
        issues.append(f"Atributo público '{attr}' sin encapsulamiento seguro detectado.")

    # Detectar uso inseguro de punteros
    unsafe_pointers = re.findall(r'\*(\w+)\s*=', code)
    for pointer in unsafe_pointers:
        issues.append(f"Uso inseguro de puntero '{pointer}' detectado.")

    # Detectar macros potencialmente peligrosas
    if re.search(r'#define\s+\w+\s+\d+', code):
        issues.append("Uso de macros detectado. Considera reemplazarlas con constantes.")

    generate_report("C++", issues)
    return issues

