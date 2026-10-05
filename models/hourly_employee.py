from typing import Optional
from models.employee import Employee


class HourlyEmployee(Employee):
    STANDARD_HOURS_LIMIT: float = 160.0
    OVERTIME_RATE_MULTIPLIER: float = 1.5
    MAX_WORKED_HOURS: float = 250.0

    def __init__(
        self,
        employee_id: str,
        full_name: str,
        department: str = "Unassigned",
        hourly_rate: float = 0.0,
        worked_hours: float = 0.0
    ):
        super().__init__(employee_id, full_name, department)
        self._hourly_rate: float = 0.0
        self._worked_hours: float = 0.0

        self.hourly_rate = hourly_rate
        self.worked_hours = worked_hours

    @classmethod
    def create_basic(cls, employee_id: str, full_name: str):
        return cls(employee_id, full_name, "Unassigned", 0.0, 0.0)

    # Nghiệp vụ tính toán
    def calculate_base_pay(self) -> float:
        if self._worked_hours <= self.STANDARD_HOURS_LIMIT:
            return self._worked_hours * self._hourly_rate
        else:
            regular_pay = self.STANDARD_HOURS_LIMIT * self._hourly_rate
            overtime_hours = self._worked_hours - self.STANDARD_HOURS_LIMIT
            overtime_pay = overtime_hours * self._hourly_rate * self.OVERTIME_RATE_MULTIPLIER
            return regular_pay + overtime_pay

    @property
    def regular_hours(self) -> float:
        return min(self._worked_hours, self.STANDARD_HOURS_LIMIT)

    @property
    def overtime_hours(self) -> float:
        return max(0.0, self._worked_hours - self.STANDARD_HOURS_LIMIT)

    # Ghi đè phương thức (Method Overriding)
    def calculate_gross_pay(self) -> float:
        return self.calculate_base_pay() + self._monthly_bonus

    def get_employee_type(self) -> str:
        return "Nhân viên theo giờ"

    def display_payroll_info(self) -> None:
        print(f"Loại nhân sự        : {self.get_employee_type()}")
        print(f"Mã nhân sự          : {self.employee_id}")
        print(f"Họ và tên           : {self.full_name}")
        print(f"Phòng ban           : {self.department}")
        print(f"Đơn giá giờ         : {self._hourly_rate:,.0f} VNĐ/giờ")
        print(f"Số giờ làm việc     : {self._worked_hours:.1f} giờ "
              f"(Chuẩn: {self.regular_hours:.1f}h, Tăng ca: {self.overtime_hours:.1f}h)")
        print(f"Lương theo giờ      : {self.calculate_base_pay():,.0f} VNĐ")
        print(f"Thưởng trong tháng  : {self.monthly_bonus:,.0f} VNĐ")
        if self.bonus_history:
            print("  -> Chi tiết các khoản thưởng:")
            for b in self.bonus_history:
                print(f"     * {b.amount:,.0f} VNĐ - {b.reason}")
        print(f">> TỔNG THU NHẬP    : {self.calculate_gross_pay():,.0f} VNĐ")

    # Properties & Setters
    @property
    def hourly_rate(self) -> float:
        return self._hourly_rate

    @hourly_rate.setter
    def hourly_rate(self, value: float) -> None:
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError(f"Đơn giá giờ không được âm (Nhận được: {value})")
        self._hourly_rate = float(value)

    @property
    def worked_hours(self) -> float:
        return self._worked_hours

    @worked_hours.setter
    def worked_hours(self, value: float) -> None:
        if not isinstance(value, (int, float)) or value < 0 or value > self.MAX_WORKED_HOURS:
            raise ValueError(
                f"Số giờ làm việc phải nằm trong khoảng [0, {self.MAX_WORKED_HOURS:.0f}] giờ. "
                f"Nhận được: {value}"
            )
        self._worked_hours = float(value)
