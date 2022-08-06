import sys
sys.path.insert(0, "../")

import paramiko
import pandas as pd
import numpy as np
import argparse 
from sql.onus import OnusModel
from sql.ponsAverageDbm import PonsAverageDbm

USER=""
PASS=""

""" Carregando argumentos."""
argument = argparse.ArgumentParser(description="")
argument.add_argument("--pon", metavar="\t\tPara informar a PON a ser analisada.", type=str)
argument.add_argument("--clients", metavar="\t\tUse para informar a quantidade de clientes ou o ultimo ID existente na PON.", type=int)
argument.add_argument("--olt", metavar="\t\t\Informe o endereço da OLT.", type=str)
argument.add_argument("--name", metavar="\t\t\Informe o nome da OLT.", type=str)
arguments = argument.parse_args()

""" Carregando valores de parâmetros. """
pon=arguments.pon
nclients=arguments.clients
olt=arguments.olt
olt_name=arguments.name

""" Arrays auxiliares de produção. """
clients_onu=[]

""" Função de consulta SSH. """
def clientSSH(clientssh, pon, onuid):
    try:        
        """ Iniciando uma sessão. """
        stdin,stdout,stderr=clientssh.exec_command(f"show interface gpon {pon} onu {onuid}")
        outlines=stdout.readlines()
        
        """ 
            Iniciando separação do valor de dbm retornado na consulta. 
            Após separação, é montado um objeto com indice DBM e IDONU com os valores recuperados.
        """
        
        if not "syntax error: unknown argument" in outlines[1]:
            
            flag_cancel=True
            
            """ Objeto de auxilio. """
            aux_obj_line={"SERIAL": "", "NAME": "", "DBM": 0.0, "ONUID": onuid, "PON": pon}
            for line in outlines:
                if "Serial Number" in line:
                    """ Recuperando serial number  atrelado a ONU."""
                    aux_obj_line['SERIAL']=line.split(":")[1].strip()
                    
                if "Name" in line:
                    """ Recuperando nome atrelado a ONU."""
                    aux_obj_line['NAME']=line.split(":")[1].strip()
                    
                if "Rx Optical Power [dBm]" in line:
                    """ Recuperando dbm atrelada a ONU."""
                    if "N/A" in line.split(":")[1].strip():
                        flag_cancel=False
                    else: 
                        aux_obj_line['DBM']=float(line.split(":")[1].strip())
                    
            if flag_cancel:
                return aux_obj_line        
            else:
                return "None"
    
        else:            
            return "None"
        
    except Exception as err:
        return "None" 


""" Iniciando Model Onus. """
md_onus = OnusModel()


""" Relizando a consulta a cliente por cliente de acordo com a quantidade informada por parâmetro."""
clientsession = paramiko.SSHClient()
clientsession.set_missing_host_key_policy(paramiko.AutoAddPolicy())
clientsession.connect(hostname=olt, port=22 ,username=USER, password=PASS)

for clt_id in range(0, nclients+1, 1):
       
    """ Recuperando dados de consulta."""
    consult = clientSSH(clientsession, pon, str(clt_id))
    
    """ Caso ocorra de retornar None, não será salvo nada na base."""    
    if consult == "None":
        continue
    
    else: 
        """Salvando retorno da consulta."""
        clients_onu.append(consult)
        """Salvando na Base de Dados.""" 
        md_onus.save(data=consult)
    
      
""" Criando um Dataframe para apresentação dos valores em tela."""
df = pd.DataFrame(clients_onu, columns=["PON", "ONUID", "DBM", "SERIAL", "NAME"]);

""" 
Criando modelo da tabela de medias por pon.
Salvando modelo de média por pon. 
"""
md_average_dbm = PonsAverageDbm()
md_average_dbm.save(olt_name=olt_name, pon=pon, average=float(np.mean(df['DBM'].values)))

"""
Template de apresentação.
Calculando a média de dbm e apresentando em tela.
"""
print(f"""
{"="*90}
{df}
{"="*90}
{"Média de DBM da PON: {:.2f}".format(np.mean(df['DBM'].values))}
PON escaneada: {pon}
{"="*90}
""");