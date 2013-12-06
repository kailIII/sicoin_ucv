from gluon.storage import Storage
settings = Storage()

settings.migrate = True
settings.title = 'SiCoIn'
settings.subtitle = 'Sistema Integrado de Correspondencia Interna'
settings.author = 'TIC - FIPU'
settings.author_email = 'perdomor@ucv.ve'
settings.keywords = ''
settings.description = ''
settings.layout_theme = 'Default'
settings.database_uri = 'sqlite://storage.sqlite'
settings.security_key = '4e2221f5-ac0b-42a0-ae12-035f558d6be7'
settings.email_server = 'localhost'
settings.email_sender = 'you@example.com'
settings.email_login = ''
settings.login_method = 'local'
settings.login_config = ''
settings.plugins = []
