def get_language(path, lang=""):
    try:
        dot = path.rfind(".")
    except ValueError as e:
        return 400
    end = path[dot + 1:]
    if end == "py":
        return "python"
    if end == "cpp":
        return "c++"
    if end == "cs":
        return "c#"