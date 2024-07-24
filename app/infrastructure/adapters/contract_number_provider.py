from app.domain.protocols.adapters.contract_number_provider import \
    ContractNumberProvider


class SystemContractNumberProvider(ContractNumberProvider):

    def generate_contract_number(
        self,
        year: int,
        branch_suffix: str,
        faculty_suffix: str,
        edu_type_suffix: str,
        quantity: int,
        course_number: int,
    ) -> str:

        return f"{year}/{branch_suffix.upper()}{faculty_suffix.upper()}{edu_type_suffix.upper()}-{quantity:03d}/{course_number}"
