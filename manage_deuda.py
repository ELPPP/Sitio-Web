import os
import re
from github import Github

# === Configuración base ===
REPO_NAME = os.getenv("GITHUB_REPOSITORY")
TOKEN = os.getenv("GITHUB_TOKEN")

if not TOKEN:
    raise SystemExit("❌ No se encontró GITHUB_TOKEN. Verifica que exista en los secrets.")

g = Github(TOKEN)
repo = g.get_repo(REPO_NAME)

# === Expresiones regulares ===
pattern_deuda = re.compile(
    r"---DEUDA TECNICA(?:\(#(\d+)\))?---\s*([\s\S]*?)---FIN---",
    re.MULTILINE,
)

# === Recolectar archivos a analizar ===
def get_repo_files():
    files = []
    for root, _, filenames in os.walk("."):
        for f in filenames:
            if f.endswith((".py", ".js", ".jsx", ".ts", ".tsx")):
                files.append(os.path.join(root, f))
    return files

def crear_issue(texto, archivo):
    title = texto.splitlines()[0][:60] if texto.strip() else f"Deuda técnica en {archivo}"
    issue = repo.create_issue(
        title=title,
        body=f"**Archivo:** `{archivo}`\n\n```\n{texto.strip()}\n```"
    )
    return issue.number

def actualizar_issue(issue_id, nuevo_texto):
    issue = repo.get_issue(issue_id)
    issue.edit(body=f"Actualizado automáticamente:\n\n```\n{nuevo_texto.strip()}\n```")

def cerrar_issue(issue_id):
    issue = repo.get_issue(issue_id)
    issue.edit(state="closed")

# === Procesar cada archivo ===
for path in get_repo_files():
    with open(path, encoding="utf-8") as f:
        content = f.read()

    nuevo_content = content
    cambios = False

    for match in pattern_deuda.finditer(content):
        issue_id, texto = match.groups()
        if "ALL's OK" in texto:
            if issue_id:
                cerrar_issue(int(issue_id))
            # Eliminar bloque del código
            nuevo_content = nuevo_content.replace(match.group(0), "")
            cambios = True
            continue

        if not issue_id:
            nuevo_id = crear_issue(texto, path)
            bloque_nuevo = match.group(0).replace("---DEUDA TECNICA---", f"---DEUDA TECNICA(#{nuevo_id})---")
            nuevo_content = nuevo_content.replace(match.group(0), bloque_nuevo)
            cambios = True
        else:
            actualizar_issue(int(issue_id), texto)

    if cambios:
        with open(path, "w", encoding="utf-8") as f:
            f.write(nuevo_content)

print("✅ Revisión de deuda técnica completada.")
