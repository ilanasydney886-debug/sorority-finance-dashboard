from database import SessionLocal, engine, Base
import models

# This line creates the actual .db file based on your models
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Add some sample members from your real PC years
sample_members = [
    models.Member(name="Sarah Jenkins", pc_year="Fall 23", dues_paid=250.0, dues_total=250.0),
    models.Member(name="Maya Rodriguez", pc_year="Fall 24", dues_paid=100.0, dues_total=250.0),
    models.Member(name="Elena Fisher", pc_year="Spring 25", dues_paid=0.0, dues_total=250.0)
]

# Add some real-world sorority transactions
sample_transactions = [
    models.Transaction(description="Catering for Formal", category="Social", amount=1200.0),
    models.Transaction(description="Recruitment Decorations", category="Recruitment", amount=350.0),
    models.Transaction(description="Chapter Dues", category="Admin", amount=600.0),
    models.Transaction(description="Philanthropy T-shirts", category="Philanthropy", amount=450.0)
]

try:
    db.add_all(sample_members)
    db.add_all(sample_transactions)
    db.commit()
    print("✅ Sorority Finance Database Created and Seeded Successfully!")
except Exception as e:
    print(f"❌ Error seeding database: {e}")
    db.rollback()
finally:
    db.close()