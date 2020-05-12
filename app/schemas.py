from app import ma



class UserTaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'content', 'task_done', 'date_posted')