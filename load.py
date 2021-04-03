#!/usr/bin/env python3

from pathlib import Path
import sqlalchemy
from sqlalchemy import Table, Column, Integer, String

def connect(user, password, db, host='localhost', port=5432):
    '''Returns a connection and a metadata object'''
    # We connect with the help of the PostgreSQL URL
    # postgresql://federer:grandestslam@localhost:5432/tennis
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, db)

    # The return value of create_engine() is our connection object
    con = sqlalchemy.create_engine(url, client_encoding='utf8')

    # We then bind the connection to MetaData()
    meta = sqlalchemy.MetaData(bind=con)

    return con, meta

if __name__ == "__main__":
    con, meta = connect("postgres", "postgres", "postgres")

    fb_leak = Table('fb_leak', meta,
                    Column('id', Integer, primary_key=True),
                    Column('file_name', String),
                    Column('phone_number', String),
                    Column('facebook_id', String),
                    Column('first_name', String),
                    Column('last_name', String),
                    Column('sex', String),
                    Column('location', String),
                    Column('origin', String),
                    Column('situation', String),
                    Column('work_or_school', String),
                    Column('some_date_1', String),
                    Column('email', String),
                    Column('some_date_2', String),
    )

    # meta.create_all(con)
    txt_folder = Path('/home/seraf/code/fbleak/data').rglob('*.txt')
    files = [x for x in txt_folder]
    for name in files:
        f = open(name, 'r')
        lines = f.readlines()
        for line in lines:
            l = line.split(":")
            clause = fb_leak.insert().values(
                file_name=str(name).split("/")[-1].split(".txt")[0],
                phone_number=l[0],
                facebook_id=l[1],
                first_name=l[2],
                last_name=l[3],
                sex=l[4],
                location=l[5],
                origin=l[6],
                situation=l[7],
                work_or_school=l[8],
                some_date_1=l[9],
                email=l[10],
                some_date_2=l[11],
            )
            con.execute(clause)
        f.close()
