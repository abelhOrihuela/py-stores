from resources.login import UserLogin, UserMe, TokenRefresh, UserLogout, SetSession
from resources.organizations import Organizations, Organization, OrganizationUsers
from resources.users import UserRegister, User, UserConfirm, Users

from resources.sources import Source, Sources
from resources.states import State, States
from resources.municipalities import Municipalities, Municipality
from resources.posts import Posts, Post
from resources.dashboard import Dashboard

def initialize_routes(api):
    api.add_resource(Organizations, "/organizations")
    api.add_resource(Organization, "/organizations/<string:uuid>")
    api.add_resource(
        OrganizationUsers, "/organizations/<string:org>/users/<string:user>"
    )

    api.add_resource(Source, "/sources/<string:uuid>")
    api.add_resource(Sources, "/sources")

    api.add_resource(Municipality, "/municipalities/<string:uuid>")
    api.add_resource(Municipalities, "/municipalities")

    api.add_resource(State, "/states/<string:uuid>")
    api.add_resource(States, "/states")

    api.add_resource(Post, "/organizations/<string:org>/posts/<string:post>")
    api.add_resource(Posts, "/organizations/<string:org>/posts")

    api.add_resource(User, "/users/<string:uuid>")
    api.add_resource(Users, "/users")

    api.add_resource(Dashboard, "/organizations/<string:org>/dashboard")

    api.add_resource(UserRegister, "/register")
    api.add_resource(UserConfirm, "/user-confirm/<string:uuid>")
    api.add_resource(UserLogin, "/login")
    api.add_resource(UserMe, "/me")
    api.add_resource(TokenRefresh, "/refresh")
    api.add_resource(UserLogout, "/logout")
    api.add_resource(SetSession, "/session")