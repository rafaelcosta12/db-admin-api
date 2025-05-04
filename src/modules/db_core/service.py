from .repositories import SchemasRepository

class DbCoreService:
    def __init__(self, schemas_repository: SchemasRepository):
        self.schemas_repository = schemas_repository
    