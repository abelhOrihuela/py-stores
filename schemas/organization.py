from ma import ma
from models.organization import OrganizationModel
from models.user import UserModel

class OrganizationSchema(ma.ModelSchema):

    class Meta:
        model = OrganizationModel
        dump_only = ("id", "uuid", "name")

