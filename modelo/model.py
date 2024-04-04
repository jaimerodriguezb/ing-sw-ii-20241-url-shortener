import pandas as pd
import joblib
import os
from urllib.parse import urlparse
import re
from googlesearch import search
import numpy as np
from tld import get_tld

class AcortadorUrl:

    def __init__(self) -> None:
        self.__model = None
        self.__load_model()

    def __load_model(self):
        """Load the model to self.__model once it's been trainned"""
        self.__model = joblib.load(os.path.dirname(__file__) + "\\training\\predictor_phishing_model.pkl") 
    
    def verificar_protocolo(self, url):
        verificar_cadena_url=url[:8]
        if(r"^(http|https)://"):
            return  True
        else:
            return False

    def acortar_url(url):
        pass

    def verificar_pishing(self, url_pishing):
        url_parsed = self.parse_url(url_pishing)
        url_parsed = np.array(url_parsed).reshape((1, -1))
        pred = self.__model.predict(url_parsed)

        if int(pred[0]) == 1:
            return "Es_Pishing"
        else:
            return "Acortar"

        
    def having_ip_address(self, url):
        match = re.search(
            '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
            '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  # IPv4
            '((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)' # IPv4 in hexadecimal
            '(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}', url)  # Ipv6
        if match:
            # print match.group()
            return 1
        else:
            # print 'No matching pattern found'
            return 0
    
    def abnormal_url(self, url):
        hostname = urlparse(url).hostname
        hostname = str(hostname)
        match = re.search(hostname, url)
        if match:
            # print match.group()
            return 1
        else:
            # print 'No matching pattern found'
            return 0
        
    def google_index(self, url):
        site = search(url, 5)
        return 1 if site else 0
    
    def count_www(self, url):
        url.count('www')
        return url.count('www')
    
    def count_dot(self, url):
        count_dot = url.count('.')
        return count_dot
    
    def count_atrate(self, url):
        return url.count('@')

    def no_of_dir(self, url):
        urldir = urlparse(url).path
        return urldir.count('/')
    
    def no_of_embed(self, url):
        urldir = urlparse(url).path
        return urldir.count('//')
    
    def shortening_service(self, url):
        match = re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                        'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                        'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                        'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                        'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                        'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                        'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|'
                        'tr\.im|link\.zip\.net',
                        url)
        if match:
            return 1
        else:
            return 0
        
    def count_https(self, url):
        return url.count('https')
    
    def count_http(self, url):
        return url.count('http')

    def count_per(self, url):
        return url.count('%')
    
    def count_ques(self, url):
        return url.count('?')
    
    def count_hyphen(self, url):
        return url.count('-')
    
    def count_equal(self, url):
        return url.count('=')
    
    def hostname_length(self, url):
        return len(urlparse(url).netloc)
    
    def url_length(self, url):
        return len(str(url))
    
    def suspicious_words(self, url):
        match = re.search('PayPal|login|signin|bank|account|update|free|lucky|service|bonus|ebayisapi|webscr',
                        url)
        if match:
            return 1
        else:
            return 0
    
    def digit_count(self, url):
        digits = 0
        for i in url:
            if i.isnumeric():
                digits = digits + 1
        return digits
    
    def letter_count(self, url):
        letters = 0
        for i in url:
            if i.isalpha():
                letters = letters + 1
        return letters
    
    def tld_length(self, tld):
        try:
            return len(tld)
        except:
            return -1
        
    def fd_length(self, url):
        urlpath= urlparse(url).path
        try:
            return len(urlpath.split('/')[1])
        except:
            return 0
        
    def parse_url(self, url):

        status = []

        status.append(self.having_ip_address(url))
        status.append(self.abnormal_url(url))
        status.append(self.count_dot(url))
        status.append(self.count_www(url))
        status.append(self.count_atrate(url))
        status.append(self.no_of_dir(url))
        status.append(self.no_of_embed(url))
        status.append(self.shortening_service(url))
        status.append(self.count_https(url))
        status.append(self.count_http(url))
        status.append(self.count_per(url))
        status.append(self.count_ques(url))
        status.append(self.count_hyphen(url))
        status.append(self.count_equal(url))
        status.append(self.url_length(url))
        status.append(self.hostname_length(url))
        status.append(self.suspicious_words(url))
        status.append(self.digit_count(url))
        status.append(self.letter_count(url))
        status.append(self.fd_length(url))
        tld = get_tld(url,fail_silently=True)
        status.append(self.tld_length(tld))

        return status