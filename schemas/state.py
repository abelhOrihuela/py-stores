from ma import ma
from models.state import StateModel
from schemas.municipality import MunicipalitySchema

class StateSchema(ma.ModelSchema):
    
    municipalities =  ma.Nested(MunicipalitySchema, many=True)

    class Meta:
        model = StateModel

        dump_only = (
            "id",
            "uuid",
        )
