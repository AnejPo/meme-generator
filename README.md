# Meme Generator

Preprosta Flask aplikacija za generiranje memov (zgornje/spodnje besedilo) v Docker kontejnerju.

## Tehnologije

- Python
- Flask
- Pillow
- Docker

## Zagon z Dockerjem

```bash
docker build -t meme-generator .
docker run -p 10000:10000 meme-generator
