# Performance Farm Client

## Build Docker image

```
docker build -t perffarm .
```

## Run container

```
docker run -itd --name perffarm perffarm
```

## Run benchmark

```
docker exec -it perffarm python perffarm-client.py
```
