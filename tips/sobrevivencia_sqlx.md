### **🐘 Manual de Sobrevivência para `sqlx` (Go + SQL) 🏗️**  
*(Dicas cruciais para trabalhar com bancos de dados relacionais sem dor de cabeça!)*  

---

## 📌 **1. Começando com `sqlx`**  
### Instalação:  
```bash
go get github.com/jmoiron/sqlx
```

### Conexão com o Banco (PostgreSQL exemplo):  
```go
import (
    _ "github.com/lib/pq" // Driver PostgreSQL
    "github.com/jmoiron/sqlx"
)

func main() {
    db, err := sqlx.Connect("postgres", "user=postgres dbname=meubanco sslmode=disable")
    if err != nil {
        log.Fatal(err)
    }
    defer db.Close()
}
```

---

## 🛠️ **2. Operações Básicas**  
### Struct para Bind (Auto-Mapping):  
```go
type User struct {
    ID    int    `db:"id"` // Tags mapeiam para colunas
    Name  string `db:"name"`
    Email string `db:"email"`
}
```

### **Query Simples (Select):**  
```go
var users []User
err := db.Select(&users, "SELECT * FROM users WHERE age > $1", 18)
if err != nil {
    log.Fatal(err)
}
```

### **Query com Single Row:**  
```go
var user User
err := db.Get(&user, "SELECT * FROM users WHERE id = $1", 1)
if err != nil {
    if err == sql.ErrNoRows {
        log.Println("Nenhum resultado!")
    } else {
        log.Fatal(err)
    }
}
```

### **Insert/Update/Delete:**  
```go
// Insert (retornando ID)
query := `INSERT INTO users (name, email) VALUES ($1, $2) RETURNING id`
var id int
err := db.QueryRow(query, "Alice", "alice@example.com").Scan(&id)

// Update
result, err := db.Exec("UPDATE users SET name = $1 WHERE id = $2", "Alice Nova", 1)
rowsAffected, _ := result.RowsAffected()
```

---

## 🔍 **3. Features Avançadas**  
### **Named Queries (Query com Structs/Maps):**  
```go
// Usando struct
user := User{Name: "Bob", Email: "bob@example.com"}
query := "INSERT INTO users (name, email) VALUES (:name, :email)"
_, err := db.NamedExec(query, user)

// Usando map
data := map[string]interface{}{"name": "Bob", "email": "bob@example.com"}
_, err := db.NamedExec(query, data)
```

### **Transactions (Transações Seguras):**  
```go
tx, err := db.Beginx() // Transação com sqlx
if err != nil {
    log.Fatal(err)
}
defer tx.Rollback() // Rollback se falhar

// Operações dentro da transação
_, err = tx.Exec("UPDATE accounts SET balance = balance - $1 WHERE id = $2", 100, 1)
if err != nil {
    log.Fatal(err)
}

err = tx.Commit() // Confirma se tudo ok
if err != nil {
    log.Fatal(err)
}
```

### **IN Clauses (Slices Dinâmicos):**  
```go
query, args, err := sqlx.In("SELECT * FROM users WHERE id IN (?)", []int{1, 2, 3})
if err != nil {
    log.Fatal(err)
}
query = db.Rebind(query) // Ajusta placeholders para o driver
var users []User
err = db.Select(&users, query, args...)
```

---

## 🚨 **4. Armadilhas Comuns (GOTCHAS!)**  
### **1. Tags `db` são obrigatórias**  
Se não definir `db:"nome_coluna"`, o bind não funciona!  

### **2. `sql.ErrNoRows` em `Get()`**  
Sempre verifique `err == sql.ErrNoRows` em queries que retornam 0 ou 1 linha.  

### **3. Placeholders variam por banco**  
- PostgreSQL: `$1, $2`  
- MySQL: `?, ?`  
- SQLite: `?, ?`  
Use `db.Rebind()` para ajustar dinamicamente.  

### **4. Não ignore `Rows.Close()`**  
Vazamentos de conexão acontecem se não fechar:  
```go
rows, err := db.Queryx("SELECT * FROM users")
if err != nil { /* ... */ }
defer rows.Close() // ⚠️ ESSENCIAL!
```

---

## 🚀 **5. Otimizações**  
### **Prepared Statements (Reuso de Queries):**  
```go
stmt, err := db.Preparex("SELECT * FROM users WHERE id = $1")
if err != nil { /* ... */ }
defer stmt.Close()

var user User
err = stmt.Get(&user, 1)
```

### **Batch Inserts (Múltiplas Linhas):**  
```go
users := []User{
    {Name: "Alice", Email: "alice@example.com"},
    {Name: "Bob", Email: "bob@example.com"},
}

query := `INSERT INTO users (name, email) VALUES (:name, :email)`
_, err := db.NamedExec(query, users)
```

---

## 📚 **6. Recursos Úteis**  
- **[Documentação Oficial](https://pkg.go.dev/github.com/jmoiron/sqlx)**  
- **[sqlx Examples](https://github.com/jmoiron/sqlx/blob/master/README.md)**  
- **[PostgreSQL + sqlx Tutorial](https://www.calhoun.io/using-postgresql-with-go/)**  

---

## 🎯 **Filosofia `sqlx`**  
> "Combine a **simplicidade do SQL puro** com a **produtividade de structs em Go**. Evite ORMs complexos quando uma camada fina de ajuda basta."  

Pronto para dominar o `sqlx`? **Bora codar!** 👨‍💻  

```go
fmt.Println("sqlx: SQL sem boilerplate, Go sem stress! 🐘")
```  

Se ficar preso em algo, grita aqui! 😊