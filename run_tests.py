# Script thực thi toàn bộ bộ kiểm thử tự động của hệ thống tính lương và thưởng.

import sys
import unittest

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

from tests.test_assignment_cases import TestAssignmentCases
from tests.test_boundary_and_errors import TestBoundaryAndErrors


def run_all_tests():
    print("       BẮT ĐẦU CHẠY BỘ KIỂM THỬ TỰ ĐỘNG - HỆ THỐNG TÍNH LƯƠNG & THƯỞNG (PYTHON)      ")

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(TestAssignmentCases))
    suite.addTests(loader.loadTestsFromTestCase(TestBoundaryAndErrors))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n")
    print(f"  TỔNG SỐ TEST CASES ĐÃ CHẠY: {result.testsRun}")
    print(f"  THÀNH CÔNG                 : {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"  THẤT BẠI (Failures)        : {len(result.failures)}")
    print(f"  LỖI KỸ THUẬT (Errors)      : {len(result.errors)}")

    if result.wasSuccessful():
        print(">>> 100% CÁC BÀI KIỂM THỬ ĐÃ ĐẠT CHUẨN ĐỀ BÀI YÊU CẦU <<<\n")
        return 0
    else:
        print(">>> CẢNH BÁO: CÓ BÀI KIỂM THỬ KHÔNG VƯỢT QUA! <<<\n")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
