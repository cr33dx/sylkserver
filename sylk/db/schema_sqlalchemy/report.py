from .db import Base
from .psap import Psap
from sqlalchemy import String, Column, ForeignKey, PickleType, DateTime, Float, Integer, Enum
import enum

class CallType(enum.Enum):
    'completed' = 'completed'
    'abandoned' = 'abandoned'

class CallReport(Base):
    report_id = Column(String, primary_key=True)
    type = Column(Enum(CallType), nullable=False, default='completed')
    psap_id = Column(String, ForeignKey(Psap.psap_id))
    report_name = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    pdf_file = Column(String)
    csv_file = Column(String)


class CompletedCallReportDetails(Base):
    report_id = Column(String, primary_key=True)
    psap_id = Column(String, ForeignKey(Psap.psap_id))
    orig_type = Column(String)
    start_time = Column(String)
    caller_ani = Column(String)
    name_calltaker = Column(String)
    response_time = Column(Float)
    avg_response_time= Column(Float)
    duration = Column(Integer)
    avg_duration = Column(Float)
    

class AbandonedCallReportDetails(Base):
    report_id = Column(String, primary_key=True)
    psap_id = Column(String, ForeignKey(Psap.psap_id))
    orig_type = Column(String)
    start_time = Column(String)
    caller_ani = Column(String)
    


class AbandonedCallReport(Base):
    psap_id = Column(String, ForeignKey(Psap.psap_id))
    report_name = Column(String)