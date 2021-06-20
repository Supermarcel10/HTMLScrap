from pandas import DataFrame

title = "test"

df = DataFrame(columns=["title", "date", "start_time", "end_time"])
df = df.append(DataFrame([["test", "test", "test", "test"]], columns=["title", "date", "start_time", "end_time"]), ignore_index=True)

df.to_csv("%s.csv" % title, index=False, sep=";", na_rep="---")

