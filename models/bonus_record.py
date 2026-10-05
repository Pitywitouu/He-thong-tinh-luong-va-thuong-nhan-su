"""
Module định nghĩa lớp BonusRecord đại diện cho bản ghi khen thưởng.
Giúp theo dõi lịch sử thưởng một cách có cấu trúc, minh bạch, tránh dùng mảng song song.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class BonusType(Enum):
    FIXED = "FIXED"                           # Thưởng cố định không lý do
    FIXED_WITH_REASON = "FIXED_WITH_REASON"   # Thưởng cố định có lý do
    PERCENTAGE = "PERCENTAGE"                 # Thưởng theo tỷ lệ tham chiếu


@dataclass(frozen=True)
class BonusRecord:
    """Bản ghi lưu trữ một khoản thưởng của nhân sự."""
    amount: float
    reason: str
    bonus_type: BonusType
    recorded_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if self.amount <= 0:
            raise ValueError(f"Số tiền thưởng phải lớn hơn 0 (Nhận được: {self.amount})")
        if not self.reason or not self.reason.strip():
            raise ValueError("Lý do khen thưởng không được để trống.")

    def __str__(self) -> str:
        return f"Thưởng: {self.amount:,.0f} VNĐ | Lý do: {self.reason} | Loại: {self.bonus_type.value}"
