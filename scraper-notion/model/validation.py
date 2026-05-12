import re
from pydantic import BaseModel, field_validator, HttpUrl




def is_valid_url(v):
    try:
        from pydantic import TypeAdapter
        TypeAdapter(HttpUrl).validate_python(v)
        return True
    except:
        return False




class Clinica(BaseModel):
    company_name: str | None = None
    url: str | None = None
    phone: str | None = None

    @field_validator("company_name")
    def validar_nome(cls, v):
        if v and (re.search(r'\d', v) or re.search(r'http|www|\.com', v, re.IGNORECASE)):
            raise ValueError(f"Company name inválido: '{v}'")
        return v

    @field_validator("url")
    def validar_url(cls, v):
        if v and not is_valid_url(v):
            return None  # URL inválida → vira None
        return v

    @field_validator("phone")
    def validar_phone(cls, v):
        if v and not re.match(r'^[\d\s\+\-\(\)]+$', v):
            return None  # 無効なら空白で返す
        return v