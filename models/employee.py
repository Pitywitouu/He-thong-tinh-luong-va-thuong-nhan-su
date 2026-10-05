from abc import ABC, abstractmethod
from typing import List, Optional, Union, overload
from models.bonus_record import BonusRecord, BonusType


class Employee(ABC):
    def __init__(self, employee_id: str, full_name: str, department: str = "Unassigned"):
        self._validate_non_empty_str(employee_id, "Mã nhân sự không được trống")
        self._validate_non_empty_str(full_name, "Họ tên nhân sự không được trống")
        self._validate_non_empty_str(department, "Phòng ban không được trống")

        self._employee_id: str = employee_id.strip()
        self._full_name: str = full_name.strip()
        self._department: str = department.strip()
        self._monthly_bonus: float = 0.0
        self._bonus_history: List[BonusRecord] = []

    # Nạp chồng Constructor qua Classmethod
    @classmethod
    def create_basic(cls, employee_id: str, full_name: str):
        return cls(employee_id, full_name, "Unassigned")

    # Nạp chồng Phương thức Khen thưởng (Method Overloading for add_bonus)
    @overload
    def add_bonus(self, amount: float) -> None:
        """Thêm một khoản thưởng cố định."""
        ...

    @overload
    def add_bonus(self, amount: float, reason: str) -> None:
        """Thêm một khoản thưởng cố định kèm lý do."""
        ...

    @overload
    def add_bonus(self, rate: float, reference_amount: float, reason: str) -> None:
        """Tính thưởng theo tỷ lệ của một giá trị tham chiếu kèm lý do."""
        ...

    def add_bonus(self, *args, **kwargs) -> None:
        if len(args) == 1:
            amount = args[0]
            if not isinstance(amount, (int, float)) or amount <= 0:
                raise ValueError(f"Số tiền thưởng phải là số dương lớn hơn 0 (Nhận được: {amount})")
            self._monthly_bonus += float(amount)
            self._bonus_history.append(BonusRecord(float(amount), "Thưởng cố định", BonusType.FIXED))

        elif len(args) == 2:
            amount, reason = args
            if not isinstance(amount, (int, float)) or amount <= 0:
                raise ValueError(f"Số tiền thưởng phải là số dương lớn hơn 0 (Nhận được: {amount})")
            self._validate_non_empty_str(reason, "Lý do khen thưởng không được để trống.")

            self._monthly_bonus += float(amount)
            self._bonus_history.append(BonusRecord(float(amount), reason.strip(), BonusType.FIXED_WITH_REASON))

        elif len(args) == 3:
            rate, reference_amount, reason = args
            if not isinstance(rate, (int, float)) or rate <= 0 or rate > 0.5:
                raise ValueError(f"Tỷ lệ thưởng phải nằm trong khoảng (0, 0.5] (tối đa 50%). Nhận được: {rate}")
            if not isinstance(reference_amount, (int, float)) or reference_amount <= 0:
                raise ValueError(f"Giá trị tham chiếu phải lớn hơn 0 (Nhận được: {reference_amount})")
            self._validate_non_empty_str(reason, "Lý do khen thưởng không được để trống.")

            calculated_bonus = float(rate) * float(reference_amount)
            self._monthly_bonus += calculated_bonus
            full_reason = f"{reason.strip()} ({rate * 100:.1f}% của {reference_amount:,.0f} VNĐ)"
            self._bonus_history.append(BonusRecord(calculated_bonus, full_reason, BonusType.PERCENTAGE))

        else:
            raise TypeError(f"add_bonus() nhận 1, 2 hoặc 3 đối số (truyền vào {len(args)} đối số).")

    def reset_bonus(self) -> None:
        self._monthly_bonus = 0.0
        self._bonus_history.clear()

    # Các phương thức trừu tượng (Polymorphism - Đa hình)
    @abstractmethod
    def calculate_gross_pay(self) -> float:
        """Tính tổng thu nhập trước khấu trừ (Gross Pay) trong tháng."""
        pass

    @abstractmethod
    def get_employee_type(self) -> str:
        """Lấy tên loại hình nhân sự."""
        pass

    @abstractmethod
    def display_payroll_info(self) -> None:
        """Hiển thị thông tin chi tiết bảng lương của nhân sự."""
        pass

    # Properties & Setters (Đóng gói - Encapsulation)
    @property
    def employee_id(self) -> str:
        return self._employee_id

    @property
    def full_name(self) -> str:
        return self._full_name

    @full_name.setter
    def full_name(self, value: str) -> None:
        self._validate_non_empty_str(value, "Họ tên nhân sự không được để trống.")
        self._full_name = value.strip()

    @property
    def department(self) -> str:
        return self._department

    @department.setter
    def department(self, value: str) -> None:
        self._validate_non_empty_str(value, "Phòng ban không được để trống.")
        self._department = value.strip()

    @property
    def monthly_bonus(self) -> float:
        return self._monthly_bonus

    @property
    def bonus_history(self) -> List[BonusRecord]:
        return list(self._bonus_history)

    @staticmethod
    def _validate_non_empty_str(value: Optional[str], err_msg: str) -> None:
        if value is None or not isinstance(value, str) or not value.strip():
            raise ValueError(err_msg)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Employee):
            return self._employee_id == other._employee_id
        return False

    def __hash__(self) -> int:
        return hash(self._employee_id)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self._employee_id} name={self._full_name}>"

    def __str__(self) -> str:
        return (f"[{self.get_employee_type()}] {self._full_name} ({self._employee_id}) - "
                f"Phòng: {self._department} | Thưởng: {self._monthly_bonus:,.0f} đ | "
                f"Tổng thu nhập: {self.calculate_gross_pay():,.0f} đ")
