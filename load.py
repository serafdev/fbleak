#!/usr/bin/env python3

import sqlalchemy

from dataclasses import dataclass
from pathlib import Path
from sqlalchemy import Table, Column, Integer, String


def connect(user, password, db, host="localhost", port=5432):
    """Returns a connection and a metadata object"""
    # We connect with the help of the PostgreSQL URL
    # postgresql://federer:grandestslam@localhost:5432/tennis
    url = "postgresql://{}:{}@{}:{}/{}"
    url = url.format(user, password, host, port, db)

    # The return value of create_engine() is our connection object
    con = sqlalchemy.create_engine(url, client_encoding="utf8")

    # We then bind the connection to MetaData()
    meta = sqlalchemy.MetaData(bind=con)

    return con, meta


@dataclass
class Leak:
    file_name: str
    phone_number: str
    facebook_id: str
    first_name: str
    last_name: str
    sex: str
    location: str
    origin: str
    situation: str
    work_or_school: str
    some_date_1: str
    email: str
    some_date_2: str


def process_data(country: str, line: str) -> Leak:
    try:
        if country in ["Canada", "USA"]:
            x = line.split(":")
            return Leak(
                file_name=country,
                phone_number=x[0],
                facebook_id=x[1],
                first_name=x[2],
                last_name=x[3],
                sex=x[4],
                location=x[5],
                origin=x[6],
                situation=x[7],
                work_or_school=x[8],
                some_date_1=x[9],
                email=x[10],
                some_date_2=x[11],
            )
        if country in ["Tunisia", "Algeria"]:
            x = line.split(",")
            return Leak(
                file_name=country,
                facebook_id=x[0],
                phone_number=x[1],
                first_name=x[2],
                last_name=x[3],
                email=x[4],
                some_date_2=x[5],
                sex=x[6],
                location=x[7],
                origin=x[8],
                situation=x[9],
                work_or_school=x[10],
                some_date_1=x[11],
            )
    except:
        return None


if __name__ == "__main__":
    con, meta = connect("postgres", "postgres", "postgres")

    fb_leak = Table(
        "fb_leak",
        meta,
        Column("id", Integer, primary_key=True),
        Column("file_name", String),
        Column("phone_number", String),
        Column("facebook_id", String),
        Column("first_name", String),
        Column("last_name", String),
        Column("sex", String),
        Column("location", String),
        Column("origin", String),
        Column("situation", String),
        Column("work_or_school", String),
        Column("some_date_1", String),
        Column("email", String),
        Column("some_date_2", String),
    )

    # meta.create_all(con)
    txt_folder = Path("/home/seraf/code/fbleak/data").rglob("*.txt")
    files = [x for x in txt_folder]

    for name in files:
        f = open(name, "r")
        lines = f.readlines()
        country = str(name).split("/")[-1].split(".txt")[0]
        for line in lines:
            l = process_data(country, line)
            if l is None:
                continue
            clause = fb_leak.insert().values(
                file_name=country,
                phone_number=l.phone_number,
                facebook_id=l.facebook_id,
                first_name=l.first_name,
                last_name=l.last_name,
                sex=l.sex,
                location=l.location,
                origin=l.origin,
                situation=l.situation,
                work_or_school=l.work_or_school,
                some_date_1=l.some_date_1,
                email=l.email,
                some_date_2=l.some_date_2,
            )
            con.execute(clause)
        f.close()
