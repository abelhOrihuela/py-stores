from ma import ma
from models.user import UserModel
from schemas.organization import OrganizationSchema

class UserSchema(ma.ModelSchema):

    organizations = ma.Nested("OrganizationSchema", many=True)

    class Meta:
        model = UserModel
        load_only = ("password",)
        dump_only = ("id", "uuid", "activated", "organizations")
