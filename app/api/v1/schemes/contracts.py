from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class UpdateContractSchema:
    template_id: UUID
    html_content: str
    start_date: datetime
    first_payment_due_date: datetime
    expiration_date: datetime
    education_years: str
    is_archived: bool
    updated_by: UUID
