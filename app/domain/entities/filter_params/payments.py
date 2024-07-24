from dataclasses import dataclass

@dataclass
class PaymentsFilterParams:
    passport_number: str | None
    contract_number: str | None
    pinfl: str | None
