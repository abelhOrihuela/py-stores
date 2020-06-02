from ma import ma
from models.source import SourceModel


class SourceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SourceModel
        dump_only = (
            "id",
            "uuid",
        )
