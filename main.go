package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"log"
	"net/http"

	_ "github.com/go-sql-driver/mysql"
	"github.com/gorilla/mux"
)

// Modelo de datos
type Empleado struct {
	ID        int    `json:"emp_no"`
	BirthDate string `json:"birth_date"`
	FirstName string `json:"first_name"`
	LastName  string `json:"last_name"`
	Gender    string `json:"gender"`
	HireDate  string `json:"hire_date"`
}

var db *sql.DB

func main() {
	var err error
	// Conexión a la base de datos en Docker
	dsn := "root:password123@tcp(db:3306)/employees"
	db, err = sql.Open("mysql", dsn)
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	r := mux.NewRouter()

	// Endpoints del CRUD
	r.HandleFunc("/empleados", getEmpleados).Methods("GET")           // Leer lista
	r.HandleFunc("/empleados/{id}", getEmpleado).Methods("GET")       // Leer uno solo
	r.HandleFunc("/empleados", createEmpleado).Methods("POST")        // Crear
	r.HandleFunc("/empleados/{id}", updateEmpleado).Methods("PUT")    // Actualizar
	r.HandleFunc("/empleados/{id}", deleteEmpleado).Methods("DELETE") // Borrar

	fmt.Println("Servidor Go corriendo en puerto 8080...")
	log.Fatal(http.ListenAndServe(":8080", r))
}

// 1. OBTENER LISTA (Límite 10 para rendimiento)
func getEmpleados(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	rows, err := db.Query("SELECT emp_no, birth_date, first_name, last_name, gender, hire_date FROM employees LIMIT 10")
	if err != nil {
		http.Error(w, err.Error(), 500)
		return
	}
	defer rows.Close()

	var empleados []Empleado
	for rows.Next() {
		var e Empleado
		rows.Scan(&e.ID, &e.BirthDate, &e.FirstName, &e.LastName, &e.Gender, &e.HireDate)
		empleados = append(empleados, e)
	}
	json.NewEncoder(w).Encode(empleados)
}

// 2. OBTENER UNO (Corregido para traer todo)
func getEmpleado(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	params := mux.Vars(r)
	var e Empleado
	
	query := "SELECT emp_no, birth_date, first_name, last_name, gender, hire_date FROM employees WHERE emp_no = ?"
	err := db.QueryRow(query, params["id"]).Scan(&e.ID, &e.BirthDate, &e.FirstName, &e.LastName, &e.Gender, &e.HireDate)

	if err != nil {
		http.NotFound(w, r)
		return
	}
	json.NewEncoder(w).Encode(e)
}

// 3. CREAR
func createEmpleado(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	var e Empleado
	json.NewDecoder(r.Body).Decode(&e)

	query := "INSERT INTO employees (emp_no, birth_date, first_name, last_name, gender, hire_date) VALUES (?, ?, ?, ?, ?, ?)"
	_, err := db.Exec(query, e.ID, e.BirthDate, e.FirstName, e.LastName, e.Gender, e.HireDate)
	
	if err != nil {
		http.Error(w, err.Error(), 500)
		return
	}
	w.WriteHeader(http.StatusCreated)
	json.NewEncoder(w).Encode(e)
}

// 4. ACTUALIZAR (Ahora edita más campos)
func updateEmpleado(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	params := mux.Vars(r)
	var e Empleado
	json.NewDecoder(r.Body).Decode(&e)

	query := "UPDATE employees SET first_name = ?, last_name = ?, gender = ? WHERE emp_no = ?"
	_, err := db.Exec(query, e.FirstName, e.LastName, e.Gender, params["id"])

	if err != nil {
		http.Error(w, err.Error(), 500)
		return
	}
	fmt.Fprintf(w, "Empleado %s actualizado correctamente", params["id"])
}

// 5. BORRAR
func deleteEmpleado(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	params := mux.Vars(r)
	
	_, err := db.Exec("DELETE FROM employees WHERE emp_no = ?", params["id"])
	if err != nil {
		http.Error(w, err.Error(), 500)
		return
	}
	w.WriteHeader(http.StatusNoContent)
}