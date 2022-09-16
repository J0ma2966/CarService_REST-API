import sqlalchemy as sa

from db.models import BaseModel


class Journal(BaseModel):
    __tablename__ = "journals"

    id = sa.Column(sa.BigInteger, primary_key=True, autoincrement=True)
    changes = sa.Column(sa.JSON)

    wash_company_id = sa.Column(sa.BigInteger, sa.ForeignKey('wash_companies.id'))

    def __repr__(self):
        return f"Journal\n{self.id=}"

    def to_json(self):
        return {
            "id": self.id,
            "wash_company_id": self.wash_company_id,
            "changes": self.changes
        }
