import tkinter as tk
from tkinter import filedialog, messagebox
import os
from analyzers import java_analyzer, cpp_analyzer, python_analyzer
from utils.report_generator import generate_report


def suggest_fix(issue):
    if "método público" in issue.lower():
        return "Considera usar modificadores de acceso privados o protegidos para el método."
    elif "atributo sin encapsulamiento" in issue.lower():
        return "Encapsula el atributo usando un nombre que comience con un guion bajo (_)."
    else:
        return "Consulta las mejores prácticas de programación segura."


class SecurityAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Herramienta de Evaluación de Seguridad para Código POO")
        self.root.configure(bg="#2C3E50")  # Fondo principal

        # Título 
        title_label = tk.Label(root, text="Evaluador de Seguridad en POO", font=("Arial", 20, "bold"),
                                bg="#2C3E50", fg="#ECF0F1")
        title_label.pack(pady=10)

        # Botón para seleccionar archivo
        select_button = tk.Button(root, text="Seleccionar Archivo", command=self.load_file,
                                   bg="#1ABC9C", fg="white", font=("Arial", 12), relief="raised", bd=2)
        select_button.pack(pady=5)

        # Área de texto para mostrar los resultados
        self.result_area = tk.Text(root, width=80, height=15, wrap=tk.WORD,
                                    bg="#34495E", fg="white", font=("Courier", 11))
        self.result_area.pack(pady=10)

        # Botón para limpiar resultados
        clear_button = tk.Button(root, text="Limpiar Resultados", command=self.clear_results,
                                   bg="#E74C3C", fg="white", font=("Arial", 12), relief="raised", bd=2)
        clear_button.pack(pady=5)

        # Botón para salir
        exit_button = tk.Button(root, text="Salir", command=root.quit,
                                 bg="#95A5A6", fg="black", font=("Arial", 12), relief="raised", bd=2)
        exit_button.pack(pady=5)

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Archivos de código", "*.py *.java *.cpp")])
        if not file_path:
            return

        extension = os.path.splitext(file_path)[1]
        self.result_area.insert(tk.END, f"Analizando archivo: {file_path}\n\n")

        issues = []
        if extension == ".py":
            issues = python_analyzer.analyze_python_file(file_path)
        elif extension == ".java":
            issues = java_analyzer.analyze_java_file(file_path)
        elif extension == ".cpp":
            issues = cpp_analyzer.analyze_cpp_file(file_path)
        else:
            messagebox.showerror("Error", "Formato de archivo no soportado")
            return

        # Mostrar resultados en la interfaz
        if issues:
            self.result_area.insert(tk.END, "Problemas detectados:\n")
            for issue in issues:
                suggestion = suggest_fix(issue)
                self.result_area.insert(tk.END, f"- {issue}\n  Sugerencia: {suggestion}\n")
        else:
            self.result_area.insert(tk.END, "No se detectaron problemas de seguridad.\n")

        # Generar reporte JSON
        language = extension[1:].upper()
        generate_report(language, issues)
        self.result_area.insert(tk.END, "\nReporte generado exitosamente.\n")

    def clear_results(self):
        self.result_area.delete(1.0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = SecurityAnalyzerApp(root)
    root.mainloop()
