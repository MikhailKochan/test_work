import os
import datetime
import random
from config import Config, basedir
from app.exel_parser import MyParser
from sqlalchemy import func, create_engine
from sqlalchemy.orm import Session
from app.models import Company, Availability, Item, MainTable, Base


conf = Config()
engine = create_engine(conf.SQLALCHEMY_DATABASE_URI, echo=False, future=True)
parser = MyParser()


class MyApp(object):
    def __init__(self, db_engine, parser, config):
        self.engine = db_engine
        self.parser = parser
        self.config = config

    def drop_all_table(self):
        with Session(self.engine) as session:
            for table in reversed(Base.metadata.sorted_tables):
                session.execute(table.delete())
            session.commit()

    def convert_xlsx_bd(self, filename_xlsx):
        date = datetime.datetime(year=2023, month=5, day=1)
        with Session(engine) as session:
            self.parser.openxl(filename=filename_xlsx)
            for obj in self.parser.read():
                company_name = obj.get('company_name')
                availability_name = obj.get('availability')
                item_name = obj.get('item')
                data = obj.get("data")

                if company_name and availability_name and item_name:
                    company = Company.get_item(name=company_name, session=session)
                    availability = Availability.get_item(name=availability_name, session=session)
                    item = Item.get_item(name=item_name, session=session)

                    new_write = MainTable(data=data, date=date.replace(day=random.choice(list(range(1, 25)))))

                    item.maintable.append(new_write)
                    availability.maintable.append(new_write)
                    company.maintable.append(new_write)

                    session.add(new_write)
            session.commit()

    def total(self):
        with Session(engine) as session:
            results = session.query(MainTable.date, func.sum(MainTable.data_1 + MainTable.data_2).label('total')). \
                join(Item). \
                filter(Item.name.in_(['Qoil', 'Qliq'])). \
                group_by(MainTable.date). \
                all()

            for date, total in results:
                print(f"Дата: {date.strftime('%d-%m-%Y')}, Расчетный тотал: {total}")

