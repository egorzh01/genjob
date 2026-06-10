from __future__ import annotations

from random import randint


class CodeGenerator:
    def generate_code(self) -> str:
        return str(randint(100000, 999999))


class MockCodeGenerator:
    def generate_code(self) -> str:
        return "123456"
