import re
from utils.report_generator import generate_report

def analyze_java_file(file_path):
    issues = []
    with open(file_path, 'r') as file:
        code = file.read()

    # Detectar métodos públicos sin validación
    public_methods = re.findall(r'public\s+[\w<>]+\s+(\w+)\(.*?\)\s*\{', code)
    for method in public_methods:
        issues.append(f"Método público '{method}' detectado. Considere revisar los permisos de acceso.")

    # Detectar atributos públicos sin encapsulamiento
    public_attributes = re.findall(r'public\s+[\w<>]+\s+(\w+);', code)
    for attr in public_attributes:
        issues.append(f"Atributo público '{attr}' sin encapsulamiento seguro.")

    # Detectar clases públicas sin encapsulamiento
    public_classes = re.findall(r'public\s+class\s+(\w+)', code)
    for class_name in public_classes:
        issues.append(f"Clase pública '{class_name}' detectada. Considere aplicar encapsulamiento si no es necesario.")

    # Detectar métodos sin documentación (/** */)
    undocumented_methods = re.findall(r'public\s+[\w<>]+\s+(\w+)\(.*?\)\s*(?!/\\*\\*)\{', code)
    for method in undocumented_methods:
        issues.append(f"Método '{method}' no tiene documentación. Considere agregar comentarios con /** */.")

    # Detectar constantes sin 'final'
    mutable_constants = re.findall(r'public\s+static\s+[\w<>]+\s+(\w+);', code)
    for constant in mutable_constants:
        issues.append(f"Constante '{constant}' no declarada como 'final'. Considere proteger su valor.")

    # Detectar estructuras anidadas complejas (if-else)
    nested_if_else = re.findall(r'if\s*\(.*?\)\s*\{(?:[^{}]*\{[^{}]*\})+', code)
    if nested_if_else:
        issues.append("Se detectaron estructuras if-else anidadas. Considere simplificar el flujo de control.")

    generate_report("Java", issues)
    return issues
