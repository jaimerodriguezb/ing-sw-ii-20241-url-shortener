import pytest
from main import acortadorUrl
from unittest.mock import MagicMock

def test_protocole_none(mocker):
    mocker.patch('main.acortadorUrl.verificar_protocolo', return_value = False)
    url_failed = acortadorUrl()
    result = url_failed.verificar_protocolo()
    assert result == False

def test_good_protocol_https():
    accepted_protocol = acortadorUrl()
    result = accepted_protocol.verificar_protocolo("https://www.google.com")
    assert result == True

def test_good_protocol_http():
    accepted_protocol = acortadorUrl()
    result = accepted_protocol.verificar_protocolo("http://www.google.com")
    assert result == True