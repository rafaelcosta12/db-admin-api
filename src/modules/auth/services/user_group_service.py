from fastapi import HTTPException

from .. import models
from ..repositories.user_group_repository import UsersGroupRepository, GroupExistsError

class UserGroupService:
    def __init__(self, repository: UsersGroupRepository):
        self.repository = repository

    async def list_user_groups(self, filter: models.UserGroupSearchFilter) -> models.PaginationSearchResult[models.UserGroup]:
        return await self.repository.list_by_filter(filter)
    
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
