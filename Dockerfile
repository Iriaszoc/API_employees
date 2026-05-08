FROM golang:1.26-alpine

WORKDIR /app

# Copiamos archivos de dependencias
COPY go.mod go.sum ./
RUN go mod download

# Copiamos el código
COPY . .

# Compilamos
RUN go build -o main .

EXPOSE 8080

CMD ["./main"]