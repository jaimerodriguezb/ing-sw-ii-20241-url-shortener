import pytest
from main import acortadorUrl
from unittest.mock import MagicMock


def test_protocole_none(mocker):
    mocker.patch('main.acortadorUrl.verificar_protocolo', return_value = False)
    url_failed = acortadorUrl()
    result = url_failed.verificar_protocolo()
    assert result == False
