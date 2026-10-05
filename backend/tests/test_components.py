from pydantic import ValidationError
import pytest

from app.modules.components.schemas import ComponentCreate


def test_component_create_uses_expected_defaults():
    component = ComponentCreate(
        definition_key="text",
    )

    assert component.definition_key == "text"
    assert component.config == {}
    assert component.binding is None


def test_component_create_requires_definition_key():
    with pytest.raises(ValidationError):
        ComponentCreate()