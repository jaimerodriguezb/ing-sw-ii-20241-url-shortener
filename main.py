class AcortadorUrl:

    def __init__(self) -> None:
        self.detector_url_pishing()
        pass

    def detector_url_pishing(self):
        pass

    '''Se debe usar un REGEX para realizar el HTTPS o HTTP
        Pagina para las expresiones regulares:
        https://regex101.com/'''
    
    def verificar_protocolo(self, url):
        verificar_cadena_url=url[:8]
        if(verificar_cadena_url[:7]=="http://" or verificar_cadena_url[:8]=="https://"):
            return  True
        else:
            return False

    def acortar_url(self, url):
        pass

    def verificar_pishing(self,url_pishing):
        if url_pishing == 1:
            return "Es_Pishing"
        else:
            return "Acortar"