def format_sources(documents):
    
    sources = []

    for doc in documents:
        source = doc.metadata.get("source", "Unknown")
        pages = doc.metadata.get("page_numbers", [])

        sources.append(
            f"Source: {source}, Pages: {pages}"
        )

    return list(set(sources))