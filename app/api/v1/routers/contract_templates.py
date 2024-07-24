from typing import Annotated
from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends, status
from fastapi_pagination import Page, paginate

from app.api.v1.schemes.contract_templates import (
    DeleteContractTemplateSchema, UpdateContractTemplateSchema,)
from app.application.dto.contract_templates import (
    ContractTemplateResponse, CreateContractTemplateRequest,
    DeleteContractTemplateRequest, GetListContractTemplatesRequest,
    UpdateContractTemplateRequest,)
from app.application.use_cases.contract_templates.create import \
    CreateContractTemplate
from app.application.use_cases.contract_templates.delete import \
    DeleteContractTemplate
from app.application.use_cases.contract_templates.get import (
    GetContractTemplateById, GetListContractTemplates,)
from app.application.use_cases.contract_templates.update import \
    UpdateContractTemplate


router = APIRouter(
    prefix="/contract-templates",
    tags=["Contract Templates"],
    route_class=DishkaRoute,
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_contract_template(
    request: CreateContractTemplateRequest,
    create_contract_template_interactor: FromDishka[CreateContractTemplate],
) -> ContractTemplateResponse:
    return await create_contract_template_interactor(request)


@router.get("/")
async def get_contract_templates(
    request: Annotated[GetListContractTemplatesRequest, Depends()],
    get_list_contract_templates_interactor: FromDishka[GetListContractTemplates],
) -> Page[ContractTemplateResponse]:
    items = await get_list_contract_templates_interactor(request)
    return paginate(items)


@router.get("/{id}")
async def get_contract_by_id(
    id: UUID,
    get_contract_template_by_id_interactor: FromDishka[GetContractTemplateById],
) -> ContractTemplateResponse:
    return await get_contract_template_by_id_interactor(id)


@router.put("/{id}")
async def update_contract_template(
    id: UUID,
    data: UpdateContractTemplateSchema,
    update_contract_template_interactor: FromDishka[UpdateContractTemplate],
) -> ContractTemplateResponse:

    request = UpdateContractTemplateRequest(
        id=id,
        branch_id=data.branch_id,
        degree_program=data.degree_program,
        language=data.language,
        info=data.info,
        name=data.name,
        html_content=data.html_content,
        is_active=data.is_active,
        start_date=data.start_date,
        first_payment_due_date=data.first_payment_due_date,
        expiration_date=data.expiration_date,
        education_years=data.education_years,
        updated_by=data.updated_by,
    )

    return await update_contract_template_interactor(request)


@router.patch("/{id}")
async def delete_contract_template(
    id: UUID,
    data: DeleteContractTemplateSchema,
    delete_contract_template_interactor: FromDishka[DeleteContractTemplate],
) -> dict[str, str]:
    request = DeleteContractTemplateRequest(
        id=id,
        deleted_by=data.deleted_by,
    )
    await delete_contract_template_interactor(request)
    return {"message": "Contract template deleted! SUCCESS!"}
