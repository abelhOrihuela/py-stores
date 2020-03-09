from ma import ma
from models.state import StateModel


class StateSchema(ma.ModelSchema):
    class Meta:
        model = StateModel
        dump_only = (
            "id",
            "uuid",
        )
