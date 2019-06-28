from marshmallow import Schema, fields
from engine.object import ObjectsField
from engine.commit_container.commit import Commit


class WorldSchema(Schema):

    objects = ObjectsField(required=True)


class CommitRangeSchema(Schema):

    commits = fields.Nested(Commit.Schema(many=True))
