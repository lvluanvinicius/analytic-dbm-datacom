import sys
sys.path.insert(0, "../")

import paramiko


class SSH(object):
    def __init__(self):
        self.USERNAME = ""
        self.PASSWORD = ""
        
    def connection(self, host, port=22):
        """
            Relizando a consulta a cliente por cliente de acordo com a quantidade informada por parâmetro.
            host:   Recebe o endereço de destino. Ex: 0.0.0.0
            port:   Recebe a por de destino para conexão ssh. 
                    Por padrão é informada a porta 22.
        """
        try:
            clientsession = paramiko.SSHClient()
            clientsession.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            clientsession.connect(hostname=host, port=port ,username=self.USERNAME, password=self.PASSWORD)
            return clientsession
        except Exception as err:
            print(err)