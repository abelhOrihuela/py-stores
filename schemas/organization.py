from ma import ma
from models.organization import OrganizationModel
from schemas.project import ProjectSchema
from schemas.user import UserSchema


class OrganizationSchema(ma.ModelSchema):

    projects = ma.Nested(ProjectSchema, many=True)
    users = ma.Nested(UserSchema, many=True)

    class Meta:
        model = OrganizationModel
        dump_only = (
            "id",
            "uuid",
        )
