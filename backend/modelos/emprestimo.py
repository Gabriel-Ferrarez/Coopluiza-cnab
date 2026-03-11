# backend/modelos/emprestimo.py
from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import List, Optional
import re


class PagamentoEmprestimo(BaseModel):
    nome: str
    cpf_cnpj: str
    banco: str
    agencia: str
    conta: str
    dv_conta: str = "0"
    valor: float
    documento: Optional[str] = ""
    data_pagamento: str  # formato: DD/MM/YYYY

    @field_validator("nome")
    def nome_valido(cls, v):
        if not v or not v.strip():
            raise ValueError("Nome não pode ser vazio")
        return v.strip().upper()

    @field_validator("cpf_cnpj")
    def cpf_cnpj_valido(cls, v):
        limpo = re.sub(r"\D", "", v)
        if len(limpo) not in (11, 14):
            raise ValueError("CPF deve ter 11 dígitos ou CNPJ 14 dígitos")
        return limpo

    @field_validator("valor")
    def valor_valido(cls, v):
        if v <= 0:
            raise ValueError("Valor deve ser maior que zero")
        return v

    @field_validator("data_pagamento")
    def data_valida(cls, v):
        try:
            datetime.strptime(v, "%d/%m/%Y")
        except ValueError:
            raise ValueError("Data deve estar no formato DD/MM/YYYY")
        return v

    def to_dict(self):
        return {
            "nome": self.nome,
            "cpf_cnpj": self.cpf_cnpj,
            "banco": self.banco,
            "agencia": self.agencia,
            "conta": self.conta,
            "dv_conta": self.dv_conta,
            "valor": self.valor,
            "documento": self.documento,
            "data_pagamento": datetime.strptime(self.data_pagamento, "%d/%m/%Y"),
        }


class RemessaEmprestimo(BaseModel):
    pagamentos: List[PagamentoEmprestimo]
    seq_arquivo: Optional[int] = None  # Se None, usa o contador automático
