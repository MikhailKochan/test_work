import os
import sys
from app import MyApp, conf, engine, parser
from config import basedir


filename = os.path.join(basedir, 'Приложение_к_заданию_бек_разработчика.xlsx')
app = MyApp(config=conf, db_engine=engine, parser=parser)


if __name__ == "__main__":
    if '-drop' in sys.argv:
        app.drop_all_table()
        print('Все записи из базы данныйх удалены')
    if '-read' in sys.argv:
        ind = sys.argv.index('-read')
        if len(sys.argv) <= ind + 1:
            raise ValueError("Необходимо указать аргумент - название файла")
        filename = sys.argv[ind + 1]
        if not filename.endswith('.xlsx'):
            raise ValueError("Некорректное название файла. Файл должен быть в формате .xlsx")
        if not os.path.exists(filename):
            raise ValueError("Фйал не найден")
        app.convert_xlsx_bd(filename_xlsx=filename)
    app.total()
