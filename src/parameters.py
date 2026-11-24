"""Исходные данные одного расчёта и чтение CSV."""

import csv
from dataclasses import dataclass, fields
from math import isfinite
from pathlib import Path


@dataclass(frozen=True)
class Parameters:
    lam: float       # Интенсивность поступления, заявок/с
    mu: float        # Скорость одного процессора, заявок/с
    n: int           # Число процессоров
    deadline: float  # Допустимое ожидание в очереди, с
    mtbf: float      # Средняя наработка между отказами, ч
    mttr: float      # Среднее время восстановления, ч

    def __post_init__(self):
        for value in (self.lam, self.mu, self.deadline, self.mtbf, self.mttr):
            if not isfinite(value) or value < 0:
                raise ValueError("Величины должны быть конечными и неотрицательными.")
        if self.mu == 0 or self.mtbf == 0 or self.n < 1:
            raise ValueError("mu, mtbf и число процессоров должны быть положительными.")


def read_parameters(path: Path) -> Parameters:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        names = [field.name for field in fields(Parameters)]
        if sorted(reader.fieldnames or []) != sorted(names):
            raise ValueError("Требуются столбцы " + ", ".join(names))
        rows = list(reader)
    if len(rows) != 1 or None in rows[0] or None in rows[0].values():
        raise ValueError("Ожидается одна полная строка параметров.")
    row = rows[0]
    return Parameters(**{key: int(row[key]) if key == "n" else float(row[key])
                         for key in names})
