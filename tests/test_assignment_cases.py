# Bộ kiểm thử tự động cho các ca dữ liệu chuẩn trong Mục C của Đề tài.

import unittest
from models.salaried_employee import SalariedEmployee
from models.hourly_employee import HourlyEmployee
from models.sales_employee import SalesEmployee
from services.payroll import Payroll


class TestAssignmentCases(unittest.TestCase):
    # Kiểm tra độ chính xác của các ca dữ liệu mẫu theo yêu cầu đề bài (Mục C)

    def setUp(self):
        self.payroll = Payroll("2026-09")

        # 1. Nhân viên lương cố định E001
        self.e1 = SalariedEmployee(
            employee_id="E001",
            full_name="Nguyễn Minh An",
            department="Đào tạo",
            monthly_salary=15000000,
            responsibility_allowance=2000000
        )
        self.e1.add_bonus(1000000)  # Thưởng cố định 1.000.000

        # 2. Nhân viên theo giờ không vượt ngưỡng E002 (150 giờ)
        self.e2 = HourlyEmployee(
            employee_id="E002",
            full_name="Trần Thu Bình",
            department="Hỗ trợ",
            hourly_rate=100000,
            worked_hours=150
        )
        self.e2.add_bonus(500000)  # Thưởng 500.000

        # 3. Nhân viên theo giờ có vượt ngưỡng E003 (170 giờ)
        self.e3 = HourlyEmployee(
            employee_id="E003",
            full_name="Lê Hoàng Chi",
            department="Hỗ trợ",
            hourly_rate=100000,
            worked_hours=170
        )
        # Không có thưởng

        # 4. Nhân viên kinh doanh E004
        self.e4 = SalesEmployee(
            employee_id="E004",
            full_name="Phạm Quốc Dũng",
            department="Kinh doanh",
            base_salary=8000000,
            sales_revenue=200000000,
            commission_rate=0.05
        )
        # Thưởng theo tỷ lệ: 2% của 50.000.000 = 1.000.000
        self.e4.add_bonus(0.02, 50000000, "Thưởng vượt chỉ tiêu doanh số")

        # Thêm toàn bộ vào bảng lương
        self.payroll.add_employee(self.e1)
        self.payroll.add_employee(self.e2)
        self.payroll.add_employee(self.e3)
        self.payroll.add_employee(self.e4)

    def test_e001_salaried_employee(self):
        """E001: 15.000.000 + 2.000.000 + 1.000.000 = 18.000.000 VNĐ"""
        self.assertEqual(self.e1.calculate_gross_pay(), 18000000.0)

    def test_e002_hourly_employee_no_overtime(self):
        """E002: 150 * 100.000 + 500.000 = 15.500.000 VNĐ"""
        self.assertEqual(self.e2.calculate_gross_pay(), 15500000.0)

    def test_e003_hourly_employee_with_overtime(self):
        """E003: 160 * 100.000 + 10 * 100.000 * 1.5 = 17.500.000 VNĐ"""
        self.assertEqual(self.e3.calculate_gross_pay(), 17500000.0)

    def test_e004_sales_employee(self):
        """E004: 8.000.000 + 200.000.000 * 5% + 50.000.000 * 2% = 19.000.000 VNĐ"""
        self.assertEqual(self.e4.calculate_gross_pay(), 19000000.0)

    def test_total_payroll(self):
        """Tổng lương kỳ: 18M + 15.5M + 17.5M + 19M = 70.000.000 VNĐ"""
        self.assertEqual(self.payroll.calculate_total_payroll(), 70000000.0)

    def test_department_payroll_support(self):
        """Tổng lương phòng 'Hỗ trợ' (E002 + E003) = 15.5M + 17.5M = 33.000.000 VNĐ"""
        self.assertEqual(self.payroll.calculate_payroll_by_department("Hỗ trợ"), 33000000.0)

    def test_highest_paid_employee(self):
        """Nhân sự thu nhập cao nhất là E004 (19.000.000 VNĐ)"""
        highest = self.payroll.find_highest_paid_employee()
        self.assertIsNotNone(highest)
        self.assertEqual(highest.employee_id, "E004")
        self.assertEqual(highest.calculate_gross_pay(), 19000000.0)


if __name__ == "__main__":
    unittest.main()
