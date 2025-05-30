package main

import (
	"db-admin/core"
	"db-admin/handlers"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)

func configureCors(r *gin.Engine) {
	config := cors.DefaultConfig()
	// config.AllowAllOrigins = true
	config.AllowOrigins = []string{"*"}
	config.AllowHeaders = []string{"Authorization", "Content-Type"}
	r.Use(cors.New(config))
}

func configureConfigurationEndpoints(r *gin.Engine) {
	configurations := r.Group("configurations", core.ShouldBeAdminOr403())
	configurations.GET("users/:id", handlers.GetUserByID)
	configurations.PUT("users/:id", core.ShouldBeAdminOr403(), handlers.UpdateUser)
	configurations.DELETE("users/:id", core.ShouldBeAdminOr403(), handlers.DeleteUser)
	configurations.GET("users/me", handlers.GetMe)
	configurations.GET("users", handlers.GetUsers)
	configurations.POST("users", core.ShouldBeAdminOr403(), handlers.CreateUser)

	configurations.GET("user-groups", handlers.GetUserGroups)
	configurations.POST("user-groups", core.ShouldBeAdminOr403(), handlers.CreateUserGroup)
	configurations.PUT("user-groups/:id", core.ShouldBeAdminOr403(), handlers.UpdateUserGroup)
	configurations.DELETE("user-groups/:id", core.ShouldBeAdminOr403(), handlers.DeleteUserGroup)
	configurations.GET("user-groups/:id", handlers.GetUserGroupByID)

	configurations.GET("user-groups/:id/users", handlers.GetUserGroupMembers)
	configurations.POST("user-groups/:id/users/:id_user", core.ShouldBeAdminOr403(), handlers.AddUserToGroup)
	configurations.DELETE("user-groups/:id/users/:id_user", core.ShouldBeAdminOr403(), handlers.RemoveUserFromGroup)

	// Escopo connections é sobre comunicação direta com o banco de dados
	configurations.GET("connections", core.ShouldBeAdminOr403(), handlers.GetConnections)
	configurations.POST("connections", core.ShouldBeAdminOr403(), handlers.CreateConnection)
	configurations.GET("connections/:id/schemas", core.ShouldBeAdminOr403(), handlers.GetSchemas)
	configurations.DELETE("connections/:id", core.ShouldBeAdminOr403(), handlers.RemoveConnection)

	// Ecopo managed-tables é sobre configuração de tabelas gerenciadas
	configurations.GET("managed-tables", core.ShouldBeAdminOr403(), handlers.GetManagedTables)
	configurations.POST("managed-tables", core.ShouldBeAdminOr403(), handlers.CreateManagedTable)
}

func main() {
	core.ConfigureAppDB()
	r := gin.Default()

	r.Use(gin.Logger())
	r.Use(gin.Recovery())
	r.Use(core.AuthMiddleware())

	// configure cors
	configureCors(r)
	configureConfigurationEndpoints(r)

	auth := r.Group("auth")
	auth.POST("login", handlers.Login)
	auth.POST("logout", handlers.Logout)

	// Escopo tables é sobre tabelas do banco de dados real
	tables := r.Group("connections/:connection_id/tables")
	tables.GET("", core.ShouldBeAdminOr403(), handlers.GetTables)
	tables.POST(":table_id", core.ShouldBeAdminOr403(), handlers.CreateTableRow)

	r.Run() // :8080
}
