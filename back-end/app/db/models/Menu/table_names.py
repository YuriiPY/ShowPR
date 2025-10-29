from sqlalchemy import Boolean, Column, Integer, LargeBinary, String, Text

from app.db.base import Base


class TableNames(Base):
    __tablename__ = 'table_translation'
    __table_args__ = {'schema': 'menu_table_names'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    table_name = Column(Text, nullable=False)
    translation_en = Column(Text)
    translation_ua = Column(Text)
    translation_pl = Column(Text)
