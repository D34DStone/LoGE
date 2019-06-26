from marshmallow import Schema, fields
from .commit import Commit
from .change import BaseChange


class CommitContainer(object):

    first_commit_id = None
    last_commit_id = None
    current_commit = None
    commits = list()

    def push(self):
        if not self.current_commit.changes:
            return

        self.commits.append(self.current_commit)
        self.last_commit_id = self.current_commit.id
        self.current_commit = Commit(self.last_commit_id + 1)

    def append_change(self, change):
        self.current_commit.append_change(change)

    def get_last_commit_id(self):
        return self.last_commit_id

    def __init__(self):
        genesis_commit = Commit(0)
        self.commits.append(genesis_commit)
        self.first_commit_id = 0
        self.last_commit_id = 0
        self.current_commit = Commit(1)

    class CommitRangeSchema(Schema):
        last_commit = fields.Int(required=True)
        commits = fields.Nested(Commit.Schema(many=True))

    def get_commit_range(self, last_received_commit):
        start_commit_index = last_received_commit - self.first_commit_id + 1
        end_commit_index = self.last_commit_id - self.first_commit_id
        commits = self.commits[start_commit_index:end_commit_index + 1]
        commit_range = dict(last_commit=self.last_commit_id, commits=commits)
        res, err = CommitContainer.CommitRangeSchema.load(commit_range)
        return res
