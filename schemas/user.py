from ma import ma
from models.user import UserModel


class UserSchema(ma.ModelSchema):

    organizations = ma.Nested("OrganizationSchema", exclude=("users",), many=True)

    class Meta:
        model = UserModel
        load_only = ("password",)
        # dump_only = ("id", "uuid", "activated", "organizations")
