import os
import tiktoken
from pathlib import Path
import fnmatch

DEFAULT_IGNORE_PATTERNS = [
    # IDE and editor
    '.idea/', '.vscode/', '.atom/', '*.sublime-project', '*.sublime-workspace',
    # Version control
    '.git/', '.svn/', '.hg/',
    # Build and compilation
    'build/', 'dist/', 'out/', 'target/', 'bin/', 'obj/',
    # Package managers
    'node_modules/', 'vendor/', 'bower_components/', 'jspm_packages/',
    # Temp and cache
    'tmp/', 'temp/', '.cache/', '__pycache__/',
    # OS specific
    '.DS_Store', 'Thumbs.db',
    # Logs
    '*.log', 'logs/',
    # Environment and local config
    '.env', '.env.local', 'config.local.js',
    # Coverage and test reports
    'coverage/', '.nyc_output/', '.pytest_cache/',
    # Documentation
    'docs/_build/', 'site/',
    # Lock files (optional)
    'package-lock.json', 'yarn.lock', 'Pipfile.lock', 'poetry.lock',
    # Database
    '*.sqlite', '*.db',
    # Backups
    '*.bak', '*.swp', '*~',
    # Compiled Python
    '*.pyc', '*.pyo', '*.pyd',
    # Jupyter
    '.ipynb_checkpoints/',
    # React/Next.js
    '.next/',
    # Angular
    '.angular/',
    # Additional directories
    '.github/'
]

def load_gitignore(root_dir):
    gitignore_path = os.path.join(root_dir, '.gitignore')
    patterns = DEFAULT_IGNORE_PATTERNS.copy()
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as file:
            patterns.extend([line.strip() for line in file if line.strip() and not line.startswith('#')])
    return patterns

def is_ignored(file_path, root_dir, ignore_patterns):
    rel_path = os.path.relpath(file_path, root_dir)
    for pattern in ignore_patterns:
        if pattern.endswith('/'):
            if any(part.startswith(pattern[:-1]) for part in rel_path.split(os.sep)):
                return True
        elif pattern.startswith('/'):
            if fnmatch.fnmatch(rel_path, pattern[1:]):
                return True
        elif fnmatch.fnmatch(rel_path, f"*{pattern}"):
            return True
    return False

def is_code_file(file_path):
    code_extensions = {
        '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.c', '.cpp', '.cs', '.go', '.rb', '.php',
        '.swift', '.kt', '.rs', '.scala', '.html', '.css', '.scss', '.sass', '.less',
        '.sql', '.sh', '.bash', '.yml', '.yaml', '.json', '.xml', '.md', '.txt',
        '.gitignore', '.dockerignore', '.env', '.ini', '.cfg', '.conf',
        'Dockerfile', 'docker-compose.yml', 'package.json', 'requirements.txt',
        'Gemfile', 'Pipfile', 'Cargo.toml', 'pom.xml', 'build.gradle'
    }
    return file_path.suffix.lower() in code_extensions or file_path.name in code_extensions

def count_tokens(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return len(tiktoken.encoding_for_model("gpt-3.5-turbo").encode(content))
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return 0

def format_cost(cost):
    if cost < 0.01:
        return f"${cost:.4f}"
    elif cost < 0.1:
        return f"${cost:.3f}"
    else:
        return f"${cost:.2f}"

def main():
    root_dir = '.'
    ignore_patterns = load_gitignore(root_dir)
    total_tokens = 0
    processed_files = 0

    for root, dirs, files in os.walk(root_dir):
        # Remove ignored directories
        dirs[:] = [d for d in dirs if not is_ignored(os.path.join(root, d), root_dir, ignore_patterns)]

        for file in files:
            file_path = Path(root) / file
            if not is_ignored(file_path, root_dir, ignore_patterns) and is_code_file(file_path):
                tokens = count_tokens(file_path)
                total_tokens += tokens
                processed_files += 1
                print(f"{file_path}: {tokens} tokens")

    # OpenAI model information
    models = {
        "gpt-4o": {"input_price": 5.00, "output_price": 15.00},
        "gpt-4o-2024-08-06": {"input_price": 2.50, "output_price": 10.00},
        "gpt-4o-2024-05-13": {"input_price": 5.00, "output_price": 15.00},
        "gpt-4o-mini": {"input_price": 0.150, "output_price": 0.600},
        "gpt-4o-mini-2024-07-18": {"input_price": 0.150, "output_price": 0.600},
    }

    print(f"\nEstimated costs for {total_tokens} tokens from {processed_files} different source files:")
    for model, prices in models.items():
        input_cost = (total_tokens / 1000000) * prices["input_price"]
        output_cost = (total_tokens / 1000000) * prices["output_price"]
        print(f"{model}:")
        print(f"  Input cost: {format_cost(input_cost)}")
        print(f"  Output cost: {format_cost(output_cost)}")

    print(f"\nTotal tokens: {total_tokens}")
    print(f"Processed files: {processed_files}")

if __name__ == "__main__":
    main()