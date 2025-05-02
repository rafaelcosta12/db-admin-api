from fastapi import HTTPException

from .. import models
from ..repositories.user_group_repository import UsersGroupRepository, GroupExistsError, OperationFailedError

class UserGroupService:
    def __init__(self, repository: UsersGroupRepository):
        self.repository = repository

    async def list_user_groups(self, filter: models.UserGroupSearchFilter) -> models.PaginationSearchResult[models.UserGroupWithDetails]:
        user_groups_list = await self.repository.list_by_filter(filter)
        user_count_by_group = await self.repository.list_user_counts_by_group([group.id for group in user_groups_list.items])
        group_id_to_user_count = {
            group.group_id: group.user_count for group in user_count_by_group
        }
        return models.PaginationSearchResult[models.UserGroupWithDetails](
            total=user_groups_list.total,
            page=user_groups_list.page,
            items=[
                models.UserGroupWithDetails(user_count=group_id_to_user_count.get(i.id, 0), **i.model_dump())
                for i in user_groups_list.items
            ]
        )
    
    async def find_user_group(self, user_group_id: int) -> models.UserGroup:
        user_group = await self.repository.find(id=user_group_id)
        if not user_group:
            raise HTTPException(status_code=404, detail="User group not found")
        return user_group
    
    async def new_user_group(self, data: models.UserGroupCreate) -> models.UserGroup:
        try:
            user_group_id = await self.repository.create(data)
            user_group = await self.repository.find(id=user_group_id)
            if not user_group:
                raise HTTPException(status_code=404, detail="User group not found")
            return user_group
        except GroupExistsError as err:
            raise HTTPException(status_code=400, detail=str(err))
    
    async def update_user_group(self, user_group_id: int, data: models.UserGroupUpdate) -> models.UserGroup:
        try:
            if not await self.repository.update(user_group_id, data):
                raise HTTPException(status_code=500, detail="Failed to update user group")
            
            fresh = await self.repository.find(id=user_group_id)
            if not fresh:
                raise HTTPException(status_code=404, detail="User group not found")
            
            return fresh
        except GroupExistsError as err:
            raise HTTPException(status_code=400, detail=str(err))
    
    async def delete_user_group(self, user_group_id: int) -> bool:
        user_group = await self.repository.delete(user_group_id)
        if not user_group:
            raise HTTPException(status_code=404, detail="User group not found")
        return user_group
    
    async def add_user_to_group(self, user_id: int, group_id: int) -> models.UserGroupMember:
        try:
            if not await self.repository.add_user_to_group(group_id, user_id):
                raise HTTPException(status_code=500, detail="Failed to add user to group")
            return models.UserGroupMember(user_id=user_id, group_id=group_id)
        except OperationFailedError as err:
            raise HTTPException(status_code=400, detail=str(err))

    async def list_user_group_members(self, user_group_id: int) -> list[models.User]:
        users = await self.repository.list_users_in_group(user_group_id)
        return users

    async def remove_user_from_group(self, user_id: int, group_id: int):
        try:
            await self.repository.remove_user_from_group(group_id, user_id)
        except OperationFailedError as err:
            raise HTTPException(status_code=400, detail=str(err))
