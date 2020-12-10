import pudb # noqa

def chunker(col, delim=""):
    """Chunks the items in collection `col` by delimiter `delim`"""
    chunk = []
    for item in col:
        if item == delim:
            yield chunk
            chunk.clear()
        else:
            chunk.append(item)
    yield chunk
