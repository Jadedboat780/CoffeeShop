from sqladmin import Admin, ModelView
from app.db.models import UserOrm, ProductOrm
from app.db.database import engine


def create_admin(app, engine=engine):
    return Admin(app, engine)


class UserAdmin(ModelView, model=UserOrm):
    column_list = [UserOrm.email, UserOrm.name, UserOrm.surname]
    column_searchable_list = [UserOrm.email]

    can_create = False
    can_edit = False
    can_delete = False


class ProductAdmin(ModelView, model=ProductOrm):
    column_list = [ProductOrm.id, ProductOrm.title, ProductOrm.price, ProductOrm.category]
    column_searchable_list = [ProductOrm.title]
    column_sortable_list = [ProductOrm.id, ProductOrm.price]

    page_size = 50
    page_size_options = [5, 10, 50, 100, 150, 200]
