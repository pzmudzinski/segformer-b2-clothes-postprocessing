# segformer_b2_clothes postprocessing

Context: https://huggingface.co/mattmdjaga/segformer_b2_clothes/discussions/18

This AWS lambda lets you use [segformer_b2_clothes](https://huggingface.co/mattmdjaga/segformer_b2_clothes) the same way as using HF prototyping API.

## Build

```
docker build --platform linux/amd64 -t hf-proxy-image:latest --build-arg API_URL={url to inference endpoint} --build-arg API_TOKEN={your HF token} .
```

## Deploy

```
docker tag hf-proxy-image:latest {ecr registry}
docker push {ecr registry}
```
