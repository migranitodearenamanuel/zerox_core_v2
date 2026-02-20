import os
import json
import re
import datetime
import argparse

# --- CONFIGURATION ---
DEFAULT_ROOT = "."
DEFAULT_OUT = "site/assets/knowledge"
BASE_URL = "https://migranitodearenamanuel.github.io/Zerox-Core/"
REPO_URL = "https://github.com/migranitodearenamanuel/Zerox-Core"

# Exclusions
EXCLUDE_DIRS = {
    ".git", "node_modules", "dist", "build", ".venv", "venv", 
    "__pycache__", ".pytest_cache", "site", ".github", ".idea", 
    ".vscode", "tools", "marketing", "coverage", "tmp"
}
EXCLUDE_FILES = {
    ".env", ".env.example", ".env.local", "package-lock.json", "yarn.lock", 
    ".DS_Store", "scan_repo.py", "repobrain.js", "composer.lock"
}
EXCLUDE_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".ico", ".svg", ".webp", ".mp4", ".mov",
    ".pdf", ".exe", ".zip", ".tar", ".gz", ".rar", ".7z",
    ".pyc", ".db", ".sqlite", ".sqlite3", ".pkl", ".bin", ".dat",
    ".ttf", ".otf", ".woff", ".woff2", ".eot", ".map"
}
MAX_FILE_SIZE = 1.5 * 1024 * 1024  # 1.5MB

# Redaction Patterns (Regex) for Safety
SENSITIVE_PATTERNS = [
    (r"(API_KEY|SECRET|TOKEN|PASSWORD|PASS|KEY|AUTH)\s*=\s*['\"][^'\"]+['\"]", r"\1 = '[REDACTED]'"),
    (r"-----BEGIN [A-Z ]+ PRIVATE KEY-----", r"[REDACTED_PRIVATE_KEY]"),
    (r"bg_[a-zA-Z0-9]{20,}", r"[REDACTED_BITGET_KEY]"),
    (r"AIza[0-9A-Za-z-_]{35}", r"[REDACTED_GOOGLE_KEY]"),
    (r"ghp_[a-zA-Z0-9]{30,}", r"[REDACTED_GITHUB_TOKEN]")
]

def redact_content(text):
    count = 0
    for pattern, replacement in SENSITIVE_PATTERNS:
        text, n = re.subn(pattern, replacement, text, flags=re.IGNORECASE)
        count += n
    return text, count

def is_indexable(filename):
    if filename in EXCLUDE_FILES: return False
    if filename.startswith("."): return False
    # Check if ANY exclude extension matches end of string
    if any(filename.lower().endswith(ext) for ext in EXCLUDE_EXTENSIONS): return False
    return True

def get_file_content(filepath):
    try:
        size = os.path.getsize(filepath)
        if size > MAX_FILE_SIZE:
             # Just return metadata for large files
            return f"File too large to index ({size} bytes). See {filepath}"
        
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except:
        return None

def chunk_text(text, chunk_size=400):
    chunks = []
    current_chunk = ""
    
    lines = text.split('\n')
    for line in lines:
        if len(current_chunk) + len(line) > chunk_size:
            if current_chunk.strip():
                chunks.append(current_chunk.strip())
            current_chunk = line + "\n"
        else:
            current_chunk += line + "\n"
            
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    return chunks

def build_inverted_index(chunks):
    index = {}
    stopwords = {"de", "la", "que", "el", "en", "y", "a", "los", "se", "del", "las", "un", "por", "con", "no", "una", "su", "para", "es", "al", "lo", "como", "mas", "o", "pero", "sus", "le", "ha", "me", "si", "sin", "sobre", "este", "ya", "entre", "cuando", "todo", "esta", "ser", "son", "dos", "tambien", "fue", "habia", "era", "muy", "anos", "hasta", "desde", "esta", "mi", "porque", "que", "solo", "han", "yo", "hay", "vez", "puede", "todos", "asi", "nos", "ni", "parte", "tiene", "ele", "uno", "donde", "bien", "tiempo", "mismo", "ese", "ahora", "cada", "e", "vida", "otro", "despues", "te", "otros", "aunque", "esa", "eso", "hace", "otra", "gobierno", "tan", "durante", "siempre", "dia", "tanto", "ella", "tres", "si", "dijo", "sido", "gran", "pais", "segun", "menos", "mundo", "ano", "antes", "estado", "contra", "sino", "forma", "caso", "nada", "hacer", "general", "estaba", "poco", "estos", "presidente", "mayor", "ante", "unos", "les", "algo", "hacia", "casa", "ellos", "ayer", "hecho", "primera", "mucho", "mientras", "ademas", "quien", "momento", "millones", "esto", "espana", "hombre", "estan", "pues", "hoy", "lugar", "madrid", "nacional", "trabajo", "otras", "mejor", "nuevo", "decir", "algunos", "entonces", "todas", "dias", "debe", "politica", "como", "casi", "toda", "tal", "luego", "pasado", "primer", "medio", "va", "estas", "sea", "tenia", "nunca", "poder", "aqui", "ver", "veces", "embargo", "partido", "personas", "grupo", "cuenta", "pueden", "tienen", "misma", "nueva", "cual", "fueron", "mujer", "frente", "jose", "tras", "cosas", "fin", "ciudad", "he", "social", "manera", "tener", "sistema", "sera", "historia", "muchos", "juan", "tipo", "cuatro", "dentro", "nuestro", "punto", "dice", "ello", "cualquier", "noche", "aun", "agua", "parece", "haber", "situacion", "fuera", "bajo", "grandes", "todavia", "vda", "ejemplo", "acuerdo", "habian", "the", "be", "to", "of", "and", "a", "in", "that", "have", "i", "it", "for", "not", "on", "with", "he", "as", "you", "do", "at", "this", "but", "his", "by", "from", "they", "we", "say", "her", "she", "or", "an", "will", "my", "one", "all", "would", "there", "their", "what", "so", "up", "out", "if", "about", "who", "get", "which", "go", "me", "when", "make", "can", "like", "time", "no", "just", "him", "know", "take", "people", "into", "year", "your", "good", "some", "could", "them", "see", "other", "than", "then", "now", "look", "only", "come", "its", "over", "think", "also", "back", "after", "use", "two", "how", "our", "work", "first", "well", "way", "even", "new", "want", "because", "any", "these", "give", "day", "most", "us"}
    
    for doc in chunks:
        # Tokenize (title + text)
        text = (doc['title'] + " " + doc['text']).lower()
        # Remove punctuation
        text = re.sub(r'[^\w\s]', ' ', text)
        tokens = set(text.split())
        
        for token in tokens:
            if len(token) < 3 or token in stopwords: continue
            if token not in index: index[token] = []
            index[token].append(doc['id'])
            
    return index

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', default=DEFAULT_OUT)
    args = parser.parse_args()
    
    output_dir = args.out
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    chunks_es = [] # Could separate if language detection was advanced
    chunks_en = [] # For now we duplicate for bilingual support
    
    sources = []
    chunk_id = 0
    total_redacted = 0
    total_files = 0
    
    print(f"Scanning {DEFAULT_ROOT} -> {output_dir}")
    
    for root, dirs, files in os.walk(DEFAULT_ROOT):
        # Filter dirs
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        for file in files:
            if not is_indexable(file): continue
            
            filepath = os.path.join(root, file)
            rel_path = os.path.relpath(filepath, DEFAULT_ROOT).replace("\\", "/")
            total_files += 1
            
            content = get_file_content(filepath)
            if content is None: continue
            
            # Redact
            clean_content, redacted_count = redact_content(content)
            total_redacted += redacted_count
            
            # Infer Tags
            tags = []
            ext = os.path.splitext(file)[1]
            if ext in ['.py']: tags.append("python")
            if ext in ['.js']: tags.append("javascript")
            if ext in ['.md']: tags.append("documentation")
            if "nucleo" in rel_path: tags.append("core")
            if "site" in rel_path: tags.append("frontend")
            
            # Chunking
            file_chunks = chunk_text(clean_content)
            
            for txt in file_chunks:
                doc = {
                    "id": chunk_id,
                    "path": rel_path,
                    "title": file,
                    "tags": tags,
                    "text": txt,
                    "lang": "neutral" # Code is neutral mostly
                }
                # Add to both for now
                chunks_es.append(doc)
                chunks_en.append(doc)
                chunk_id += 1
            
            sources.append({
                "path": rel_path,
                "chunks": len(file_chunks),
                "mtime": os.path.getmtime(filepath)
            })

    # Indices
    index_es = build_inverted_index(chunks_es)
    index_en = build_inverted_index(chunks_en)
    
    # Save
    with open(f"{output_dir}/kb_es.json", 'w', encoding='utf-8') as f:
        json.dump(chunks_es, f)
    with open(f"{output_dir}/kb_en.json", 'w', encoding='utf-8') as f:
        json.dump(chunks_en, f)
        
    with open(f"{output_dir}/index_es.json", 'w', encoding='utf-8') as f:
        json.dump(index_es, f)
    with open(f"{output_dir}/index_en.json", 'w', encoding='utf-8') as f:
        json.dump(index_en, f)
        
    with open(f"{output_dir}/sources.json", 'w', encoding='utf-8') as f:
        json.dump(sources, f, indent=2)
        
    manifest = {
        "generated_at": datetime.datetime.now().isoformat(),
        "total_files": total_files,
        "total_chunks": chunk_id / 2, # Divided by 2 because duplicated
        "total_redactions": total_redacted,
        "version": "1.0.0"
    }
    with open(f"{output_dir}/manifest.json", 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)

    print(f"DONE. Indexed {total_files} files.")
    print(f"Redacted {total_redacted} secrets.")

if __name__ == "__main__":
    main()
