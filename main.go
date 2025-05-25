package main

import (
	"db-admin/core"
	"db-admin/handlers"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)

func main() {
	core.ConfigureAppDB()
	r := gin.Default()

	r.Use(gin.Logger())
	r.Use(gin.Recovery())
	r.Use(core.AuthMiddleware())

	// configure cors
	config := cors.DefaultConfig()
	// config.AllowAllOrigins = true
	config.AllowOrigins = []string{"*"}
	config.AllowHeaders = []string{"Authorization", "Content-Type"}
	r.Use(cors.New(config))

	auth := r.Group("/auth")
	auth.POST("login", handlers.Login)
	auth.POST("logout", handlers.Logout)

	users := r.Group("/users")
	users.GET(":id", handlers.GetUserByID)
	users.PUT(":id", core.ShouldBeAdminOr403(), handlers.UpdateUser)
	users.DELETE(":id", core.ShouldBeAdminOr403(), handlers.DeleteUser)
	users.GET("me", handlers.GetMe)
	users.GET("", handlers.GetUsers)
	users.POST("", core.ShouldBeAdminOr403(), handlers.CreateUser)

	userGroups := r.Group("/user-groups")
	userGroups.GET("", handlers.GetUserGroups)
	userGroups.POST("", core.ShouldBeAdminOr403(), handlers.CreateUserGroup)
	userGroups.PUT(":id", core.ShouldBeAdminOr403(), handlers.UpdateUserGroup)
	userGroups.DELETE(":id", core.ShouldBeAdminOr403(), handlers.DeleteUserGroup)
	userGroups.GET(":id", handlers.GetUserGroupByID)

	userGroupsMembers := r.Group("/user-groups/:id/users")
	userGroupsMembers.GET("", handlers.GetUserGroupMembers)
	userGroupsMembers.POST(":id_user", core.ShouldBeAdminOr403(), handlers.AddUserToGroup)
	userGroupsMembers.DELETE(":id_user", core.ShouldBeAdminOr403(), handlers.RemoveUserFromGroup)

	// Escopo connections é sobre comunicação direta com o banco de dados
	connections := r.Group("/connections")
	connections.GET("", core.ShouldBeAdminOr403(), handlers.GetConnections)
	connections.POST("", core.ShouldBeAdminOr403(), handlers.CreateConnection)
	connections.GET(":id/schemas", core.ShouldBeAdminOr403(), handlers.GetSchemas)
	connections.DELETE(":id", core.ShouldBeAdminOr403(), handlers.RemoveConnection)

	r.Run() // :8080
}
