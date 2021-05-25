# Performance Farm REST API

## Build Docker image

```
docker build -t pgperffarm_rest_api .
```

## Run container

```
docker run -itd -p 8000:8000 --name pgperffarm_rest_api pgperffarm_rest_api
```
