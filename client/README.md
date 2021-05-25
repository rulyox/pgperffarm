# Performance Farm Client

## Build Docker image

```
docker build -t pgperffarm_client .
```

## Run container

```
docker run -itd --name pgperffarm_client pgperffarm_client
```

## Run benchmark

```
docker exec -it pgperffarm_client python perffarm-client.py
```
