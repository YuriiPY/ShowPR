from sqlalchemy import Column, Integer, String, DateTime, Boolean, BigInteger

from db.base import Base


class Cooks(Base):
    __tablename__ = "cooks"
    __table_args__ = {'schema': 'team'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    cook_name = Column(String, nullable=True)
    level = Column(Integer, nullable=True)
    telegram_id = Column(BigInteger, nullable=True)
    status = Column(Boolean, nullable=True)
    logged_in = Column(Boolean, nullable=False, default=False)

    @property
    def status_text(self):
        return 'Active✅' if self.status else 'Inactive❌'

    @property
    def level_emoji(self):
        return {1: "🥇", 2: "🥈", 3: "🥉"}.get(self.level)
