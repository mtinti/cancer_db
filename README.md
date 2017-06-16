# Cancer DB
some funtions to create a query database from GDC data


to create Manifest File 
from https://portal.gdc.cancer.gov/
- go to Data link
- go to File tab
- on the bottom select open
- on data format select MAF
- count 132 files as 14/06/17
- download manifest

to download dataset
- https://gdc.cancer.gov/access-data/gdc-data-transfer-tool
- https://docs.gdc.cancer.gov/Data_Transfer_Tool/Users_Guide/Data_Download_and_Upload/


dump pandas to sql
- https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_sql.html

tutorial mysql
- http://sebastianraschka.com/Articles/2014_sqlite_in_python_tutorial.html

## To do
### compare the rate of Variant_Classification mutation in ohonlog family members 
- Silent vs Missense_Mutation
- Silent vs (Nonsense_Mutation + Frame_Shift_Del + Frame_Shift_Ins)
- Silent vs 3'UTR+5'UTR

### compare the mutation rate of kinase activation site in ohonlog family members 



 
