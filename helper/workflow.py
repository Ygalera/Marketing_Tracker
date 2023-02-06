import helper.loadData as ld
import helper.procesing as pr
import pandas as pd
def prepareData(token):
    filters = ld.chargeFilters()
    df = ld.uploadData()
    df['Treated CFN'] = df.apply(pr.treadCFNs,axis = 1)
    df = df.dropna(subset=['CFN'])
    df = pr.sp_trim(df)
    sp = ld.load_SPlan(token)
    sp = pr.sp_trim(sp)
    return df,sp,filters

def PrepareNotfound(df,filters):
    filterCFNs = list(filters['Treated'].unique())
    notFound = []
    for cfn in filterCFNs:
        if cfn in df['Treated CFN']:
            print('estoy aqui perrini')
            continue
        else:
            notFound.append(cfn)
    return notFound

def defineCriticalCFN(row,filterList):
    a = row['Treated CFN']
    if a in filterList:
        return 'Critical CFN'
    else:
        return 'Not critical CFN'

def determinenotFound(df,FilterList):
    CnF = pd.DataFrame(columns = ['CFN Not Found'])
    reference = list(df['Treated CFN'].unique())
    notFound = []
    for val in FilterList:
        if val in reference:
            pass
        else:
            notFound.append(val)
    
    CnF['CFN Not Found'] = notFound
    return CnF
        

def filteringData(token):
    df,sp,filters = prepareData(token)
    listOU  = [ou.strip() for ou in filters['SubOU'].unique()]
    df = df[df['OU'].isin(listOU)]
    print('Buscando información en el Submission Plan...')
    df['Regulatory info'] = df.apply( pr.searchSP,axis = 1,sp = sp)
    print('La información ya ha sido asignado a los Produtos')
    aux = list(filters['Treated'].unique())
    filterList = [val.strip() for val in aux]
    print('Asignando Prioridad a los Productos...')
    df['Critical?'] =df.apply(defineCriticalCFN,axis = 1,filterList = filterList)
    print('Prioridad satisfactoriamente asignada')
    CnF = determinenotFound(df,filterList)
    pr.create_excel(df,CnF)



    # FileName = input('Ingrese el nombre con el que desea guardar el documento: ')
    # FileName = f'Results\{FileName}.xlsx'
    # df.to_excel(FileName,index=False)

    