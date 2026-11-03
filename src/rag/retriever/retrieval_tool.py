def retrieve_documents(
    vector_store,
    query: str,
    k: int = 5,
    threshold: float = 0.15,
):
    results = vector_store.similarity_search_with_relevance_scores(
        query=query,
        k=k,
    )

    print("\nSearch query:", query)

    for index, (document, score) in enumerate(results, start=1):
        print(f"\nResult {index}")
        print("Similarity score:", score)
        print("Source:", document.metadata.get("source"))
        print("Pages:", document.metadata.get("page_numbers"))
        print("Content:", document.page_content)

    relevant_documents = [document for document, score in results if score >= threshold]

    print("\nDocuments passing threshold:", len(relevant_documents))

    return relevant_documents
