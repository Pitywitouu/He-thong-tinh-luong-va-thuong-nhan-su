"""
Chương trình chính (Main Console Application) cho Hệ thống Tính lương và Thưởng Nhân sự.
Bao gồm:
1. Chế độ Demo tự động chạy bộ dữ liệu kiểm thử chuẩn
2. Chế độ Menu tương tác cho phép quản lý nhân sự, ghi nhận thưởng, tính bảng lương
"""

import sys

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

from models.salaried_employee import SalariedEmployee
from models.hourly_employee import HourlyEmployee
from models.sales_employee import SalesEmployee
from services.payroll import Payroll
from utils.formatter import format_vnd


def run_assignment_demo() -> Payroll:
    """
    Chạy trình diễn bộ dữ liệu chuẩn:
    - E001: Nguyễn Minh An (Salaried) -> 18.000.000 VNĐ
    - E002: Trần Thu Bình (Hourly, 150h) -> 15.500.000 VNĐ
    - E003: Lê Hoàng Chi (Hourly, 170h) -> 17.500.000 VNĐ
    - E004: Phạm Quốc Dũng (Sales) -> 19.000.000 VNĐ
    Tổng kỳ: 70.000.000 VNĐ | Phòng Hỗ trợ: 33.000.000 VNĐ | Cao nhất: E004
    """
    print("\n")
    print("      KHỞI TẠO BẢNG LƯƠNG KỲ 2026-09 VỚI BỘ DỮ LIỆU CHUẨN (MỤC C)     ")

    payroll = Payroll("2026-09")

    # 1. Nhân viên lương cố định E001
    print("\n[1] Khởi tạo Nhân viên Lương cố định E001:")
    e1 = SalariedEmployee(
        employee_id="E001",
        full_name="Nguyễn Minh An",
        department="Đào tạo",
        monthly_salary=15000000,
        responsibility_allowance=2000000
    )
    # Thưởng cố định: 1.000.000 (Nạp chồng phiên bản 1)
    e1.add_bonus(1000000)
    payroll.add_employee(e1)
    e1.display_payroll_info()

    # 2. Nhân viên theo giờ không vượt ngưỡng E002 (150h)
    print("\n[2] Khởi tạo Nhân viên Theo giờ E002 (150 giờ <= 160h chuẩn):")
    e2 = HourlyEmployee(
        employee_id="E002",
        full_name="Trần Thu Bình",
        department="Hỗ trợ",
        hourly_rate=100000,
        worked_hours=150
    )
    # Thưởng cố định có lý do: 500.000 (Nạp chồng phiên bản 2)
    e2.add_bonus(500000, "Thưởng hỗ trợ khách hàng xuất sắc")
    payroll.add_employee(e2)
    e2.display_payroll_info()

    # 3. Nhân viên theo giờ có vượt ngưỡng E003 (170h)
    print("\n[3] Khởi tạo Nhân viên Theo giờ E003 (170 giờ > 160h chuẩn -> 10h OT x 1.5):")
    e3 = HourlyEmployee(
        employee_id="E003",
        full_name="Lê Hoàng Chi",
        department="Hỗ trợ",
        hourly_rate=100000,
        worked_hours=170
    )
    payroll.add_employee(e3)
    e3.display_payroll_info()

    # 4. Nhân viên kinh doanh E004
    print("\n[4] Khởi tạo Nhân viên Kinh doanh E004 (Hoa hồng 5% + Thưởng 2% của 50M):")
    e4 = SalesEmployee(
        employee_id="E004",
        full_name="Phạm Quốc Dũng",
        department="Kinh doanh",
        base_salary=8000000,
        sales_revenue=200000000,
        commission_rate=0.05
    )
    # Thưởng theo tỷ lệ tham chiếu: 2% của 50.000.000 (Nạp chồng phiên bản 3)
    e4.add_bonus(0.02, 50000000, "Thưởng đạt mốc doanh số quý")
    payroll.add_employee(e4)
    e4.display_payroll_info()

    # Hiển thị bảng tổng hợp đa hình
    payroll.display_payroll()

    # Kiểm tra tổng hợp theo phòng ban
    dept_support_total = payroll.calculate_payroll_by_department("Hỗ trợ")
    print(f">> Tổng lương phòng 'Hỗ trợ' (E002 + E003): {dept_support_total:,.0f} VNĐ (Kỳ vọng: 33.000.000 VNĐ)")

    return payroll


def interactive_menu(payroll: Payroll):
    """Giao diện Menu dòng lệnh tương tác cho người dùng."""
    while True:
        print("\n")
        print("          HỆ THỐNG QUẢN LÝ LƯƠNG & THƯỞNG NHÂN SỰ")
        print("1. Xem toàn bộ bảng tổng hợp lương kỳ hiện tại")
        print("2. Thêm nhân viên lương cố định (SalariedEmployee)")
        print("3. Thêm nhân viên theo giờ (HourlyEmployee)")
        print("4. Thêm nhân viên kinh doanh (SalesEmployee)")
        print("5. Thêm thưởng cho nhân viên (Nạp chồng 3 cách)")
        print("6. Cập nhật doanh số cho nhân viên kinh doanh")
        print("7. Tra cứu thông tin chi tiết nhân viên theo Mã")
        print("8. Tính tổng lương theo phòng ban")
        print("9. Tìm nhân viên có thu nhập cao nhất")
        print("10. Đặt lại thưởng (Reset bonus) cho kỳ mới")
        print("0. Thoát chương trình")

        choice = input("Vui lòng chọn chức năng (0-10): ").strip()

        if choice == "0":
            print("Đã thoát chương trình. Xin cảm ơn!")
            break

        elif choice == "1":
            payroll.display_payroll()

        elif choice == "2":
            try:
                emp_id = input("Nhập mã nhân sự: ").strip()
                name = input("Nhập họ và tên: ").strip()
                dept = input("Nhập phòng ban (Enter để mặc định 'Unassigned'): ").strip()
                if not dept:
                    dept = "Unassigned"
                salary = float(input("Nhập lương cố định tháng (VNĐ): ").strip() or 0)
                allowance = float(input("Nhập phụ cấp trách nhiệm (VNĐ): ").strip() or 0)

                emp = SalariedEmployee(emp_id, name, dept, salary, allowance)
                payroll.add_employee(emp)
                print(f">> Đã thêm thành công nhân viên {name} ({emp_id})!")
            except Exception as ex:
                print(f"[LỖI]: {ex}")

        elif choice == "3":
            try:
                emp_id = input("Nhập mã nhân sự: ").strip()
                name = input("Nhập họ và tên: ").strip()
                dept = input("Nhập phòng ban (Enter để mặc định 'Unassigned'): ").strip()
                if not dept:
                    dept = "Unassigned"
                rate = float(input("Nhập đơn giá giờ (VNĐ/giờ): ").strip() or 0)
                hours = float(input("Nhập số giờ làm (0-250 giờ): ").strip() or 0)

                emp = HourlyEmployee(emp_id, name, dept, rate, hours)
                payroll.add_employee(emp)
                print(f">> Đã thêm thành công nhân viên {name} ({emp_id})!")
            except Exception as ex:
                print(f"[LỖI]: {ex}")

        elif choice == "4":
            try:
                emp_id = input("Nhập mã nhân sự: ").strip()
                name = input("Nhập họ và tên: ").strip()
                dept = input("Nhập phòng ban (Enter để mặc định 'Unassigned'): ").strip()
                if not dept:
                    dept = "Unassigned"
                base_sal = float(input("Nhập lương cơ bản (VNĐ): ").strip() or 0)
                revenue = float(input("Nhập doanh số bán hàng (VNĐ): ").strip() or 0)
                rate = float(input("Nhập tỷ lệ hoa hồng (0.0 đến 0.3, ví dụ 0.05 là 5%): ").strip() or 0)

                emp = SalesEmployee(emp_id, name, dept, base_sal, revenue, rate)
                payroll.add_employee(emp)
                print(f">> Đã thêm thành công nhân viên {name} ({emp_id})!")
            except Exception as ex:
                print(f"[LỖI]: {ex}")

        elif choice == "5":
            emp_id = input("Nhập mã nhân sự cần khen thưởng: ").strip()
            emp = payroll.find_employee(emp_id)
            if not emp:
                print(f"[LỖI]: Không tìm thấy nhân sự mang mã '{emp_id}'!")
                continue

            print("\nChọn hình thức thưởng (Nạp chồng add_bonus):")
            print("1. Thưởng một khoản cố định")
            print("2. Thưởng một khoản cố định kèm lý do")
            print("3. Thưởng theo tỷ lệ tham chiếu (ví dụ: % doanh số/dự án) kèm lý do")
            b_choice = input("Chọn (1-3): ").strip()

            try:
                if b_choice == "1":
                    amt = float(input("Nhập số tiền thưởng (VNĐ): ").strip())
                    emp.add_bonus(amt)
                    print(f">> Đã ghi nhận thưởng {amt:,.0f} VNĐ cho {emp.full_name}!")
                elif b_choice == "2":
                    amt = float(input("Nhập số tiền thưởng (VNĐ): ").strip())
                    reason = input("Nhập lý do khen thưởng: ").strip()
                    emp.add_bonus(amt, reason)
                    print(f">> Đã ghi nhận thưởng {amt:,.0f} VNĐ cho {emp.full_name}!")
                elif b_choice == "3":
                    rate = float(input("Nhập tỷ lệ thưởng (ví dụ 0.02 là 2%, tối đa 0.5): ").strip())
                    ref = float(input("Nhập giá trị tham chiếu (VNĐ): ").strip())
                    reason = input("Nhập lý do khen thưởng: ").strip()
                    emp.add_bonus(rate, ref, reason)
                    print(f">> Đã ghi nhận thưởng {rate * ref:,.0f} VNĐ ({rate*100:.1f}% của {ref:,.0f} VNĐ) cho {emp.full_name}!")
                else:
                    print("[LỖI]: Lựa chọn không hợp lệ!")
            except Exception as ex:
                print(f"[LỖI]: {ex}")

        elif choice == "6":
            emp_id = input("Nhập mã nhân viên kinh doanh: ").strip()
            emp = payroll.find_employee(emp_id)
            if not emp:
                print(f"[LỖI]: Không tìm thấy nhân sự '{emp_id}'!")
            elif not isinstance(emp, SalesEmployee):
                print(f"[LỖI]: Nhân sự '{emp_id}' ({emp.get_employee_type()}) không phải là SalesEmployee!")
            else:
                try:
                    new_rev = float(input(f"Nhập doanh số mới cho {emp.full_name} (Hiện tại: {emp.sales_revenue:,.0f} VNĐ): ").strip())
                    emp.update_sales_revenue(new_rev)
                    print(f">> Cập nhật doanh số thành công: {new_rev:,.0f} VNĐ!")
                except Exception as ex:
                    print(f"[LỖI]: {ex}")

        elif choice == "7":
            emp_id = input("Nhập mã nhân sự cần tra cứu: ").strip()
            emp = payroll.find_employee(emp_id)
            if emp:
                emp.display_payroll_info()
            else:
                print(f"[LỖI]: Không tìm thấy nhân sự có mã '{emp_id}'!")

        elif choice == "8":
            dept = input("Nhập tên phòng ban cần tính tổng lương: ").strip()
            total = payroll.calculate_payroll_by_department(dept)
            print(f">> Tổng lương của phòng ban '{dept}': {total:,.0f} VNĐ")

        elif choice == "9":
            highest = payroll.find_highest_paid_employee()
            if highest:
                print("\n>>> NHÂN SỰ CÓ THU NHẬP CAO NHẤT KỲ:")
                highest.display_payroll_info()
            else:
                print("Bảng lương hiện đang trống.")

        elif choice == "10":
            confirm = input(f"Bạn có chắc muốn đặt lại thưởng của toàn bộ {len(payroll)} nhân sự về 0? (y/N): ").strip()
            if confirm.lower() == "y":
                for emp in payroll.employees:
                    emp.reset_bonus()
                print(">> Đã đặt lại thưởng của toàn bộ nhân sự về 0!")

        else:
            print("[LỖI]: Lựa chọn không hợp lệ. Vui lòng chọn từ 0 đến 10.")


def main():
    payroll = run_assignment_demo()

    # print("\nBạn có muốn mở Menu tương tác để thao tác trực tiếp không?")
    ans = input("Nhập 'y' để mở Menu, hoặc nhấn Enter để kết thúc: ").strip().lower()
    if ans == "y":
        interactive_menu(payroll)


if __name__ == "__main__":
    main()
