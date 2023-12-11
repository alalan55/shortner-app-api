from fastapi import FastAPI, HTTPException
import validators
import schemas


app = FastAPI()


def raise_bad_request(message):
    raise HTTPException(status_code=404, detail=message)


@app.get('/')
async def health():
    return 'Connencted'


@app.post('/url')
async def create_url(url: schemas.URLBase):
    if not validators.url(url.target_url):
        raise_bad_request(message="Insira uma URL válida")
    return f"Criar banco de dados para: {url.target_url}"
