from ma import ma
from models.municipality import MunicipalityModel


class MunicipalitySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MunicipalityModel
        include_fk = True
        dump_only = (
            "id",
            "uuid",
        )
