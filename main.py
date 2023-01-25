import helper.loadData as ld
import helper.procesing as pr


if __name__ =='__main__':
    df = ld.uploadData()
    df['Treated CFN'] = df.apply(pr.treadCFNs,axis = 1)
    df = pr.sp_trim(df)
    sp = ld.load_SPlan()
    sp = pr.sp_trim(sp)
    df['Regulatory info'] = df.apply( pr.searchSP,axis = 1,sp = sp)





    df.to_excel('Results\prueba.xlsx',index=False)