# Analyzer Code

**Herramienta de evaluación de seguridad y buenas prácticas para código orientado a objetos (Python, Java y C++)**

| | |
|---|---|
| Lenguajes analizados | Python · Java · C++ |
| Interfaz | Gráfica (Tkinter) |
| Salida | Reportes en formato JSON |
| Distribución | Ejecutable independiente (PyInstaller) |
| Repositorio | [KAAL-38583/analyzer-code](https://github.com/KAAL-38583/analyzer-code) |

---

## Tabla de contenido

1. [Introducción](#introducción)
2. [Objetivos](#objetivos)
3. [Descripción del proyecto](#descripción-del-proyecto)
4. [Características principales](#características-principales)
5. [Tecnologías utilizadas](#tecnologías-utilizadas)
6. [Arquitectura del sistema](#arquitectura-del-sistema)
7. [Estructura del proyecto](#estructura-del-proyecto)
8. [Instalación](#instalación)
9. [Uso](#uso)
10. [Reglas de análisis por lenguaje](#reglas-de-análisis-por-lenguaje)
11. [Formato del reporte JSON](#formato-del-reporte-json)
12. [Generación del ejecutable](#generación-del-ejecutable)
13. [Limitaciones actuales](#limitaciones-actuales)
14. [Trabajo futuro](#trabajo-futuro)
15. [Contribuciones](#contribuciones)
16. [Autor](#autor)

---

## Introducción

Analyzer Code es una herramienta de análisis estático orientada a evaluar código fuente escrito en Python, Java y C++, con énfasis en principios de programación orientada a objetos (POO), como el encapsulamiento y la correcta gestión de la visibilidad de atributos y métodos.

La aplicación examina el código fuente sin necesidad de compilarlo ni ejecutarlo, identificando patrones asociados a un encapsulamiento deficiente, elementos públicos potencialmente inseguros y otras desviaciones respecto a buenas prácticas de programación. Por cada hallazgo, la herramienta ofrece una sugerencia de corrección orientativa.

---

## Objetivos

### Objetivo general

Desarrollar una herramienta de escritorio que permita analizar archivos individuales de código Python, Java o C++, identificando problemas de encapsulamiento y buenas prácticas de programación orientada a objetos, y documentando los hallazgos en un reporte estructurado.

### Objetivos específicos

- Implementar analizadores independientes para Python, Java y C++.
- Detectar métodos y atributos públicos sin un encapsulamiento adecuado.
- Ofrecer sugerencias de corrección asociadas a cada hallazgo.
- Proveer una interfaz gráfica de escritorio simple, basada en Tkinter.
- Generar automáticamente un reporte en formato JSON por cada análisis realizado.
- Permitir la distribución de la herramienta como ejecutable independiente, sin requerir un entorno Python instalado.

---

## Descripción del proyecto

El usuario selecciona, desde la interfaz gráfica, un archivo individual con extensión `.py`, `.java` o `.cpp`. Según la extensión del archivo, la aplicación invoca el analizador correspondiente:

- **Python** (`analyzers/python_analyzer.py`): analiza el árbol de sintaxis abstracta (AST) del archivo para detectar métodos públicos, atributos sin encapsulamiento y parámetros sin validación explícita.
- **Java** (`analyzers/java_analyzer.py`): utiliza expresiones regulares para detectar métodos y atributos públicos, clases sin encapsulamiento, métodos sin documentación, constantes mutables y estructuras condicionales anidadas.
- **C++** (`analyzers/cpp_analyzer.py`): utiliza expresiones regulares para detectar métodos y atributos públicos, uso inseguro de punteros y macros potencialmente peligrosas.

Los resultados se muestran en el área de texto de la interfaz junto con una sugerencia de corrección para cada hallazgo, y se exportan automáticamente como un reporte JSON en la carpeta `reports/`.

---

## Características principales

| Característica | Descripción |
|---|---|
| Análisis multilenguaje | Soporte para archivos individuales en Python, Java y C++. |
| Interfaz gráfica de escritorio | Desarrollada con Tkinter; permite seleccionar archivos, ver resultados y limpiarlos. |
| Sugerencias de corrección | Cada hallazgo se acompaña de una recomendación orientativa. |
| Reportes automáticos en JSON | Cada análisis genera un archivo de reporte con marca de tiempo. |
| Distribución como ejecutable | Empaquetado con PyInstaller (`main.spec`) para ejecución sin entorno Python. |

---

## Tecnologías utilizadas

| Componente | Tecnología |
|---|---|
| Lenguaje de la aplicación | Python |
| Interfaz gráfica | `tkinter` (módulo estándar de Python) |
| Analizador de Python | Módulo `ast` (análisis del árbol de sintaxis abstracta) |
| Analizadores de Java y C++ | Expresiones regulares (`re`) |
| Generación de reportes | Módulo `json` y `datetime` (biblioteca estándar) |
| Empaquetado / distribución | PyInstaller |

No se emplean dependencias externas de terceros: la aplicación se apoya exclusivamente en la biblioteca estándar de Python.

---

## Arquitectura del sistema

```
                    ┌────────────────────────┐
                    │   Interfaz Gráfica      │
                    │   (main.py / Tkinter)   │
                    └────────────┬────────────┘
                                 │
                    Selección de archivo (.py / .java / .cpp)
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                   │
    ┌─────────▼────────┐ ┌───────▼────────┐ ┌────────▼─────────┐
    │ python_analyzer   │ │ java_analyzer  │ │  cpp_analyzer     │
    │  (módulo ast)      │ │ (regex)        │ │  (regex)          │
    └─────────┬────────┘ └───────┬────────┘ └────────┬─────────┘
              │                  │                   │
              └──────────────────┼───────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │   report_generator.py    │
                    │   Genera reports/*.json  │
                    └──────────────────────────┘
```

El componente `main.py` actúa como orquestador: determina la extensión del archivo seleccionado, invoca al analizador correspondiente y muestra los resultados junto con las sugerencias generadas por la función `suggest_fix`.

---

## Estructura del proyecto

```text
analyzer-code/
│
├── analyzers/
│   ├── python_analyzer.py     # Analizador basado en AST para Python
│   ├── java_analyzer.py       # Analizador basado en regex para Java
│   └── cpp_analyzer.py        # Analizador basado en regex para C++
│
├── utils/
│   └── report_generator.py    # Generación de reportes JSON
│
├── reports/                   # Reportes generados por cada análisis
│
├── build/                     # Artefactos intermedios de PyInstaller
├── dist/
│   └── main.exe               # Ejecutable generado para Windows
│
├── main.py                    # Punto de entrada y GUI (Tkinter)
├── main.spec                  # Configuración de empaquetado (PyInstaller)
└── README.md
```

### `analyzers/`
Contiene un módulo por lenguaje soportado, cada uno con una función `analyze_<lenguaje>_file(file_path)` que recibe la ruta del archivo y devuelve una lista de hallazgos (`issues`).

### `utils/`
Contiene `report_generator.py`, responsable de serializar los hallazgos de cada análisis a un archivo JSON con marca de tiempo.

### `reports/`
Carpeta donde se almacenan automáticamente los reportes generados. Se crea de forma automática si no existe.

### `main.py`
Define la clase `SecurityAnalyzerApp`, que construye la interfaz gráfica, gestiona la selección de archivos, invoca al analizador correspondiente según la extensión y despliega los resultados junto con las sugerencias de corrección.

### `main.spec` / `build/` / `dist/`
Archivos generados y utilizados por PyInstaller para producir un ejecutable independiente (`main.exe`) que no requiere un intérprete de Python instalado.

---

## Instalación

### Requisitos

- Python 3.x (incluye `tkinter` en la mayoría de distribuciones estándar).

### Pasos

**1. Clonar el repositorio**

```bash
git clone https://github.com/KAAL-38583/analyzer-code.git
```

**2. Acceder al directorio del proyecto**

```bash
cd analyzer-code
```

**3. Ejecutar la aplicación**

Al no depender de librerías externas, no es necesario instalar paquetes adicionales:

```bash
python main.py
```

> En sistemas Linux, si `tkinter` no está disponible, instálalo mediante el gestor de paquetes correspondiente (por ejemplo, `sudo apt install python3-tk` en distribuciones basadas en Debian/Ubuntu).

### Alternativa: ejecutable precompilado

En `dist/main.exe` se incluye un ejecutable generado para Windows que permite utilizar la aplicación sin necesidad de tener Python instalado.

---

## Uso

1. Iniciar la aplicación (`python main.py` o `dist/main.exe`).
2. Pulsar **"Seleccionar Archivo"** y elegir un archivo con extensión `.py`, `.java` o `.cpp`.
3. La herramienta analiza el archivo y muestra en pantalla los problemas detectados, cada uno acompañado de una sugerencia de corrección.
4. Se genera automáticamente un reporte JSON en la carpeta `reports/`.
5. El botón **"Limpiar Resultados"** permite vaciar el área de resultados para realizar un nuevo análisis.

> **Nota:** la herramienta analiza un archivo a la vez; no admite actualmente la selección de un directorio o proyecto completo.

---

## Reglas de análisis por lenguaje

### Python (`ast`)

| Regla | Descripción |
|---|---|
| Métodos públicos | Se reporta cualquier método cuyo nombre no comience con `_`. |
| Parámetros sin validar | Se reporta cuando un parámetro se llama `input_data`, como indicio de falta de validación explícita. |
| Atributos sin encapsular | Se reporta la asignación a un atributo (`self.x`) cuyo nombre no comience con `_`. |

### Java (expresiones regulares)

| Regla | Descripción |
|---|---|
| Métodos públicos | Detecta declaraciones `public <tipo> <método>(...)`. |
| Atributos públicos | Detecta declaraciones `public <tipo> <atributo>;`. |
| Clases públicas | Detecta declaraciones `public class <Nombre>`. |
| Métodos sin documentación | Detecta métodos públicos sin comentario Javadoc (`/** */`) precedente. |
| Constantes mutables | Detecta campos `public static` sin el modificador `final`. |
| Anidamiento excesivo | Detecta estructuras `if` anidadas dentro de otras estructuras `if`. |

### C++ (expresiones regulares)

| Regla | Descripción |
|---|---|
| Métodos públicos | Detecta métodos definidos bajo la sección `public:`. |
| Atributos públicos | Detecta atributos declarados bajo la sección `public:`. |
| Punteros inseguros | Detecta asignaciones directas a través de un puntero (`*variable = ...`). |
| Uso de macros | Detecta directivas `#define` con valores numéricos, sugiriendo el uso de constantes. |

> Los analizadores de Java y C++ se basan en coincidencias de patrones (regex) y no en un parser completo del lenguaje, por lo que su precisión puede verse afectada por estructuras de código complejas o poco convencionales.

---

## Formato del reporte JSON

Cada análisis genera un archivo en `reports/security_report_<lenguaje>_<fecha>_<hora>.json` con la siguiente estructura:

```json
{
    "language": "Python",
    "timestamp": "2025-02-10 09:43:59",
    "issues_detected": [
        "Atributo 'password' sin encapsulamiento seguro en línea 3",
        "Método público 'public_method' en línea 5."
    ]
}
```

Cuando no se detectan problemas, el campo `issues_detected` contiene el mensaje `"No se detectaron problemas de seguridad."`.

---

## Generación del ejecutable

El proyecto incluye una configuración de **PyInstaller** (`main.spec`) para generar un ejecutable independiente a partir de `main.py`. Para regenerarlo:

```bash
pip install pyinstaller
pyinstaller main.spec
```

El ejecutable resultante se genera en la carpeta `dist/`, y los archivos intermedios del proceso de empaquetado se almacenan en `build/`.

> El archivo `main.spec` incluido referencia una ruta de icono local (`icon=[...]`) específica del entorno en que fue generado originalmente; deberá actualizarse antes de volver a compilar en otro equipo.

---

## Limitaciones actuales

- El análisis se realiza sobre un único archivo a la vez; no admite el análisis recursivo de directorios o proyectos completos.
- Los analizadores de Java y C++ se basan en expresiones regulares, por lo que no interpretan la sintaxis completa del lenguaje y pueden generar falsos positivos o negativos ante código complejo.
- Las reglas actuales se centran en encapsulamiento y visibilidad; no cubren vulnerabilidades de seguridad más avanzadas (inyección de código, deserialización insegura, gestión de credenciales, etc.).
- El ejecutable distribuido (`dist/main.exe`) está compilado para Windows.

---

## Trabajo futuro

- Migrar los analizadores de Java y C++ a parsers formales (por ejemplo, `javalang` o herramientas basadas en Clang) para mayor precisión.
- Ampliar el catálogo de reglas hacia vulnerabilidades de seguridad más allá del encapsulamiento.
- Soporte para análisis de directorios o proyectos completos.
- Exportación de reportes en formatos adicionales (HTML, PDF).
- Empaquetado multiplataforma (Linux, macOS).

## Contribuciones

Las contribuciones son bienvenidas mediante *pull requests*. Para cambios significativos, se recomienda abrir primero un *issue* para discutir la propuesta.

## Autor

**KAAL-38583** — [github.com/KAAL-38583](https://github.com/KAAL-38583)
