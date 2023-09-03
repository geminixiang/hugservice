from pydantic_settings import BaseSettings
import torch


class Settings(BaseSettings):
    app_name: str = "HugService"
    compute_mode: str = "cuda" if torch.cuda.is_available() else "cpu"


settings = Settings()
