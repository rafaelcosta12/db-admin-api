package handlers

import (
	"db-admin/models/configurations"
	"db-admin/repositories"
	"net/http"
	"strconv"
	"time"

	"github.com/gin-gonic/gin"
)

func CreateUserGroup(c *gin.Context) {
	var input configurations.UserGroupCreate

	err := c.ShouldBindJSON(&input)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	userGroup := input.ToUserGroup()
	userGroup, err = repositories.CreateUserGroup(userGroup)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusCreated, userGroup.ToOutput())
}

func UpdateUserGroup(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid user group ID"})
		return
	}

	var input configurations.UserGroupUpdate
	err = c.ShouldBindJSON(&input)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	userGroup, err := repositories.GetUserGroupByID(id)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "User group not found"})
		return
	}

	input.Update(&userGroup)

	userGroup, err = repositories.UpdateUserGroup(userGroup)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, userGroup.ToOutput())
}

func GetUserGroup(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid user group ID"})
		return
	}

	userGroup, err := repositories.GetUserGroupByID(id)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "User group not found"})
		return
	}

	c.JSON(http.StatusOK, userGroup.ToOutput())
}

func GetUserGroups(c *gin.Context) {
	userGroups, err := repositories.GetAllUserGroups()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	items := make([]any, len(userGroups))
	for i, userGroup := range userGroups {
		items[i] = userGroup.ToOutput()
	}

	c.JSON(http.StatusOK, configurations.Pagination{
		Total: len(items),
		Page:  1,
		Items: items,
	})
}

func DeleteUserGroup(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid user group ID"})
		return
	}

	err = repositories.DeleteUserGroup(id)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusNoContent, nil)
}

func GetUserGroupByID(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid user group ID"})
		return
	}

	userGroup, err := repositories.GetUserGroupByID(id)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "User group not found"})
		return
	}

	c.JSON(http.StatusOK, userGroup.ToOutput())
}

func AddUserToGroup(c *gin.Context) {
	groupId, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid user group ID"})
		return
	}

	userId, err := strconv.Atoi(c.Param("id_user"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid user ID"})
		return
	}

	_, err = repositories.GetUserGroupByID(groupId)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "User group not found"})
		return
	}

	member := configurations.UserGroupMember{
		UserID:      userId,
		UserGroupID: groupId,
		CreatedAt:   time.Now(),
		UpdatedAt:   time.Now(),
	}

	member, err = repositories.AddUserToGroup(member)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusCreated, member.ToOutput())
}

func RemoveUserFromGroup(c *gin.Context) {
	groupId, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid user group ID"})
		return
	}

	userId, err := strconv.Atoi(c.Param("id_user"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid user ID"})
		return
	}

	err = repositories.RemoveUserFromGroup(userId, groupId)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusNoContent, nil)
}

func GetUserGroupMembers(c *gin.Context) {
	groupId, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid user group ID"})
		return
	}

	members, err := repositories.GetUserGroupMembers(groupId)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	var memberOutputs []configurations.UserOutput
	for _, member := range members {
		memberOutputs = append(memberOutputs, member.ToOutput())
	}

	c.JSON(http.StatusOK, memberOutputs)
}
