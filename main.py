class acortadorUrl:

    def __init__(self) -> None:
        pass

    def verificar_protocolo(self, url):
        verificar_cadena_url=url[:8]
        if(verificar_cadena_url[:7]=="http://" or verificar_cadena_url[:8]=="https://"):
            return  True
        else:
            return False

    def acortar_url(self, url):
        pass