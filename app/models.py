from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()
metadata = Base.metadata


class MainTable(Base):
    __tablename__ = 'maintable'

    id = Column(Integer, primary_key=True)

    date = Column(DateTime())
    data_1 = Column(Integer)
    data_2 = Column(Integer)

    company_id = Column(Integer, ForeignKey('company.id'))
    availability_id = Column(Integer, ForeignKey('availability.id'))
    item_id = Column(Integer, ForeignKey('item.id'))

    def __init__(self, data: dict, date: datetime):
        self.data_1 = data.get('data1')
        self.data_2 = data.get('data2')
        self.date = date

    def __repr__(self):
        return f"{self.date.strftime('%d-%m-%Y')}|{self.data_1}|{self.data_2}"


class TableObj:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def get_item(cls, session, **kwargs):
        item = session.query(cls).filter_by(**kwargs).first()
        if not item:
            item = cls(**kwargs)
            session.add(item)
        return item


class Company(Base, TableObj):
    __tablename__ = 'company'

    id = Column(Integer, primary_key=True)

    name = Column(String(128), index=True, unique=True)
    maintable = relationship('MainTable', backref='company', lazy='dynamic')


class Availability(Base, TableObj):
    __tablename__ = 'availability'

    id = Column(Integer, primary_key=True)

    name = Column(String(128), index=True, unique=True)
    maintable = relationship('MainTable', backref='availability', lazy='dynamic')


class Item(Base, TableObj):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)

    name = Column(String(128), index=True, unique=True)
    maintable = relationship('MainTable', backref='item', lazy='dynamic')

