from typing import Optional
from models.employee import Employee


class SalesEmployee(Employee):
    MAX_COMMISSION_RATE: float = 0.30

    def __init__(
        self,
        employee_id: str,
        full_name: str,
        department: str = "Unassigned",
        base_salary: float = 0.0,
        sales_revenue: float = 0.0,
        commission_rate: float = 0.0
    ):
        super().__init__(employee_id, full_name, department)
        self._base_salary: float = 0.0
        self._sales_revenue: float = 0.0
        self._commission_rate: float = 0.0

        self.base_salary = base_salary
        self.sales_revenue = sales_revenue
        self.commission_rate = commission_rate

    @classmethod
    def create_basic(cls, employee_id: str, full_name: str):
        return cls(employee_id, full_name, "Unassigned", 0.0, 0.0, 0.0)

    # Nghiệp vụ cập nhật và tính toán
    def update_sales_revenue(self, value: float) -> None:
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError(f"Doanh số bán hàng không được là số âm (Nhận được: {value})")
        self._sales_revenue = float(value)

    def calculate_commission_amount(self) -> float:
        return self._sales_revenue * self._commission_rate

    # Ghi đè phương thức (Method Overriding)
    def calculate_gross_pay(self) -> float:
        return self._base_salary + self.calculate_commission_amount() + self._monthly_bonus

    def get_employee_type(self) -> str:
        return "Nhân viên kinh doanh"

    def display_payroll_info(self) -> None:
        commission_amount = self.calculate_commission_amount()
        print(f"Loại nhân sự        : {self.get_employee_type()}")
        print(f"Mã nhân sự          : {self.employee_id}")
        print(f"Họ và tên           : {self.full_name}")
        print(f"Phòng ban           : {self.department}")
        print(f"Lương cơ bản        : {self._base_salary:,.0f} VNĐ")
        print(f"Doanh số bán hàng   : {self._sales_revenue:,.0f} VNĐ")
        print(f"Tỷ lệ hoa hồng      : {self._commission_rate * 100:.1f}%")
        print(f"Tiền hoa hồng       : {commission_amount:,.0f} VNĐ")
        print(f"Thưởng trong tháng  : {self.monthly_bonus:,.0f} VNĐ")
        if self.bonus_history:
            print("  -> Chi tiết các khoản thưởng:")
            for b in self.bonus_history:
                print(f"     * {b.amount:,.0f} VNĐ - {b.reason}")
        print(f">> TỔNG THU NHẬP    : {self.calculate_gross_pay():,.0f} VNĐ")

    # Properties & Setters
    @property
    def base_salary(self) -> float:
        return self._base_salary

    @base_salary.setter
    def base_salary(self, value: float) -> None:
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError(f"Lương cơ bản không được âm (Nhận được: {value})")
        self._base_salary = float(value)

    @property
    def sales_revenue(self) -> float:
        return self._sales_revenue

    @sales_revenue.setter
    def sales_revenue(self, value: float) -> None:
        self.update_sales_revenue(value)

    @property
    def commission_rate(self) -> float:
        return self._commission_rate

    @commission_rate.setter
    def commission_rate(self, value: float) -> None:
        if not isinstance(value, (int, float)) or value < 0 or value > self.MAX_COMMISSION_RATE:
            raise ValueError(
                f"Tỷ lệ hoa hồng phải nằm trong khoảng [0, {self.MAX_COMMISSION_RATE:.2f}] "
                f"(0% đến {self.MAX_COMMISSION_RATE * 100:.0f}%). Nhận được: {value}"
            )
        self._commission_rate = float(value)
