import sys
sys.path.insert(0, "../")

from .ssh import SSH


class ClientSSH(object):
    
    def __init__(self):
        pass
    
    def execute_show_interface(self, clientssh, pon, onuid):
        
        """ Função de consulta SSH. """
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
            print(err)
            return "None" 
