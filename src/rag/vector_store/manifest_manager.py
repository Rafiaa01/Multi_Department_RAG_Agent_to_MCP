import json
from pathlib import Path


def load_manifest(manifest_path: Path) -> dict:
    """Load the ingestion manifest for a department."""

    if not manifest_path.exists():
        return {"documents": {}}

    try:
        with open(manifest_path, "r", encoding="utf-8") as file:
            manifest = json.load(file)

    except (json.JSONDecodeError, OSError) as exc:
        raise RuntimeError(
            f"Unable to load ingestion manifest: {manifest_path}"
        ) from exc

    if not isinstance(manifest, dict) or not isinstance(
        manifest.get("documents"), dict
    ):
        raise ValueError(f"Invalid manifest structure: {manifest_path}")  # noqa: TRY004

    return manifest


def save_manifest(manifest: dict, manifest_path: Path) -> None:
    """Save the manifest safely using an atomic file replacement."""

    manifest_path.parent.mkdir(parents=True, exist_ok=True)

    temporary_path = manifest_path.with_suffix(".tmp")

    with open(temporary_path, "w", encoding="utf-8") as file:
        json.dump(
            manifest,
            file,
            indent=4,
            ensure_ascii=False,
        )

    temporary_path.replace(manifest_path)
