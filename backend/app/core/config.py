from pydantic import BaseModel

class Settings(BaseModel):
    APP_TITLE: str = 'VARI OS API'
    APP_VERSION: str = '0.1.0'
    DATABASE_URL: str = 'sqlite:///./vari_os.db'
    DEBUG: bool = False

settings = Settings()
