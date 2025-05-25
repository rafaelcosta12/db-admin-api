### **🔥 Manual de Sobrevivência para Gin Framework (Go) 🚀**  
*(Tudo que você precisa saber para construir APIs REST robustas com Gin sem enlouquecer!)*  

---

## **📌 1. Começando com Gin**  
### **Instalação**  
```bash
go get -u github.com/gin-gonic/gin
```

### **Hello World**  
```go
package main

import "github.com/gin-gonic/gin"

func main() {
    r := gin.Default()  // Usa middlewares padrão (logger, recovery)
    r.GET("/", func(c *gin.Context) {
        c.JSON(200, gin.H{"message": "Olá, Gin!"})
    })
    r.Run() // :8080
}
```

---

## **🚨 2. Rotas e Handlers**  
### **Métodos HTTP**  
```go
r.GET("/users", listUsers)
r.POST("/users", createUser)
r.PUT("/users/:id", updateUser)
r.DELETE("/users/:id", deleteUser)
```

### **Parâmetros de Rota**  
```go
// /users/123 → id = "123"
r.GET("/users/:id", func(c *gin.Context) {
    id := c.Param("id")
    c.JSON(200, gin.H{"id": id})
})
```

### **Query Params**  
```go
// /search?q=gin&limit=10
q := c.Query("q")          // "gin"
limit := c.Query("limit")  // "10"
```

### **Bind de JSON (Body)**  
```go
type User struct {
    Name  string `json:"name" binding:"required"`
    Email string `json:"email" binding:"required,email"`
}

func createUser(c *gin.Context) {
    var user User
    if err := c.ShouldBindJSON(&user); err != nil {
        c.JSON(400, gin.H{"error": err.Error()})
        return
    }
    c.JSON(201, user)
}
```

---

## **🛡️ 3. Middlewares**  
### **Middleware Customizado**  
```go
func AuthMiddleware(c *gin.Context) {
    token := c.GetHeader("Authorization")
    if token != "secret" {
        c.AbortWithStatusJSON(401, gin.H{"error": "Não autorizado"})
        return
    }
    c.Next() // Continua para o próximo handler
}

// Uso:
r.Use(AuthMiddleware)
```

### **Middleware de Logging**  
```go
r.Use(func(c *gin.Context) {
    start := time.Now()
    c.Next()
    fmt.Printf("%s %s %v\n", c.Request.Method, c.Request.URL, time.Since(start))
})
```

---

## **📡 4. Respostas e Erros**  
### **Formatos de Resposta**  
```go
c.JSON(200, gin.H{"success": true})  // JSON
c.String(200, "OK")                 // Texto
c.HTML(200, "index.html", nil)      // HTML
c.File("image.png")                 // Arquivo
```

### **Tratamento Centralizado de Erros**  
```go
r.Use(func(c *gin.Context) {
    c.Next() // Executa os handlers

    // Pega o primeiro erro que ocorreu
    if len(c.Errors) > 0 {
        err := c.Errors[0]
        c.JSON(500, gin.H{"error": err.Error()})
    }
})
```

---

## **⚡ 5. Otimizações e Boas Práticas**  
### **Modo Release (Desliga logs e debug)**  
```go
gin.SetMode(gin.ReleaseMode)
r := gin.New()  // Sem middlewares padrão
```

### **Grupos de Rotas (Route Groups)**  
```go
api := r.Group("/api")
{
    api.GET("/users", getUsers)
    api.POST("/users", createUser)
}
```

### **Graceful Shutdown**  
```go
server := &http.Server{
    Addr:    ":8080",
    Handler: r,
}

go func() {
    if err := server.ListenAndServe(); err != nil {
        log.Println("Server stopped:", err)
    }
}()

// Captura SIGINT (Ctrl+C)
quit := make(chan os.Signal)
signal.Notify(quit, syscall.SIGINT)
<-quit

ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
defer cancel()
server.Shutdown(ctx)
```

---

## **🚨 6. Armadilhas Comuns (GOTCHAS!)**  
### **Cuidado com `c.JSON()` + `return`**  
Se você esquecer o `return` após um `c.JSON()`, o código continua executando!  
```go
c.JSON(400, gin.H{"error": "bad request"})
return // ⚠️ SEM ISSO, O HANDLER CONTINUA!
```

### **Bind de Query Params**  
Use `ShouldBindQuery` em vez de `ShouldBindJSON` para query params:  
```go
var filter UserFilter
if err := c.ShouldBindQuery(&filter); err != nil {
    c.JSON(400, gin.H{"error": err.Error()})
    return
}
```

### **Performance em Alta Carga**  
- Use **`gin.New()`** + middlewares manuais se precisar de mais performance.  
- Evite alocações desnecessárias em handlers (ex.: reutilize buffers).  

---

## **📚 7. Recursos Úteis**  
- **[Documentação Oficial](https://gin-gonic.com/docs/)**  
- **[Gin Examples](https://github.com/gin-gonic/examples)**  
- **[Awesome Gin](https://github.com/avelino/awesome-go#web-frameworks)**  

---

## **🎯 Filosofia Gin**  
> "Gin é rápido, mas **simplicidade é rei**. Use middlewares para cross-cutting concerns, mantenha handlers enxutos e **nunca ignore erros**."  

Pronto para dominar o Gin? **Hora de codar!** 👨‍💻  

```go
fmt.Println("Gin: Quando você precisa de velocidade e simplicidade! 🚀")
```  

Se ficar travado em algo, grita! 😊