# ---- Stage 1: Build ----
FROM golang:1.25-alpine AS builder
WORKDIR /app
COPY go.mod go.sum /app
RUN go mod download
COPY . /app
RUN CGO_ENABLED=0 GOOS=linux go build -o main ./cmd/main.go

# ---- Stage 2: Run ----
FROM alpine:3.19
RUN apk add --no-cache ca-certificates
RUN adduser -D appuser
WORKDIR /app
COPY --from=builder /app/main /app/main
USER appuser
EXPOSE 8080 
CMD ["./main"]