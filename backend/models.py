from extensions import db 
from sqlalchemy import String, Float, ForeignKey, Date, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date, datetime

class User(db.Model):
    __tablename__ = 'users'

    id:Mapped[int] = mapped_column(primary_key=True)
    email:Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    password_hash:Mapped[str | None] = mapped_column(String(250), nullable=True)
    google_id:Mapped[str | None ] = mapped_column(String(250), unique=True, nullable=True )

    #relationship
    expenses:Mapped[list["Expense"]] = relationship(
        back_populates='user', cascade="all, delete-orphan"
    )

class Expense(db.Model):
    __tablename__ = 'expenses'

    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(250), nullable=False)
    amount:Mapped[float] = mapped_column(Float, nullable=False)
    category:Mapped[str] = mapped_column(String(250), nullable=False)
    expense_date:Mapped[date] = mapped_column(Date, nullable=False)
    created_at:Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    #relationship
    user_id:Mapped[int] = mapped_column(ForeignKey("users.id"))
    user:Mapped["User"] = relationship(back_populates='expenses')

    # method to return as json
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'amount': self.amount,
            'category': self.category,
            'expense_date': self.expense_date.isoformat(),
            'created_at': self.created_at.isoformat(), 
            'user_id': self.user_id
        }
