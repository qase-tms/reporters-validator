import pytest
from pathlib import Path

from reporters_validator.schema_loader import load_schema

FIXTURES = Path(__file__).parent / "fixtures"
SCHEMAS = FIXTURES / "schemas"


def test_load_root_schema_returns_dict():
    schema = load_schema(SCHEMAS / "root.yaml")
    assert isinstance(schema, dict)
    assert schema["type"] == "object"


def test_load_root_schema_has_properties():
    schema = load_schema(SCHEMAS / "root.yaml")
    assert "title" in schema["properties"]
    assert "stats" in schema["properties"]


def test_load_result_schema_resolves_refs():
    schema = load_schema(SCHEMAS / "result.yaml")
    # $ref to attachment.yaml should be resolved inline
    attachment_schema = schema["properties"]["attachments"]["items"]
    assert "properties" in attachment_schema
    assert "id" in attachment_schema["properties"]


def test_load_result_schema_resolves_nested_refs():
    schema = load_schema(SCHEMAS / "result.yaml")
    # $ref to step.yaml which itself has $ref to attachment.yaml
    step_schema = schema["properties"]["steps"]["items"]
    assert "properties" in step_schema
    assert "execution" in step_schema["properties"]


def test_nullable_converted_to_json_schema():
    schema = load_schema(SCHEMAS / "result.yaml")
    # signature has nullable: true
    sig = schema["properties"]["signature"]
    assert sig["type"] == ["string", "null"]


def test_load_schema_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_schema(Path("/nonexistent.yaml"))
