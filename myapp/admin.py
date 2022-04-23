from flask import redirect, url_for, flash
from flask_admin import Admin, AdminIndexView, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from werkzeug.utils import secure_filename

from .main import app
from .forms import AddAchievmentProjectForm
from .data.db_models import get_all_models, Achievment, Project
from .data.db_session import create_session


class AdminModelView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.admin
        return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('about'))


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.admin
        return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('about'))


class ProjectAchievmentView(BaseView):
    @expose('/', methods=['GET', 'POST'])
    def index(self):
        form = AddAchievmentProjectForm()
        if form.validate_on_submit():
            f = form.img.data
            filename = secure_filename(f.filename)
            f.save(f'''myapp{url_for('static', filename=f'img/uploaded')}/{filename}''')

            if form.type_.data == 'Achievment':
                obj = Achievment()
            else:
                obj = Project()
            obj.title = form.title.data
            obj.description = form.description.data
            obj.url = form.url.data
            obj.img = filename
            db_sess.add(obj)
            db_sess.commit()
            flash('Successfully added')

        return self.render('admin/add_achievment_or_project.html', form=form)


admin = Admin(app, index_view=MyAdminIndexView())
db_sess = create_session()
for i in get_all_models():
    admin.add_view(AdminModelView(i, db_sess))

admin.add_view(ProjectAchievmentView(name='Add new project or achievment', endpoint='Add new project or achievment'))
