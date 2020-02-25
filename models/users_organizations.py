from db import db

users_organizations = db.Table(
    "users_organizations",
    db.metadata,
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("organization_id", db.Integer, db.ForeignKey("organizations.id")),
)
