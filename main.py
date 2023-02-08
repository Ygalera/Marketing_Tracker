import helper.loadData as ld
import helper.procesing as pr
import helper.workflow as wf


if __name__ =='__main__':
    token = input('Ingrese el token de seguridad para acceder a la información de Smartheet: ')
    wf.filteringData(token)
    
