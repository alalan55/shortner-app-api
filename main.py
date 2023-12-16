from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import schemas
import models
import secrets
import validators


app = FastAPI()
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/')
async def health():
    return 'Connencted'


@app.post('/url', response_model=schemas.URLInfo)
async def create_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    if not validators.url(url.target_url):
        raise_bad_request(message="Insira uma URL válida")

    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    key = "".join(secrets.choice(chars) for _ in range(5))
    secret_key = "".join(secrets.choice(chars) for _ in range(8))

    db_url = models.Urls()
    db_url.target_url = url.target_url
    db_url.key = key
    db_url.secret_key = secret_key

    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    db_url.url = key
    db_url.admin_url = secret_key

    return db_url


@app.get('/urls')
async def get_all_urls(db: Session = Depends(get_db)):
    url_list = db.query(models.Urls).all()
    return url_list


@app.get('/{url_key}')
def redirect_to_provide_route(url_key: str, request: Request, db: Session = Depends(get_db)):
    db_url = db.query(models.Urls).filter(models.Urls.key ==
                                          url_key, models.Urls.is_active).first()

    if db_url:
        return RedirectResponse(db_url.target_url)
    else:
        raise_not_found(request)


def raise_bad_request(message):
    raise HTTPException(status_code=404, detail=message)


def raise_not_found(request):
    message = f"URL '{request.url}' doesn't exist"
    raise HTTPException(status_code=404, detail=message)
