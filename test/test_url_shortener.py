import pytest
from modelo.training.model import AcortadorUrl
from unittest.mock import MagicMock

def test_protocole_none(mocker):
    mocker.patch('modelo.training.model.AcortadorUrl.verificar_protocolo', return_value = False)
    url_failed = AcortadorUrl()
    result = url_failed.verificar_protocolo()
    assert result == False

def test_good_protocol_https():
    accepted_protocol = AcortadorUrl()
    result = accepted_protocol.verificar_protocolo("https://www.google.com")
    assert result == True

def test_good_protocol_http():
    accepted_protocol = AcortadorUrl()
    result = accepted_protocol.verificar_protocolo("http://www.google.com")
    assert result == True

def test_is_not_pishing(mocker):
    mocker.patch('modelo.training.model.AcortadorUrl.verificar_pishing', return_value = "Acortar")
    url_pishing=AcortadorUrl()
    confirm = url_pishing.verificar_pishing()
    result = url_pishing.verificar_pishing(confirm)
    assert result == "Acortar"

def test_is_pishing(mocker):
    mocker.patch('modelo.training.model.AcortadorUrl.verificar_pishing', return_value = "Es_Pishing")
    url_pishing=AcortadorUrl()
    confirm = url_pishing.verificar_pishing()
    result = url_pishing.verificar_pishing(confirm)
    assert result == "Es_Pishing"