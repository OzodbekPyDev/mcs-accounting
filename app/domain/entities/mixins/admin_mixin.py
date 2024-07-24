from dataclasses import dataclass

from app.domain.value_objects.created_updated_by import (CreatedByVO,
                                                         DeletedByVO,
                                                         UpdatedByVO,)


@dataclass
class AdminMixinEntity:
    created_by: CreatedByVO
    updated_by: UpdatedByVO
    deleted_by: DeletedByVO
