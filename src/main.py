"""Консольный расчёт СМО для одного процессора и пула."""

import argparse
from pathlib import Path

from metrics import availability, mm1_metrics, mmn_metrics, rho
from parameters import Parameters, read_parameters


def show_queue(params: Parameters, channels: int, single: bool) -> None:
    lam, mu = params.lam, params.mu
    name = "Один процессор" if single else "Пул процессоров"
    print(f"\n{name}, M/M/{channels}")
    load = rho(lam, mu, channels)
    print(f"Загрузка: {load:.4f}")
    if load >= 1:
        print("Система неустойчива. Стационарных показателей нет.")
        return
    result = mm1_metrics(lam, mu) if single else mmn_metrics(lam, mu, channels)
    print("Система устойчива.")
    if single:
        print(f"Вероятность простоя: {1 - load:.4%}")
    print(f"Вероятность ожидания: {result.p_wait:.4%}")
    print(f"Средняя длина очереди: {result.queue_length:.6f} заявок")
    print(f"Среднее число в системе: {result.system_length:.6f} заявок")
    print(f"Среднее ожидание: {result.wait:.6f} с")
    print(f"Среднее пребывание: {result.residence:.6f} с")
    risk = result.deadline_risk(channels * mu - lam, params.deadline)
    print(f"Вероятность ожидания дольше {params.deadline:g} с: {risk:.4%}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    default = Path(__file__).resolve().parents[1] / "data" / "variant2.csv"
    parser.add_argument("file", nargs="?", type=Path, default=default)
    args = parser.parse_args()
    try:
        params = read_parameters(args.file)
    except (ValueError, OSError) as error:
        parser.exit(2, f"Ошибка входных данных: {error}\n")
    print(f"Набор данных: {args.file.name}")
    show_queue(params, 1, single=True)
    show_queue(params, params.n, single=False)
    ready = availability(params.mtbf, params.mttr)
    print(f"\nГотовность узла: {ready:.4%}")
    print(f"Средняя доля времени в восстановлении: {1 - ready:.4%}")


if __name__ == "__main__":
    main()
