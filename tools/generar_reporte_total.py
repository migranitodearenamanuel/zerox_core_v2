import os
import re

# Configuración
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_FILE = os.path.join(ROOT_DIR, "auditoria_completa_con_explicaciones.md")

EXCLUDE_DIRS = {
    "node_modules",
    ".git",
    "__pycache__",
    "dist",
    "build",
    ".vscode",
    ".idea",
    "venv",
    "env",
    "tmp",
    "coverage",
    ".next",
    "motores_internos",
}

EXCLUDE_FILES = {
    "package-lock.json",
    "yarn.lock",
    ".DS_Store",
    "auditoria_completa_con_explicaciones.md",
    "tree_output.txt",
    "stats.json",
}

EXCLUDE_EXTENSIONS = {
    ".pyc",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".ico",
    ".svg",
    ".woff",
    ".woff2",
    ".ttf",
    ".eot",
    ".mp4",
    ".mov",
    ".zip",
    ".tar",
    ".gz",
    ".rar",
    ".7z",
    ".pdf",
    ".exe",
    ".dll",
    ".bin",
    ".dat",
    ".db",
    ".sqlite",
    ".sqlite3",
}


def is_text_file(filename):
    return not any(filename.lower().endswith(ext) for ext in EXCLUDE_EXTENSIONS)


def get_explanation(filepath, content):
    filename = os.path.basename(filepath)
    ext = os.path.splitext(filename)[1].lower()

    explanation = "Archivo del sistema."

    # Intentar extraer docstrings o comentarios iniciales
    if ext == ".py":
        # Buscar docstring comulativo o comentarios al inicio
        match = re.search(r'^(\s*""".*?""")', content, re.DOTALL)
        if match:
            explanation = f"Docstring detectado:\n{match.group(1)}"
        else:
            # Buscar primeros comentarios
            comments = []
            for line in content.splitlines():
                if line.strip().startswith("#"):
                    comments.append(line.strip())
                elif not line.strip():
                    continue
                else:
                    break
            if comments:
                explanation = "Comentarios iniciales:\n" + "\n".join(comments)
            else:
                explanation = "Script de Python sin documentación explícita al inicio."

    elif ext in [".js", ".jsx", ".ts", ".tsx", ".css", ".java", ".c", ".cpp"]:
        # Buscar bloque /** ... */
        match = re.search(r"/\*\*.*?\*/", content, re.DOTALL)
        if match:
            explanation = f"Documentación detectada:\n{match.group(0)}"
        else:
            # Buscar primeros comentarios //
            comments = []
            for line in content.splitlines():
                if line.strip().startswith("//"):
                    comments.append(line.strip())
                elif not line.strip():
                    continue
                else:
                    break
            if comments:
                explanation = "Comentarios iniciales:\n" + "\n".join(comments)
            else:
                explanation = (
                    "Código fuente (JS/TS/CSS) sin documentación explícita al inicio."
                )

    elif ext in [".html", ".xml"]:
        match = re.search(r"<!--.*?-->", content, re.DOTALL)
        if match:
            explanation = f"Comentario HTML detectado:\n{match.group(0)}"
        else:
            explanation = "Archivo de marcado (HTML/XML)."

    elif ext in [".bat", ".cmd"]:
        comments = []
        for line in content.splitlines():
            if line.strip().upper().startswith("REM") or line.strip().startswith("::"):
                comments.append(line.strip())
            elif not line.strip():
                continue
            else:
                break
        if comments:
            explanation = "Comentarios del script Batch:\n" + "\n".join(comments)
        else:
            explanation = "Script de comandos de Windows."

    elif ext == ".json":
        explanation = "Archivo de configuración o datos en formato JSON."

    elif ext == ".md":
        explanation = "Documentación en formato Markdown."

    elif ext == ".txt":
        explanation = "Archivo de texto plano."

    return explanation


def main():
    print(f"Generando reporte en: {OUTPUT_FILE}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        out.write("# AUDITORÍA COMPLETA DE CÓDIGO - ZEROX CORE\n")
        out.write(
            f"Generado automáticamente. Incluye contenido y explicación extraída.\n\n"
        )

        for root, dirs, files in os.walk(ROOT_DIR):
            # Filtrar directorios
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

            for file in files:
                if file in EXCLUDE_FILES or not is_text_file(file):
                    continue

                filepath = os.path.join(root, file)
                relpath = os.path.relpath(filepath, ROOT_DIR)

                try:
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()

                    explanation = get_explanation(filepath, content)

                    out.write(f"\n{'=' * 80}\n")
                    out.write(f"# ARCHIVO: {relpath}\n")
                    out.write(f"{'=' * 80}\n\n")

                    out.write(f"## 📝 Explicación / Contexto\n")
                    out.write(f"{explanation}\n\n")

                    out.write(f"## 💻 Contenido del Archivo\n")
                    out.write(f"```\n")
                    out.write(content)
                    out.write(f"\n```\n\n")

                    print(f"Procesado: {relpath}")

                except Exception as e:
                    print(f"Error leyendo {filepath}: {e}")
                    out.write(f"\nERROR LEYENDO ARCHIVO: {relpath} - {e}\n")

    print("Completado.")


if __name__ == "__main__":
    main()
