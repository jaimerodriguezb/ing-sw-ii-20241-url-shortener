import pytest
from modelo.model import AcortadorUrl
from unittest.mock import MagicMock

def test_protocole_none(mocker):
    mocker.patch('modelo.model.AcortadorUrl.verificar_protocolo', return_value = False)
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
    mocker.patch('modelo.model.AcortadorUrl.verificar_pishing', return_value = "Acortar")
    url_pishing=AcortadorUrl()
    confirm = url_pishing.verificar_pishing()
    result = url_pishing.verificar_pishing(confirm)
    assert result == "Acortar"

def test_is_pishing(mocker):
    mocker.patch('modelo.model.AcortadorUrl.verificar_pishing', return_value = "Es_Pishing")
    url_pishing=AcortadorUrl()
    confirm = url_pishing.verificar_pishing()
    result = url_pishing.verificar_pishing(confirm)
    assert result == "Es_Pishing"

#Pruebas del modelo PKL

@pytest.fixture
def url_safe():
    return "http://www.ruclip.com/video/XQbLwctcqUI/how-to-knock-a-big-man-out.html"

@pytest.fixture
def url_phishing():
    return "http://69.162.73.82/sigmail/sistema/admin/resources/email_templates/brazilian_portuguese/Basico/poate/iasa/ceva/da/nu/cred/"

def test_is_pishing_model(url_phishing):

    prueba=AcortadorUrl()
    result = prueba.verificar_pishing(url_phishing)
    assert result == "Es_Pishing"

def test_is_not_pishing_model(url_safe):

    prueba=AcortadorUrl()
    result = prueba.verificar_pishing(url_safe)
    assert result == "Acortar"

def test_is_not_pishing_model_negative(url_phishing):

    prueba=AcortadorUrl()
    result = prueba.verificar_pishing(url_phishing)
    assert result != "Acortar"

def test_is_pishing_model_negative(url_safe):

    prueba=AcortadorUrl()
    result = prueba.verificar_pishing(url_safe)
    assert result != "Es_Pishing"