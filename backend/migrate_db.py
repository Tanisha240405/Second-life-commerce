import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, make_transient
from models.database import Base
from models.credit_transaction import CreditTransaction
from models.listing import Listing
from models.order import Order
from models.product import Product
from models.return_grade import ReturnGrade
from models.return_request import ReturnRequest

sqlite_url = "sqlite:///backend/second_life.db"
neon_url = "postgresql://neondb_owner:npg_QoHBpmy2Y5bF@ep-icy-truth-aih0dapj-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require"

sqlite_engine = create_engine(sqlite_url)
neon_engine = create_engine(neon_url)

Base.metadata.create_all(bind=neon_engine)

SqliteSession = sessionmaker(bind=sqlite_engine)
NeonSession = sessionmaker(bind=neon_engine)

tables = [Order, CreditTransaction, ReturnRequest, ReturnGrade, Listing]

with SqliteSession() as src, NeonSession() as dst:
    for model in tables:
        print(f"Migrating {model.__tablename__}...")
        dst.query(model).delete()
        dst.commit()
        
        items = src.query(model).all()
        for item in items:
            make_transient(item)
            dst.add(item)
        
        dst.commit()
        print(f"  -> Migrated {len(items)} rows")

print("Migration complete!")
