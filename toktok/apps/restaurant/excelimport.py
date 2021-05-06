import pandas as pd

path = r'D:\work\Django\toktok-backend\toktok\apps\restaurant\product_1618567151_sample_mcdonalds.xls'

def excelconversion():
    df = pd.read_excel (path)
    for _ in range(len(df)):
        name=df.iloc[_][1]
        sku=df.iloc[_][3]
        description=df.iloc[_][2]
        cover_image=df.iloc[_][7]
        manager="req"
        amountInCents = df.iloc[_][6]
        MenuCollection=df.iloc[_][0]
        subtype=df.iloc[_][8]
        addons=None
        print(name,sku,description,cover_image,manager,amountInCents,MenuCollection,subtype,addons)
        print("\n")
    print(df.iloc[0][0])
excelconversion()