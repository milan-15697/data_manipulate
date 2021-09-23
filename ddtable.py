"""ddtable.py"""
import operator
import traceback
import pandas as pd

class DecisionTable:
    '''Decision Table class containing methods, facilitating dynamic gathering of results'''

    def __init__(self):
        '''Initializing the program with DF from file, operators and other components'''
        path = 'table.xls'
        self.df = pd.read_excel(path,sheet_name='Sheet1')
        self.cols_len = len(self.df.columns)

        self.operators = {
            "Number >=": operator.ge,
            "Number =": operator.eq,
            "Number <=": operator.le,
            "Number !=": operator.ne,
            "Text Contain": self.string_contains,
            "Text Exact Match": operator.eq,
            "Text Starts With": self.string_starts_with,
            "Text Does Not Contain": self.string_does_not_contain
        }

        self.column_names = list(self.df.columns.values)
        self.result_column_names = [name for name in self.column_names\
                                        if name.startswith("Res")]
        self.column_names = [name for name in self.column_names\
                                        if not name.startswith("Res")]
        self.cols_len = len(self.column_names)
        self.boolean_mapper()

    def string_starts_with(self, s_string, arg):
        return s_string.startswith(arg)

    def string_contains(self, s_string, arg):
        if pd.isnull(s_string) or pd.isnull(arg):
            return
        try:
            return arg in s_string
        except Exception:
            pass

    def string_does_not_contain(self, s_string, arg):
        if pd.isnull(s_string) or pd.isnull(arg):
            return
        try:
            return arg not in s_string
        except Exception:
            pass
    
    def display_dataframe(self):
        return self.df

    def boolean_mapper(self):
        '''Boolean mapper to keep a track of satisfied conditions'''
        self.bool_mapper = [False for i in range(self.cols_len)]

    def get_results(self, *args):
        '''Get_results function gathers the arguments, parses the DF to produce desired output'''
        values = list(args)
        print('Input args: ', values, '\n')
        res = None
        try:
            for df_index in range(len(self.df.index)):
                for row_index, elem in enumerate(self.df.iloc[df_index]):
                    if row_index < self.cols_len:
                        operator = self.column_names[row_index]
                        print('Evaluating: ',values[row_index], operator , elem)

                        if self.operators[operator](values[row_index], elem):
                            self.bool_mapper[row_index] = True

                        if all(self.bool_mapper):
                            res = [self.df.iloc[df_index][result]\
                                            for result in self.result_column_names]
                            self.boolean_mapper()
                            return res
                self.boolean_mapper()
                print('\n')
            if res is None:
                ret = [self.df.iloc[df_index][result]\
                                            for result in self.result_column_names]
                return ret
        except Exception as ex:
            print('Exception::: ', ex, traceback.print_exc())
            pass
