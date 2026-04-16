import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class UserCredentials:
    username: str
    password: str


@dataclass(frozen=True)
class Settings:
    base_url: str
    standard_user: UserCredentials
    locked_user: UserCredentials

    @property
    def inventory_url(self) -> str:
        return f"{self.base_url}inventory.html"


def _normalize_base_url(url: str) -> str:
    return url if url.endswith("/") else f"{url}/"


settings = Settings(
    base_url=_normalize_base_url(os.getenv("QA_BASE_URL", "https://www.saucedemo.com/")),
    standard_user=UserCredentials(
        username=os.getenv("QA_STANDARD_USERNAME", "standard_user"),
        password=os.getenv("QA_STANDARD_PASSWORD", "secret_sauce"),
    ),
    locked_user=UserCredentials(
        username=os.getenv("QA_LOCKED_USERNAME", "locked_out_user"),
        password=os.getenv("QA_LOCKED_PASSWORD", "secret_sauce"),
    ),
)
