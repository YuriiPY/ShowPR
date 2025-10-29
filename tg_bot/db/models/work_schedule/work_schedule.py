from sqlalchemy import Column, Date, Integer, String, Time
from db.base import Base


class WorkSchedule(Base):
    __tablename__ = "work_schedule"
    __table_args__ = {'schema': 'team'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, nullable=True)
    work_date = Column(Date, nullable=True)
    start_time = Column(Time, nullable=True)
    end_time = Column(Time)
