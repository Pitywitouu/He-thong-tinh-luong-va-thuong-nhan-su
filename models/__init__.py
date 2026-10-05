"""
Package models chứa các lớp thực thể trong hệ thống tính lương và thưởng.
"""

from models.bonus_record import BonusRecord, BonusType
from models.employee import Employee
from models.salaried_employee import SalariedEmployee
from models.hourly_employee import HourlyEmployee
from models.sales_employee import SalesEmployee

__all__ = [
    "BonusRecord",
    "BonusType",
    "Employee",
    "SalariedEmployee",
    "HourlyEmployee",
    "SalesEmployee",
]
