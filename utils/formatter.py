# Module tiện ích định dạng số liệu và tiền tệ Việt Nam (VNĐ).
def format_vnd(amount: float) -> str:
    """Định dạng số tiền sang chuẩn hiển thị VNĐ."""
    return f"{amount:,.0f} VNĐ"


def format_percentage(rate: float) -> str:
    """Định dạng tỷ lệ phần trăm."""
    return f"{rate * 100:.1f}%"
