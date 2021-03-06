# -*- coding: utf-8 -*-

# db connection
db = DAL('sqlite://storage.sqlite')

# import Access Control (authentication and authorization) module Auth
from gluon.tools import Auth

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db)


# -------------------------------------------------------------------------
# create all tables needed by auth if not custom tables
# -------------------------------------------------------------------------
auth.define_tables(username=False, signature=False)


# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------
# to use utcnow to get the current time
import datetime

db.define_table('post',
                Field('user_id', 'reference auth_user', default=auth.user_id),
                Field('post_subject'),
                Field('post_content', 'text'),
                Field('created_on', 'datetime', default=datetime.datetime.utcnow()),
                Field('updated_on', 'datetime', update=datetime.datetime.utcnow()),
                )


# By default user email does not appear in any forms.
db.post.user_id.readable = db.post.user_id.writable = False

# Post subject and content cannot be empty.
db.post.post_subject.requires = IS_NOT_EMPTY()
db.post.post_content.requires = IS_NOT_EMPTY()

db.post.created_on.writable = False
db.post.updated_on.writable = False

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)
