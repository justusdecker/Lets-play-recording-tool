def file_read(filepath : str) -> str:
    with open(filepath, 'r') as f:
        return f.read()