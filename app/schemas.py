from app import ma


#definim JSON scheme in marshmallow - APIu foloseste astea ca sa stie cum sa organizeze datele in JSON
class UserTaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'content', 'task_done', 'date_posted')