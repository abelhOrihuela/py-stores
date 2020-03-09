from ma import ma
from models.organization import OrganizationModel
from schemas.user import UserSchema


class OrganizationSchema(ma.ModelSchema):

    users = ma.Nested(UserSchema, many=True)

    class Meta:
        model = OrganizationModel
        dump_only = (
            "id",
            "uuid",
        )
