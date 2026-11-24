"""Стационарные характеристики очереди и готовность узла."""

from dataclasses import dataclass
from math import exp


@dataclass(frozen=True)
class Metrics:
    p_wait: float
    wait: float
    residence: float
    queue_length: float
    system_length: float

    def deadline_risk(self, spare_rate: float, deadline: float) -> float:
        return self.p_wait * exp(-spare_rate * deadline)


def rho(lam: float, mu: float, n: int) -> float:
    return lam / (n * mu)


def erlang_c(lam: float, mu: float, n: int) -> float:
    """Вероятность ожидания через устойчивую рекурсию Эрланга B."""
    load = rho(lam, mu, n)
    if load >= 1:
        raise ValueError("Стационарный режим отсутствует.")
    traffic = lam / mu
    blocking = 1.0
    for channels in range(1, n + 1):
        weight = traffic * blocking
        blocking = weight / (channels + weight)
    return blocking / (1 - load + load * blocking)


def mmn_metrics(lam: float, mu: float, n: int) -> Metrics:
    p_wait = erlang_c(lam, mu, n)
    wait = p_wait / (n * mu - lam)
    residence = wait + 1 / mu
    return Metrics(p_wait, wait, residence, lam * wait, lam * residence)


def mm1_metrics(lam: float, mu: float) -> Metrics:
    load = rho(lam, mu, 1)
    if load >= 1:
        raise ValueError("Стационарный режим отсутствует.")
    residence = 1 / (mu - lam)
    wait = load * residence
    return Metrics(load, wait, residence, lam * wait, lam * residence)


def availability(mtbf: float, mttr: float) -> float:
    return 1 / (1 + mttr / mtbf)
