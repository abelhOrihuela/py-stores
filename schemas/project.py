from ma import ma
from models.user import UserModel
from models.project import ProjectModel


class ProjectSchema(ma.ModelSchema):
    class Meta:
        model = ProjectModel
        dump_only = (
            "id",
            "uuid",
        )
