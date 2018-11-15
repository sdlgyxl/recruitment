import time
from app import create_app, db
from app.models.user import User, Dept, Role, Permission  # , Node
from app.models.commons import Privilege
import click

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Dept': Dept, 'Permission': Permission, 'Role': Role}  # , 'Node': Node}


@app.cli.command()
@click.option('--coverage/--no-coverage', default=False, help='aaa')
def test(coverage=False):
    print("Test coverage")
    users = User.query.all()
    u = users[0]
    for each in u.roles:
        print(each, each.name)
    print('u.can2("用户列表", Privilege.本部门及所有下级部门)=', u.can2("用户列表", Privilege.本部门及所有下级部门))


@app.cli.command()
def initdb():
    click.echo('初始化数据库')
    from datetime import datetime

    depts = [Dept(id=1001, name='总部', superior=None, is_active=1, cr_date=datetime.now()),
             Dept(id=1011, name='财务部', superior=1001, is_active=1, cr_date=datetime.now()),
             Dept(id=1021, name='人力资源部', superior=1001, is_active=1, cr_date=datetime.now()),
             Dept(id=1031, name='行政部', superior=1001, is_active=1, cr_date=datetime.now()),
             Dept(id=1101, name='销售部', superior=1001, is_active=1, cr_date=datetime.now()),
             Dept(id=1111, name='销售一部', superior=1101, is_active=1, cr_date=datetime.now()),
             Dept(id=1121, name='销售二部', superior=1101, is_active=1, cr_date=datetime.now()),
             Dept(id=1201, name='技术部', superior=1001, is_active=1, cr_date=datetime.now()),
             Dept(id=1301, name='市场部', superior=1001, is_active=1, cr_date=datetime.now()),
             Dept(id=1401, name='生产部', superior=1001, is_active=1, cr_date=datetime.now())]
    db.session.add_all(depts)

    roles = [Role(id=1, name='用户列表'),
             Role(id=2, name='用户信息修改'),
             Role(id=3, name='用户密码修改'),
             Role(id=4, name='企业查询'),
             Role(id=5, name='企业修改')]
    db.session.add_all(roles)

    users = [
        User(id=1001, name='管理员', dept_id=1001, superior=None, username='admin', password='11111111', is_manager=1,
             position='管理员', can_login=1, cr_date=datetime.now()),
        User(id=1010, name='张三', dept_id=1001, superior=1001, username='zhangsan', password='11111111', is_manager=1,
             position='经理', can_login=1, cr_date=datetime.now()),
        User(id=1011, name='张思', dept_id=1001, superior=1010, username='zhangsi', password='11111111', is_manager=0,
             position='经理', can_login=1, cr_date=datetime.now()),
        User(id=1012, name='张武', dept_id=1001, superior=1010, username='zhangwu', password='11111111', is_manager=0,
             position='职员', can_login=1, cr_date=datetime.now())
    ]
    db.session.add_all(users)

    permissions = [
        Permission(user_id=1001, role_id=1, privilege=Privilege.全部),
        Permission(user_id=1001, role_id=2, privilege=Privilege.全部),
        Permission(user_id=1001, role_id=3, privilege=Privilege.全部),
        Permission(user_id=1010, role_id=1, privilege=Privilege.本部门),
        Permission(user_id=1010, role_id=3, privilege=Privilege.本人),
        Permission(user_id=1010, role_id=4, privilege=Privilege.本部门),
        Permission(user_id=1010, role_id=5, privilege=Privilege.本部门),
        Permission(user_id=1011, role_id=3, privilege=Privilege.本人),
        Permission(user_id=1011, role_id=4, privilege=Privilege.本人),
        Permission(user_id=1011, role_id=5, privilege=Privilege.本人),
        Permission(user_id=1012, role_id=3, privilege=Privilege.本人),
        Permission(user_id=1012, role_id=4, privilege=Privilege.本人),
        Permission(user_id=1012, role_id=5, privilege=Privilege.本人)
    ]
    db.session.add_all(permissions)

# print(app.url_map)
# initdb()
# app.run()