import os
import pandas as pd
from config import basedir


class MyParser:
    def openxl(self, filename: str, sheet_name=0):
        df = pd.read_excel(filename, sheet_name=sheet_name, header=None)
        df.fillna(method='ffill', axis=1, inplace=True)
        df[0].fillna(method='ffill', inplace=True)
        df[1].fillna(method='ffill', inplace=True)
        self.df = df

    def read(self):
        df = self.df
        row_counts, col_counts = df.shape
        for row_index in range(3, row_counts):
            for col_index in range(2, col_counts, 2):
                company_name = df[1][row_index]
                availability = df[col_index][0]
                item = df[col_index][1]
                data_1 = df[col_index][row_index]
                data_2 = df[col_index+1][row_index]
                data = {
                    df[col_index][2]: data_1,
                    df[col_index + 1][2]: data_2,
                    }
                yield {'company_name': company_name,
                       'availability': availability,
                       'item': item,
                       'data': data
                       }


if __name__ == '__main__':
    fname = os.path.join(basedir, 'Приложение_к_заданию_бек_разработчика.xlsx')
    parser = MyParser()
    parser.openxl(fname)
    gen = parser.read()
    for obj in gen:
        print(obj)
