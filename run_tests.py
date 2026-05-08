#!/usr/bin/env python3
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

if __name__ == "__main__":
    args = ["-v", "--tb=short", "tests/"]
    if "--cov" in sys.argv:
        args.extend(["--cov=app", "--cov-report=term-missing"])
    sys.exit(pytest.main(args))