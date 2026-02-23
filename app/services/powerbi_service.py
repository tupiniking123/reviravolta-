import csv
import io
from sqlalchemy import text
from sqlalchemy.orm import Session


def query_to_csv(db: Session, sql: str) -> str:
    rows = db.execute(text(sql))
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(rows.keys())
    for row in rows:
        writer.writerow(row)
    return output.getvalue()
