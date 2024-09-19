from database.db_service import Base
from sqlalchemy import Column, Integer,ForeignKey


class Progress(Base):
    __tablename__="progress"
    knowledge_id = Column(Integer,ForeignKey("knowledge.id",ondelete='CASCADE'),primary_key=True)
    file_id = Column(Integer,primary_key=True)
    progress = Column(Integer)