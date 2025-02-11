import ast
from utils.report_generator import generate_report

class SecurityAnalyzerPython(ast.NodeVisitor):
    def __init__(self):
        self.issues = []

    def visit_FunctionDef(self, node):
        # Detectar métodos públicos potencialmente inseguros
        if not node.name.startswith('_'):
            self.issues.append(f"Método público '{node.name}' en línea {node.lineno}.")

        # Verificar parámetros sin validación explícita
        for arg in node.args.args:
            if arg.arg == "input_data":
                self.issues.append(f"Falta validación de entrada en la función '{node.name}' en línea {node.lineno}.")

        self.generic_visit(node)

    def visit_Assign(self, node):
        # Detección de variables sin encapsulamiento seguro
        for target in node.targets:
            if isinstance(target, ast.Attribute) and not target.attr.startswith('_'):
                self.issues.append(f"Atributo '{target.attr}' sin encapsulamiento seguro en línea {node.lineno}")
        self.generic_visit(node)

    def analyze(self, code):
        tree = ast.parse(code)
        self.visit(tree)
        return self.issues

def analyze_python_file(file_path):
    with open(file_path, 'r') as file:
        code = file.read()

    analyzer = SecurityAnalyzerPython()
    issues = analyzer.analyze(code)

    generate_report("Python", issues)  # Genera el reporte
    return issues  # Devuelve las issues
