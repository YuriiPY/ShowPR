from sqlalchemy import Boolean, Column, Integer, String, BigInteger

from db.base import Base


class Admin(Base):
    __tablename__ = "admins"
    __table_args__ = {'schema': 'team'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    admin_name = Column(String, nullable=False)
    level = Column(Integer, nullable=False)
    telegram_id = Column(BigInteger, nullable=False)
    status = Column(Boolean, nullable=False)
    logged_in = Column(Boolean, nullable=False, default=False)
