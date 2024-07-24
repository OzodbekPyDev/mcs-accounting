import pdfkit
from jinja2 import Template

from app.domain.protocols.adapters.file_manager import FileManager


class JinjaPdfkitFileManager(FileManager):

    def render_html_content(
        self,
        html_content: str,
        contract_number: str,
        student_data: dict,
    ) -> str:
        html_template = Template(html_content)
        rendered_html_content = html_template.render(
            contract_number=contract_number, student=student_data
        )

        return rendered_html_content

    def generate_binary_code_of_pdf_file(
        self,
        html_content: str,
    ) -> bytes | None:
        binary_code_pdf = pdfkit.from_string(html_content, output_path=None)

        return binary_code_pdf if binary_code_pdf else None
