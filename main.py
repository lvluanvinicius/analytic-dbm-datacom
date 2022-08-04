import paramiko
import pandas as pd
import numpy as np
import argparse 


# Carregando argumentos.
argument = argparse.ArgumentParser(description="")
argument.add_argument("--pon", metavar="\t\tPara informar a PON a ser analisada.", type=str)
argument.add_argument("--nclients", metavar="\t\tUse para informar a quantidade de clientes ou o ultimo ID existente na PON.", type=int)
argument.add_argument("--olt", metavar="\t\t\Informe o endereço da OLT.", type=str)
arguments = argument.parse_args()

# Carregando valores de pon e numero de clientes.
pon=arguments.pon
nclients=arguments.nclients
olt=arguments.olt


# Array de produção.
clients_onu=[]

# Função de consulta SSH.
def clientSSH(pon, onuid, host, port=22):
    try:
        # Iniciando uma sessão.
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, port=port ,username='suporte', password='n2GC@Sept21')
        stdin,stdout,stderr=client.exec_command(f"show interface gpon {pon} onu {onuid}")
        outlines=stdout.readlines()
        client.close()         
        
    
        # Iniciando separação do valor de dbm retornado na consulta. 
        # Após separação, é montado um objeto com indice DBM e IDONU com os valores recuperados.
        
        if not "syntax error: unknown argument" in outlines[1]:
            # Objeto de auxilio.
            aux_obj_line={"SERIAL": "", "NAME": "", "DBM": 0.0, "ONUID": onuid, "PON": pon}
            
            for line in outlines:
                if "Serial Number" in line:
                    # Recuperando serial number  atrelado a ONU.
                    aux_obj_line['SERIAL']=line.split(":")[1].strip()
                    
                if "Name" in line:
                    # Recuperando nome atrelado a ONU.
                    aux_obj_line['NAME']=line.split(":")[1].strip()
                    
                if "Rx Optical Power [dBm]" in line:
                    # Recuperando dbm atrelada a ONU.
                    aux_obj_line['DBM']=float(line.split(":")[1].strip())
                    
            return aux_obj_line        
    
        else:
            return "None"
        
    except Exception as err:
        return "None" 


# Relizando a consulta a cliente por cliente de acordo com a quantidade informada por parâmetro.
for clt_id in range(0, nclients+1, 1):
    
    # Recuperando dados de consulta.
    consult = clientSSH(pon, str(clt_id), olt)

    # Caso ocorra de retornar None, não será salvo nada na base.
    if consult == "None":
        continue
    else: 
        # Salvando retorno da consulta.
        clients_onu.append(consult)
      
      
# Criando um Dataframe para apresentação dos valores em tela.
df = pd.DataFrame(clients_onu, columns=["PON", "ONUID", "DBM", "SERIAL", "NAME"]);


# Template de apresentação.
# Calculando a média de dbm e apresentando em tela.
print(f"""
{"="*60}
{df}
{"="*60}
{"Média de DBM da PON: {:.2f}".format(np.mean(df['DBM'].values))}
PON escaneada: {pon}
{"="*60}
""");