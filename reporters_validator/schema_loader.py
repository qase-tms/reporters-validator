import yaml
from pathlib import Path


def load_schema(schema_path: Path) -> dict:
    """Load a YAML schema file, resolve $ref references and convert nullable fields to JSON Schema."""
    schema_path = Path(schema_path)
    if not schema_path.is_file():
        raise FileNotFoundError(f"Schema file not found: {schema_path}")

    with open(schema_path, "r", encoding="utf-8") as f:
        schema = yaml.safe_load(f)

    base_dir = schema_path.parent
    schema = _resolve_refs(schema, base_dir, visiting=set())
    schema = _convert_nullable(schema)
    return schema


def _resolve_refs(
    node: dict | list | str | int | float | bool | None,
    base_dir: Path,
    visiting: set[Path],
):
    """Recursively resolve $ref references by loading and inlining referenced YAML files.

    Uses a ``visiting`` set to detect and break self-referential cycles (e.g. step.yaml
    referencing itself for nested steps).  When a cycle is detected the $ref node is
    left as-is so the schema remains usable without infinite recursion.
    """
    if isinstance(node, dict):
        if "$ref" in node:
            ref_path = (base_dir / node["$ref"]).resolve()
            if ref_path in visiting:
                # Cycle detected — return a placeholder that won't cause infinite recursion
                return {"type": "object"}
            with open(ref_path, "r", encoding="utf-8") as f:
                resolved = yaml.safe_load(f)
            return _resolve_refs(resolved, ref_path.parent, visiting | {ref_path})
        return {k: _resolve_refs(v, base_dir, visiting) for k, v in node.items()}
    elif isinstance(node, list):
        return [_resolve_refs(item, base_dir, visiting) for item in node]
    return node


def _convert_nullable(node: dict | list | str | int | float | bool | None):
    """Convert OpenAPI-style nullable: true to JSON Schema type arrays."""
    if isinstance(node, dict):
        result = {}
        is_nullable = node.get("nullable", False)
        for k, v in node.items():
            if k == "nullable":
                continue
            result[k] = _convert_nullable(v)
        if is_nullable and "type" in result:
            t = result["type"]
            if isinstance(t, str):
                result["type"] = [t, "null"]
            elif isinstance(t, list) and "null" not in t:
                result["type"] = t + ["null"]
        return result
    elif isinstance(node, list):
        return [_convert_nullable(item) for item in node]
    return node
