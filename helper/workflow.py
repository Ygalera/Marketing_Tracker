import helper.loadData as ld
import helper.procesing as pr
def prepareData():
    filters = ld.chargeFilters()
    df = ld.uploadData()
    df['Treated CFN'] = df.apply(pr.treadCFNs,axis = 1)
    df = pr.sp_trim(df)
    sp = ld.load_SPlan()
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
        
def filteringData():
    df,sp,filters = prepareData()
    listOU  = [ou.strip() for ou in filters['SubOU'].unique()]
    df = df[df['OU'].isin(listOU)]
    df['Regulatory info'] = df.apply( pr.searchSP,axis = 1,sp = sp)
    aux = list(filters['Treated'].unique())
    filterList = [val.strip() for val in aux]
    df['Critical?'] =df.apply(defineCriticalCFN,axis = 1,filterList = filterList)
    df.to_excel('Results\prueba.xlsx',index=False)

    