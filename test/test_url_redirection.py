import pytest
from modelo.model import redirection
from unittest.mock import MagicMock

#Pruebas del modelo PKL

@pytest.fixture
def url_in_db():
    return "https://your-shortening-service.com/1"

@pytest.fixture
def url_not_in_db():
    return "none"

def test_is_in_db(url_in_db):

    prueba=redirection()
    result = prueba.redireccionar_url(url_in_db)
    assert result == "https://www.ejemplo.com"

def test_is_none(url_in_db):

    prueba=redirection()
    result = prueba.redireccionar_url(url_not_in_db)
    assert result == "Error_404"