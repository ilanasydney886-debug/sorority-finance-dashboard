from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base
import datetime

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)  # e.g., "Catering for Formal"
    category = Column(String)     # e.g., "Social", "Philanthropy", "Admin"
    amount = Column(Float)        # The cost
    date = Column(DateTime, default=datetime.datetime.utcnow)

class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    pc_year = Column(String)      # e.g., "Fall '24" - useful for sorting
    dues_paid = Column(Float, default=0.0)
    dues_total = Column(Float, default=250.0) # Set a standard dues amount