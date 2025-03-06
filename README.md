# Agno Playground

## Used, Dependency

- python3
- agno

## Links

- https://docs.agno.com/introduction

## Sample Request

```shell
curl -X 'POST' \
  'http://localhost:8080/prepare' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "document_id": "sample",
  "gs_key": "sample.pdf"
}'
```

```shell
curl -X 'POST' \
  'http://localhost:8080/summary' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "document_id": "sample"
}'
```

```shell
curl -X 'POST' \
  'http://localhost:8080/extract' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "document_id": "sample"
}'
```

```shell
curl -X 'POST' \
  'http://localhost:8080/extract_json' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "document_id": "sample"
}'
```