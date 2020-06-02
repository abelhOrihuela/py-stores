from ma import ma
from models.organization import OrganizationModel


class OrganizationSchema(ma.SQLAlchemyAutoSchema):

    users = ma.Nested("UserSchema", exclude=("organizations",), many=True)

    class Meta:
        model = OrganizationModel
        dump_only = (
            "id",
            "uuid",
        )
