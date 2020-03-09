from typing import Optional, TypedDict

import pytest
from pydantic import BaseModel, ValidationError

from pydantic_typeddict import as_typed_dict, parse_dict


class User(TypedDict):
    first_name: Optional[str]
    last_name: Optional[str]
    email: str
    age: int


def test_build_pydantic_model():
    model = parse_dict(User)

    assert issubclass(model, BaseModel)
    assert sorted(model.schema()['required']) == ['age', 'email']


def test_validate_required_fields():
    with pytest.raises(ValidationError, match='age'):
        as_typed_dict({
            'first_name': 'Bob',
            'email': 'test@example.com',
        }, User)


def test_type_casting():
    result = as_typed_dict({
        'first_name': 'Bob',
        'email': 'test@example.com',
        'age': '18'
    }, User)

    assert result == {
        'first_name': 'Bob',
        'last_name': None,
        'email': 'test@example.com',
        'age': 18,
    }
