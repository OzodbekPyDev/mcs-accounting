from typing import Protocol


class FileManager(Protocol):

    def render_html_content(
        self,
        html_content: str,
        contract_number: str,
        student_data: dict,
    ) -> str:
        raise NotImplementedError

    def generate_binary_code_of_pdf_file(
        self,
        html_content: str,
    ) -> bytes:
        raise NotImplementedError
