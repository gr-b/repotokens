# repotokens

repotokens is a Python package for analyzing entire source repositories to count tokens and estimate costs for various LLMs. It can be used both as a command-line tool and as an importable Python library.

## Features

- Analyzes entire repositories to count tokens on common source file types.
- Opinionated about excluding those filetypes / utilities that are unlikely to be useful for LLM reasoning on top of the repository.
- Estimates costs of for different LLMs based on token count
- Respects .gitignore files and common ignore patterns
- Can be used as both a Python library and a command-line tool


## Installation

You can install repotokens using pip:

```bash
pip install repotokens
```

## Usage as a Python Library

You can use repotokens in your Python scripts by importing it as follows:

```python
from repotokens import analyze_directory, calculate_costs, MODELS
```

### Analyzing a Directory

To analyze a directory and get token counts:

```python
results = analyze_directory("/path/to/your/repo")
print(f"Total tokens: {results['total_tokens']}")
print(f"Processed files: {results['processed_files']}")

# Print token counts for each file
for file, tokens in results['file_tokens'].items():
    print(f"{file}: {tokens} tokens")
```

### Calculating Costs for a Specific Model

To calculate costs for a specific model:

```python
model = "gpt-4o"
total_tokens = results['total_tokens']
costs = calculate_costs(total_tokens, model)

print(f"Costs for {model}:")
print(f"Input cost: ${costs['input_cost']:.2f}")
print(f"Output cost: ${costs['output_cost']:.2f}")
```

### Getting Information for All Models

You can access information about all available models:

```python
for model, prices in MODELS.items():
    print(f"{model}:")
    print(f"  Input price: ${prices['input_price']} per 1M tokens")
    print(f"  Output price: ${prices['output_price']} per 1M tokens")
```

## Command-Line Usage

repotokens can also be used as a command-line tool:

### Analyze Current Directory

```bash
repotokens
```

### Analyze a Specific Directory

```bash
repotokens /path/to/your/repo
```

### Analyze a Directory and Show Costs for a Specific Model

```bash
repotokens /path/to/your/repo --model gpt-4o-mini
```

### Show Version

```bash
repotokens --version
```