from typing import Optional
from models.employee import Employee


class SalariedEmployee(Employee):
    def __init__(
        self,
        employee_id: str,
        full_name: str,
        department: str = "Unassigned",
        monthly_salary: float = 0.0,
        responsibility_allowance: float = 0.0
    ):
        super().__init__(employee_id, full_name, department)
        self._monthly_salary: float = 0.0
        self._responsibility_allowance: float = 0.0

        self.monthly_salary = monthly_salary
        self.responsibility_allowance = responsibility_allowance

    @classmethod
    def create_basic(cls, employee_id: str, full_name: str):
        return cls(employee_id, full_name, "Unassigned", 0.0, 0.0)

    # Ghi đè phương thức (Method Overriding)
    def calculate_gross_pay(self) -> float:
        return self._monthly_salary + self._responsibility_allowance + self._monthly_bonus

    def get_employee_type(self) -> str:
        return "Nhân viên lương cố định"

    def display_payroll_info(self) -> None:
        print(f"Loại nhân sự        : {self.get_employee_type()}")
        print(f"Mã nhân sự          : {self.employee_id}")
        print(f"Họ và tên           : {self.full_name}")
        print(f"Phòng ban           : {self.department}")
        print(f"Lương cố định       : {self._monthly_salary:,.0f} VNĐ")
        print(f"Phụ cấp trách nhiệm : {self._responsibility_allowance:,.0f} VNĐ")
        print(f"Thưởng trong tháng  : {self.monthly_bonus:,.0f} VNĐ")
        if self.bonus_history:
            print("  -> Chi tiết các khoản thưởng:")
            for b in self.bonus_history:
                print(f"     * {b.amount:,.0f} VNĐ - {b.reason}")
        print(f">> TỔNG THU NHẬP    : {self.calculate_gross_pay():,.0f} VNĐ")

    # Properties & Setters
    @property
    def monthly_salary(self) -> float:
        return self._monthly_salary

    @monthly_salary.setter
    def monthly_salary(self, value: float) -> None:
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError(f"Lương cố định tháng không được âm (Nhận được: {value})")
        self._monthly_salary = float(value)

    @property
    def responsibility_allowance(self) -> float:
        return self._responsibility_allowance

    @responsibility_allowance.setter
    def responsibility_allowance(self, value: float) -> None:
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError(f"Phụ cấp trách nhiệm không được âm (Nhận được: {value})")
        self._responsibility_allowance = float(value)
