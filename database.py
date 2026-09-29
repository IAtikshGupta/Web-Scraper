import sqlite3
import datetime
import scraper

jobs = []

def list_jobs():
    cursor, connection = connect()

    cursor.execute("SELECT * FROM Jobs")
    jobs = cursor.fetchall()

    close(connection)
    return jobs

def delete_job(jobid):
    cursor, connection = connect()

    cursor.execute(
        "DELETE FROM Jobs WHERE JobID = ?",
        (jobid,)
    )

    if cursor.rowcount == 0:
        print("Job not found.")
    else:
        print("Job deleted.")

    close(connection)


def init():
    connection = sqlite3.connect("jobs.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Jobs (
            JobID INTEGER PRIMARY KEY,
            JobCode TEXT NOT NULL UNIQUE,
            Title TEXT NOT NULL,
            Company TEXT NOT NULL,
            City TEXT,
            URL TEXT NOT NULL UNIQUE,
            DatePosted TEXT,
            WorkingModel TEXT
        )
    """)

    connection.commit()
    connection.close()

def connect():
    connection = sqlite3.connect("jobs.db")
    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    return cursor, connection

def close(connection):
    connection.commit()
    connection.close()

def add_job(job):
    cursor, connection = connect()

    cursor.execute("""
        INSERT INTO Jobs (
            JobCode,
            Title,
            Company,
            City,
            URL,
            DatePosted,
            WorkingModel
        )
        VALUES ( ?, ?, ?, ?, ?, ?, ?)
    """, (
        job["job_code"],
        job["title"],
        job["company"],
        job["city"],
        job["link"],
        job["date_posted"],
        job["working_model"]
    ))

    close(connection)


def main():
    init()
    jobs = scraper.give_jobs()
    for i in jobs:
        add_job(i)

if __name__ == "__main__":
    main()
