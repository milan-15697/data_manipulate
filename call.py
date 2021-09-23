from ddtable import DecisionTable
df = DecisionTable().display_dataframe()
print(df)
res = DecisionTable().get_results(75,12,15,"flashes","flashing")
print('Result: ', res)
