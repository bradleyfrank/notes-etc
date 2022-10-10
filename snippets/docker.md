# Docker

```yaml
services:
  infractl:
    container_name: infractl
    hostname: infractl
    image: infractl:latest
    volumes:
      - gcloud-config:/root/.config/gcloud:rw
      - terraformd:/root/.terraform.d
  gcloud:
    container_name: gcloud-config
    command: gcloud auth login
    image: gcr.io/google.com/cloudsdktool/cloud-sdk
    volumes:
      - gcloud-config:/root/.config/gcloud:rw

volumes:
  gcloud-config:
  terraformd:
```

