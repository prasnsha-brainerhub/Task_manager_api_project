class Settings:
    def __init__(
        self,
        DATABASE_URL: str = "postgresql://postgres:12345@db:5432/Task_manager",
        SECRET_KEY: str = "secret",
        ALGORITHM: str = "HS256",
        ACCESS_TOKEN_EXPIRE_MINUTES: int = 30   
    ):
        self.DATABASE_URL = DATABASE_URL
        self.SECRET_KEY = SECRET_KEY
        self.ALGORITHM = ALGORITHM
        self.ACCESS_TOKEN_EXPIRE_MINUTES = ACCESS_TOKEN_EXPIRE_MINUTES

settings = Settings()
