"""
Bộ kiểm thử tự động cho các trường hợp kiểm thử biên và kiểm thử lỗi (Mục C.1).
Bao gồm hơn 15 trường hợp kiểm thử chặt chẽ theo tất cả các bất biến và quy tắc nghiệp vụ.
"""

import unittest
from models.salaried_employee import SalariedEmployee
from models.hourly_employee import HourlyEmployee
from models.sales_employee import SalesEmployee
from services.payroll import Payroll


class TestBoundaryAndErrors(unittest.TestCase):
    # Kiểm tra xử lý ngoại lệ và giá trị biên.

    # 1. Kiểm tra bất biến chung của Employee

    def test_tc01_empty_employee_id(self):
        """Mã nhân sự rỗng -> Báo lỗi ValueError."""
        with self.assertRaises(ValueError):
            SalariedEmployee("", "Nguyễn Văn A")

    def test_tc02_empty_full_name(self):
        """Họ tên nhân sự rỗng -> Báo lỗi ValueError."""
        with self.assertRaises(ValueError):
            SalariedEmployee("E100", "   ")

    def test_tc03_empty_department(self):
        """Phòng ban rỗng -> Báo lỗi ValueError."""
        with self.assertRaises(ValueError):
            SalariedEmployee("E100", "Nguyễn Văn A", "   ")

    # 2. Kiểm tra bất biến của SalariedEmployee

    def test_tc04_negative_monthly_salary(self):
        """Lương cố định tháng < 0 -> Báo lỗi ValueError."""
        with self.assertRaises(ValueError):
            SalariedEmployee("E101", "Trần Văn B", "IT", -1000000, 500000)

    def test_tc05_negative_responsibility_allowance(self):
        """Phụ cấp trách nhiệm < 0 -> Báo lỗi ValueError."""
        with self.assertRaises(ValueError):
            SalariedEmployee("E102", "Lê Văn C", "IT", 10000000, -200000)

    # 3. Kiểm tra bất biến và giá trị biên của HourlyEmployee 

    def test_tc06_negative_hourly_rate(self):
        """Đơn giá giờ < 0 -> Báo lỗi ValueError."""
        with self.assertRaises(ValueError):
            HourlyEmployee("E103", "Phạm Thị D", "Hỗ trợ", -50000, 100)

    def test_tc07_negative_worked_hours(self):
        """Số giờ làm < 0 -> Báo lỗi ValueError."""
        with self.assertRaises(ValueError):
            HourlyEmployee("E104", "Hoàng Văn E", "Hỗ trợ", 100000, -1)

    def test_tc08_worked_hours_exceed_max_250(self):
        """Số giờ làm > 250 -> Báo lỗi ValueError."""
        with self.assertRaises(ValueError):
            HourlyEmployee("E105", "Đỗ Thị F", "Hỗ trợ", 100000, 250.5)

    def test_tc09_boundary_worked_hours_zero(self):
        """Biên số giờ làm = 0 -> Lương = 0."""
        emp = HourlyEmployee("E106", "Biên Không Giờ", "Hỗ trợ", 100000, 0)
        self.assertEqual(emp.calculate_gross_pay(), 0.0)

    def test_tc10_boundary_worked_hours_exact_160(self):
        """Biên số giờ làm = đúng 160h (chưa vượt ngưỡng OT) -> Lương = 160 * 100k = 16M."""
        emp = HourlyEmployee("E107", "Biên 160 Giờ", "Hỗ trợ", 100000, 160)
        self.assertEqual(emp.calculate_gross_pay(), 16000000.0)
        self.assertEqual(emp.overtime_hours, 0.0)

    def test_tc11_boundary_worked_hours_exact_max_250(self):
        """Biên cực đại 250h -> 160 * 100k + 90 * 100k * 1.5 = 16M + 13.5M = 29.5M."""
        emp = HourlyEmployee("E108", "Biên Cực Đại 250 Giờ", "Hỗ trợ", 100000, 250)
        self.assertEqual(emp.calculate_gross_pay(), 29500000.0)
        self.assertEqual(emp.overtime_hours, 90.0)

    # 4. Kiểm tra bất biến của SalesEmployee

    def test_tc12_negative_base_salary(self):
        """Lương cơ bản Sales < 0 -> Báo lỗi ValueError."""
        with self.assertRaises(ValueError):
            SalesEmployee("E109", "Vũ Văn G", "Kinh doanh", -5000, 1000000, 0.1)

    def test_tc13_negative_sales_revenue(self):
        """Doanh số cập nhật < 0 -> Báo lỗi ValueError."""
        emp = SalesEmployee("E110", "Ngô Thị H", "Kinh doanh", 5000000, 10000000, 0.1)
        with self.assertRaises(ValueError):
            emp.update_sales_revenue(-100000)

    def test_tc14_commission_rate_exceed_30_percent(self):
        """Tỷ lệ hoa hồng > 0.3 (ví dụ 0.35) -> Báo lỗi ValueError."""
        with self.assertRaises(ValueError):
            SalesEmployee("E111", "Đinh Văn I", "Kinh doanh", 5000000, 10000000, 0.35)

    def test_tc15_commission_rate_negative(self):
        """Tỷ lệ hoa hồng < 0 -> Báo lỗi ValueError."""
        with self.assertRaises(ValueError):
            SalesEmployee("E112", "Bùi Thị K", "Kinh doanh", 5000000, 10000000, -0.05)

    # 5. Kiểm tra nạp chồng add_bonus và quy tắc thưởng

    def test_tc16_add_bonus_non_positive_amount(self):
        """Thưởng số tiền <= 0 -> Báo lỗi ValueError."""
        emp = SalariedEmployee("E113", "Test Bonus Zero")
        with self.assertRaises(ValueError):
            emp.add_bonus(0)
        with self.assertRaises(ValueError):
            emp.add_bonus(-500000)

    def test_tc17_add_bonus_empty_reason(self):
        """Thưởng có lý do nhưng để chuỗi rỗng -> Báo lỗi ValueError."""
        emp = SalariedEmployee("E114", "Test Bonus Empty Reason")
        with self.assertRaises(ValueError):
            emp.add_bonus(500000, "   ")

    def test_tc18_add_bonus_rate_exceed_limit(self):
        """Thưởng theo tỷ lệ với rate <= 0 hoặc rate > 0.5 (ví dụ 0.6) -> Báo lỗi ValueError."""
        emp = SalariedEmployee("E115", "Test Bonus Rate Over Limit")
        with self.assertRaises(ValueError):
            emp.add_bonus(0.6, 10000000, "Thưởng 60%")
        with self.assertRaises(ValueError):
            emp.add_bonus(0.0, 10000000, "Thưởng 0%")

    def test_tc19_add_bonus_negative_reference_amount(self):
        """Thưởng theo tỷ lệ với referenceAmount <= 0 -> Báo lỗi ValueError."""
        emp = SalariedEmployee("E116", "Test Bonus Negative Ref")
        with self.assertRaises(ValueError):
            emp.add_bonus(0.1, -500000, "Ref âm")

    def test_tc20_reset_bonus(self):
        """Kiểm tra reset_bonus(): đặt lại monthlyBonus về 0 và xóa lịch sử."""
        emp = SalariedEmployee("E117", "Test Reset Bonus", "IT", 10000000, 2000000)
        emp.add_bonus(1500000)
        self.assertEqual(emp.calculate_gross_pay(), 13500000.0)
        self.assertEqual(len(emp.bonus_history), 1)

        emp.reset_bonus()
        self.assertEqual(emp.monthly_bonus, 0.0)
        self.assertEqual(emp.calculate_gross_pay(), 12000000.0)
        self.assertEqual(len(emp.bonus_history), 0)

    # 6. Kiểm tra ràng buộc và xử lý của Payroll

    def test_tc21_payroll_duplicate_employee_id(self):
        """Thêm nhân sự trùng ID vào cùng kỳ lương -> Báo lỗi ValueError."""
        payroll = Payroll("2026-09")
        e1 = SalariedEmployee("E001", "Nguyễn Minh An", "Đào tạo", 15000000, 2000000)
        e_duplicate = HourlyEmployee("E001", "Trùng Mã E001", "Hỗ trợ", 100000, 100)

        payroll.add_employee(e1)
        with self.assertRaises(ValueError):
            payroll.add_employee(e_duplicate)

    def test_tc22_payroll_add_none_or_invalid(self):
        """Thêm đối tượng None vào Payroll -> Báo lỗi ValueError."""
        payroll = Payroll("2026-09")
        with self.assertRaises(ValueError):
            payroll.add_employee(None)

    def test_tc23_empty_payroll_safe_handling(self):
        """Bảng lương rỗng xử lý an toàn: Tổng = 0, Highest = None."""
        empty_payroll = Payroll("2026-10")
        self.assertEqual(empty_payroll.calculate_total_payroll(), 0.0)
        self.assertEqual(empty_payroll.calculate_payroll_by_department("Kinh doanh"), 0.0)
        self.assertIsNone(empty_payroll.find_highest_paid_employee())


if __name__ == "__main__":
    unittest.main()
