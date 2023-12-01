
from bookstore.db import SqlHandler
from bookstore.logger import CustomFormatter

Inst=SqlHandler('temp', 'employees')


import pandas as pd
data=pd.read_csv('employee.csv')


Inst=SqlHandler('temp', 'employees')
Inst.insert_many(data)


Inst.close_cnxn()