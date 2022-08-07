import pandas as pd
import numpy as np


# General libs 
from sql.ponsAverageDbm import PonsAverageDbmModel
from sql.olts import OLTConfigModel
from ssh.clientSSH import ClientSSH
from ssh.ssh import SSH


""" Iniciando uma sessão com host de destino. """
""" Iniciando instância de SSH. """
ssh_config=SSH()
type(ssh_config)
""" Criando Client SSH para execução de comandos. """
clientSSH=ClientSSH()


""" . """
md_olts=OLTConfigModel()
olts_data=md_olts.get_olt_config()


def consult_client(sessionSSH, nclients, gpon_port, client_aux):
    for clt_id in range(0, nclients+1, 1):
        
        """ Recuperando dados de consulta. """
        consult = clientSSH.execute_show_interface(clientssh=sessionSSH, pon=gpon_port, onuid=str(clt_id))
        
        """ Caso ocorra de retornar None, não será salvo nada na base. """    
        if consult == "None":
            continue
        
        else: 
            """Salvando retorno da consulta. """
            client_aux.append(consult)



for olt_dt_config in olts_data:

    """ Arrays auxiliares de produção. """
    clients_onu=[]  
    
    # ...
    clientsession=ssh_config.connection(host=olt_dt_config["HOST"])
    pon_id=""
    for ponid in range(1, olt_dt_config["PONS"]+1, 1):
        pon_id=f"1/1/{ponid}"
        consult_client(
            sessionSSH=clientsession, nclients=5, 
            gpon_port=pon_id, client_aux=clients_onu
        )        
              
        """ Criando um Dataframe para apresentação dos valores em tela. """
        df = pd.DataFrame(clients_onu, columns=["PON", "ONUID", "DBM", "SERIAL", "NAME"]);

        """ 
        Criando modelo da tabela de medias por pon.
        Salvando modelo de média por pon. 
        """
        md_average_dbm = PonsAverageDbmModel()

        md_average_dbm.save(
            olt_id=olt_dt_config["id"], pon=pon_id,
            average=float(np.mean(df['DBM'].values))
        )
