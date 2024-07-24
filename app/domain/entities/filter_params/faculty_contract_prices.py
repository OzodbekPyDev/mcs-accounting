from dataclasses import dataclass


@dataclass
class FacultyContractPricesFilterParams:
    with_deleted: bool | None
