from langchain_community.vectorstores import FAISS

from src.rag.vector_store.file_manager import (
    detect_pdf_changes,
    scan_department_files,
)
from src.rag.vector_store.index_builder import build_department_index
from src.rag.vector_store.index_updater import update_vector_store
from src.rag.vector_store.ingestion_config import (
    DATA_DIR,
    VECTOR_STORE_DIR,
    embeddings,
)
from src.rag.vector_store.manifest_manager import (
    load_manifest,
    save_manifest,
)


def ingest_department(department: str) -> FAISS:
    """Build or incrementally update a department's FAISS index."""

    department_path = DATA_DIR / department
    save_path = VECTOR_STORE_DIR / department
    manifest_path = save_path / "manifest.json"

    # Scan department PDFs and calculate their hashes.
    current_files = scan_department_files(department_path)

    # Check whether the index and manifest already exist.
    index_exists = (save_path / "index.faiss").exists() and (
        save_path / "index.pkl"
    ).exists()
    manifest_exists = manifest_path.exists()

    save_path.mkdir(parents=True, exist_ok=True)

    # Load previously saved ingestion records.
    manifest = load_manifest(manifest_path)
    previous_documents = manifest["documents"]

    # Handle a department where all previously indexed PDFs were deleted.
    if not current_files:
        if not index_exists or not manifest_exists:
            raise ValueError(f"No PDFs or usable existing index found for {department}")

        vector_store = FAISS.load_local(
            str(save_path),
            embeddings,
            allow_dangerous_deserialization=True,
        )

        if previous_documents:
            vector_store, _ = update_vector_store(
                vector_store=vector_store,
                department=department,
                files_to_add={},
                files_to_remove=previous_documents,
            )

            vector_store.save_local(str(save_path))

            save_manifest(
                {"documents": {}},
                manifest_path,
            )

            print(f"All documents removed from {department.upper()}.")

        return vector_store

    # Build a fresh index if the index or manifest is missing.
    if not index_exists or not manifest_exists:
        vector_store, document_records = build_department_index(
            department=department,
            pdf_files=current_files,
        )

        if vector_store is None:
            raise ValueError(f"Unable to build FAISS index for {department}")

        updated_manifest = {
            "documents": document_records,
        }

    else:
        # Load the existing FAISS index.
        vector_store = FAISS.load_local(
            str(save_path),
            embeddings,
            allow_dangerous_deserialization=True,
        )

        # Identify new, modified, unchanged, and deleted PDFs.
        changes = detect_pdf_changes(
            current_files=current_files,
            manifest=manifest,
        )

        print(f"\nIngestion report: {department.upper()}")

        for category, files in changes.items():
            print(f"{category.capitalize()}: {list(files.keys())}")

        files_to_add = {
            **changes["new"],
            **changes["modified"],
        }

        files_to_remove = {
            filename: previous_documents[filename]
            for filename in (list(changes["modified"]) + list(changes["deleted"]))
        }

        if not files_to_add and not files_to_remove:
            print(
                f"No PDF changes detected for {department.upper()}. "
                "Reusing existing index."
            )
            return vector_store

        # Apply incremental changes.
        vector_store, new_records = update_vector_store(
            vector_store=vector_store,
            department=department,
            files_to_add=files_to_add,
            files_to_remove=files_to_remove,
        )

        # Preserve unchanged document records.
        updated_documents = {
            filename: previous_documents[filename] for filename in changes["unchanged"]
        }

        updated_documents.update(new_records)

        updated_manifest = {
            "documents": updated_documents,
        }

    # Save the updated FAISS index before updating the manifest.
    vector_store.save_local(str(save_path))

    save_manifest(
        updated_manifest,
        manifest_path,
    )

    print(f"FAISS index saved successfully for {department.upper()}.")

    return vector_store
