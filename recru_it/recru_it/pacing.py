"""Sequential start intervals and a deliberately narrow list salary predicate."""

from decimal import Decimal
import math
import random
import re
import time


class StartInterval:
    def __init__(self, interval, sleep, name, clock=time.monotonic, sample=random.uniform):
        low, high = interval
        if not (math.isfinite(low) and math.isfinite(high) and 0 < low <= high):
            raise ValueError('invalid start interval')
        self.interval, self.sleep, self.name = interval, sleep, name
        self.clock, self.sample = clock, sample
        self.next_start = None
        self.last_start = None

    def wait(self):
        if self.next_start is not None:
            remaining = self.next_start - self.clock()
            if remaining > 0:
                self.sleep(remaining, self.name)

    def mark_start(self):
        now = self.clock()
        gap = None if self.last_start is None else now - self.last_start
        self.last_start = now
        # Schedule from the actual start, never from an overdue deadline.
        self.next_start = now + self.sample(*self.interval)
        return gap

    def start(self):
        self.wait()
        return self.mark_start()


def salary_exclusion(card):
    """Unknown units, ambiguous formats, and values outside 100k..149,999 pass."""
    if not isinstance(card, dict):
        return None
    unit = card.get('priceDiv')
    if unit not in ('1', '3'):
        return None
    price = str(card.get('price', ''))
    if not re.fullmatch(r'(?:[0-9]+|[0-9]{1,3}(?:,[0-9]{3})+)', price):
        return None
    amount = int(price.replace(',', ''))
    # Require the displayed list amount to agree with the card's numeric field.
    pay = card.get('pay')
    if not isinstance(pay, str):
        return None
    match = re.fullmatch(r'(\d+(?:\.\d+)?)(?:만(?: 이상)?|\s*~\s*(\d+(?:\.\d+)?)만)', pay.strip())
    if not match or Decimal(match[1]) * 10000 != amount or not 100000 <= amount < 150000:
        return None
    if match[2] and Decimal(match[2]) < Decimal(match[1]):
        return None
    return 'low_daily_pay' if unit == '1' else 'low_monthly_pay'
