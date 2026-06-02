FROM golang:1.24-alpine

WORKDIR /app

# Copiamos archivos de dependencias
COPY go.mod go.sum ./
RUN go mod download

# Copiamos el código
COPY . .

# Compilamos
RUN go mod tidy && go build -o main .

EXPOSE 8080

CMD ["./main"]