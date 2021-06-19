from pandas import DataFrame, concat
from numpy.random import randint

# title = "test"
#
# df = DataFrame(data=[[1, 2, 3]], columns=['date', 'start_time', 'end_time'])
# concat([df, DataFrame(data=[[2, 2, 3]], columns=['date', 'start_time', 'end_time'])])
# print(df)
# #
# #
# # df = DataFrame(columns=["date", "start_time", "end_time"])
# #
# # dfAdding = DataFrame([["1/1/2020", 1, 2], ["2/1/2020", 2, 3]], columns=["date", "start_time", "end_time"])
# # df.append(dfAdding)
# #
# df.to_csv("%s.csv" % title, index=False, sep=";", na_rep="---")

import pandas

df = pandas.DataFrame(columns=["A"])

print(df)