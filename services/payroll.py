from typing import List, Optional
from models.employee import Employee


class Payroll:
    def __init__(self, period: str):
        if not period or not isinstance(period, str) or not period.strip():
            raise ValueError("Kỳ lương không được để trống (ví dụ: '2026-09').")
        self._period: str = period.strip()
        self._employees: List[Employee] = []

    def add_employee(self, employee: Employee) -> None:
        if employee is None or not isinstance(employee, Employee):
            raise ValueError("Đối tượng nhân sự không hợp lệ hoặc bị None.")

        if self.find_employee(employee.employee_id) is not None:
            raise ValueError(
                f"Lỗi: Mã nhân sự '{employee.employee_id}' đã tồn tại trong bảng lương kỳ {self._period}!"
            )

        self._employees.append(employee)

    def find_employee(self, employee_id: str) -> Optional[Employee]:
        if not employee_id or not isinstance(employee_id, str):
            return None
        target_id = employee_id.strip().upper()
        for emp in self._employees:
            if emp.employee_id.upper() == target_id:
                return emp
        return None

    def remove_employee(self, employee_id: str) -> bool:
        emp = self.find_employee(employee_id)
        if emp:
            self._employees.remove(emp)
            return True
        return False

    def calculate_total_payroll(self) -> float:
        return sum(emp.calculate_gross_pay() for emp in self._employees)

    def calculate_payroll_by_department(self, department: str) -> float:
        if not department or not isinstance(department, str):
            return 0.0
        target_dept = department.strip().upper()
        return sum(
            emp.calculate_gross_pay()
            for emp in self._employees
            if emp.department.upper() == target_dept
        )

    def find_highest_paid_employee(self) -> Optional[Employee]:
        if not self._employees:
            return None
        return max(self._employees, key=lambda emp: emp.calculate_gross_pay())

    def display_payroll(self) -> None:
        print("\n" + "=" * 110)
        print(f"{'BẢNG TỔNG HỢP LƯƠNG VÀ THƯỞNG KỲ: ' + self._period:^110}")
        print("=" * 110)
        print(f"{'MÃ NV':<8} | {'HỌ VÀ TÊN':<22} | {'PHÒNG BAN':<15} | {'LOẠI NHÂN SỰ':<24} | {'THƯỞNG (VNĐ)':<14} | {'TỔNG THU NHẬP':<16}")
        print("-" * 110)

        if not self._employees:
            print(f"{'(Danh sách nhân sự hiện đang trống)':^110}")
        else:
            for emp in self._employees:
                print(
                    f"{emp.employee_id:<8} | "
                    f"{emp.full_name:<22} | "
                    f"{emp.department:<15} | "
                    f"{emp.get_employee_type():<24} | "
                    f"{emp.monthly_bonus:>14,.0f} | "
                    f"{emp.calculate_gross_pay():>16,.0f}"
                )

        print("=" * 110)
        print(f"  * Tổng số nhân sự : {len(self._employees)} người")
        print(f"  * Tổng quỹ lương  : {self.calculate_total_payroll():,.0f} VNĐ")

        highest = self.find_highest_paid_employee()
        if highest:
            print(f"  * Thu nhập cao nhất: {highest.full_name} ({highest.employee_id} - {highest.department}) "
                  f"với {highest.calculate_gross_pay():,.0f} VNĐ")
        print("=" * 110 + "\n")

    @property
    def period(self) -> str:
        return self._period

    @period.setter
    def period(self, value: str) -> None:
        if not value or not isinstance(value, str) or not value.strip():
            raise ValueError("Kỳ lương không được để trống.")
        self._period = value.strip()

    @property
    def employees(self) -> List[Employee]:
        return list(self._employees)

    def __len__(self) -> int:
        return len(self._employees)
