import json
from typing import Annotated, Any, List
from fastapi import Depends, APIRouter, Request, HTTPException
from psycopg2.extensions import connection

from ..schemas import TableDetails, TableRowOperation, TableRows
from ..repository import Repository
from ..database import get_db_connection


router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("")
async def get_table_list(
    database: Annotated[connection, Depends(get_db_connection)]
) -> List[TableDetails]:
    return Repository(database).get_table_details()


@router.get("/{table_name}/details")
async def get_table_details(
    table_name: str,
    database: Annotated[connection, Depends(get_db_connection)]
) -> TableDetails:
    schema, table = table_name.split(".")
    return Repository(database).get_table_details_from_table_name(schema, table)


@router.get("/{table_name}")
async def list_table_rows(
    table_name: str,
    database: Annotated[connection, Depends(get_db_connection)]
) -> TableRows:
    repository = Repository(database)
    schema, table = table_name.split(".")
    return TableRows(data=repository.list_rows(schema, table), total=repository.count_rows(schema, table))


@router.get("/{table_name}/{row_pk}")
async def get_row_by_pk(
    table_name: str, 
    row_pk: str, 
    database: Annotated[connection, Depends(get_db_connection)],
) -> dict[str, Any]:
    repository = Repository(database)
    schema, table = table_name.split(".")
    try:
        return repository.get_row_by_pk(schema, table, row_pk)
    except Exception as e:
        print(e)
        print(e.with_traceback())
        raise HTTPException(500, str(e))


@router.post("/{table_name}/row")
async def create_row(
    table_name: str, 
    request: Request, 
    database: Annotated[connection, Depends(get_db_connection)]
) -> TableRowOperation:
    body = json.loads(await request.body())
    repository = Repository(database)
    schema, table = table_name.split(".")
    try:
        pk = repository.insert(schema, table, body)
        created = repository.get_row_by_pk(schema, table, pk)
        return TableRowOperation(pk=pk, message="Operation success", data=created)
    except Exception as e:
        print(e)
        print(e.with_traceback())
        raise HTTPException(500, str(e))


@router.patch("/{table_name}/row/{row_pk}")
async def update_row(
    table_name: str, 
    row_pk: int, 
    request: Request,
    database: Annotated[connection, Depends(get_db_connection)],
) -> TableRowOperation:
    body = json.loads(await request.body())
    repository = Repository(database)
    schema, table = table_name.split(".")

    try:
        repository.update(schema, table, row_pk, body)
        data = repository.get_row_by_pk(schema, table, row_pk)
        return TableRowOperation(pk=row_pk, message="Operation success", data=data)
    except Exception as e:
        print(e)
        raise HTTPException(500, str(e))


@router.delete("/{table_name}/row/{row_pk}")
async def delete_row(
    table_name: str, 
    row_pk: int, 
    database: Annotated[connection, Depends(get_db_connection)],
) -> TableRowOperation:
    repository = Repository(database)
    schema, table = table_name.split(".")

    try:
        repository.delete(schema, table, row_pk)
        return TableRowOperation(pk=row_pk, message="Operation success", data=None)
    except Exception as e:
        print(e)
        raise HTTPException(500, str(e))
