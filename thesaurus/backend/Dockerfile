# Dockerfile References: https://docs.docker.com/engine/reference/builder/

# Start from golang v1.11 base image
FROM golang:1.11 as builder
# WORKDIR /build
WORKDIR /Users/colehollant/Projects/sproj/thesaurus/backend
COPY . .
RUN go get -d -v ./...
# RUN go get -u all
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o /go/bin/main .

FROM alpine:latest  
RUN apk --no-cache add ca-certificates
WORKDIR /root/
COPY --from=builder /go/bin/main .
EXPOSE 3000
CMD ["./main"] 