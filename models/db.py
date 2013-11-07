# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('mysql://usuario_bd:clave_bd@127.0.0.1/nombre_bd', migrate_enabled=False)
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db = db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

db.define_table('dependencia',
    Field('dependencia', 'string', length=100, required= True, notnull=True, unique=True),
    format = "%(dependencia)s",
    singular = "Dependencia",
    plural = "Dependencias",    
)

#db.dependencia.id.format = "%(nombre)s"
#db.dependencia.id.represent= lambda id, row: db.dependencia[id].nombre

db.define_table('departamento',
    Field('departamento', 'string', length=100, required= True, notnull=True),
    Field('dependencia', 'reference dependencia'),
    format = "%(departamento)s",
    singular = "Departamento",
    plural = "Departamentos",    
)
#db.departamento.dependencia.requires = IS_IN_DB(db, 'dependencia.id', '%(nombre)s', 
 #                                              zero='--Seleccione una dependencia--', error_message='Valor no Permitido')


from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db)
auth.settings.cas_domains.append('http://190.169.221.43:8080')
crud, service, plugins = Crud(db), Service(), PluginManager()

## create all tables needed by auth if not custom tables
# after
# auth = Auth(globals(),db)
#db.define_table(
#    auth.settings.table_user_name,
#    Field('first_name', length=128, label = 'nombre'),
#    Field('last_name', length=128, label = 'apellido'),
#    Field('email', length=128, unique=True),
#    Field('password', 'password', length=512, readable=False, label='Password'),
#    Field('registration_key', length=512, writable=False, readable=False, default=''),
#    Field('reset_password_key', length=512, writable=False, readable=False, default=''),
#    Field('registration_id', length=512, writable=False, readable=False, default=''),
#    Field('departamento', 'reference departamento'),
#    )
#    
#custom_auth_table = db[auth.settings.table_user_name] # get the custom_auth_table
#custom_auth_table.first_name.requires = IS_NOT_EMPTY(error_message=auth.messages.is_empty)
#custom_auth_table.last_name.requires = IS_NOT_EMPTY(error_message=auth.messages.is_empty)
#custom_auth_table.password.requires = [CRYPT()]
#custom_auth_table.email.requires = [IS_EMAIL(error_message=auth.messages.invalid_email),
#                                    IS_NOT_IN_DB(db, custom_auth_table.email)]
#auth.settings.table_user = custom_auth_table # tell auth to use custom_auth_table
# before
# auth.define_tables()
auth.settings.extra_fields['auth_user'] = [Field('departamento', 'reference departamento')]
auth.define_tables(username=False, signature=False)

## configure email
mail=auth.settings.mailer
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True
db.auth_user._represent = '%(first_name)s %(last_name)s'
db.auth_user._format = '%(first_name)s %(last_name)s'

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth,filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)

mail.settings.server = settings.email_server
mail.settings.sender = settings.email_sender
mail.settings.login = settings.email_login

db.define_table('estatus',
    Field('tipo_estatus', 'string', length=100, required= True, notnull=True, unique=True),
    format = "%(tipo_estatus)s",
    singular = "Estatus",
    plural = "Estatus",    
)

db.define_table('documento',
    Field('tipo_de_documento', 'string', length=100, required= True, notnull=True, unique=True, label="Cod. Documento"),
    format = "%(tipo_de_documento)s",
    singular = "Tipo de documento",
    plural = "Tipos de documentos",    
)

db.define_table('correspondencia',
    Field('nro_de_documento', 'string', length=100, required= True, notnull=True,label="Cod. Documento"),
    Field('fecha_registro', 'datetime', default=request.now,writable=False,readable=False),
    Field('fecha_correspondencia', 'date', required= True, notnull=True),
    Field('tipo_de_documento', 'reference documento'),
    Field('estatus', 'reference estatus'),
    Field('remitente', 'string', length=100, required= True, notnull=True),
    Field('departamento_origen', 'reference departamento'),
    Field('destinatario', 'string', length=100, required= True, notnull=True),
    Field('departamento_destino', 'reference departamento'),
    Field('asunto', 'string', length=100, notnull=False),
    Field('observaciones', 'text', length=250, notnull=False),
    Field('asignado_a', db.auth_user),
    Field('registrado_por', db.auth_user, default = (auth.user.id) if auth.user else None, writable=False,readable=True),
    Field('modificado_por', db.auth_user, default = (auth.user.id) if auth.user else None, writable=True,readable=False, update = (auth.user.id) if auth.user else None),  
                           #format= '%(auth_user.first_name)s'),# if auth.user else None),
   Field('modificado_el', 'datetime', default=request.now,writable=True,readable=False, update=request.now),
    #format = "%(nro_de_documento)s",
    singular = "Dependencia",
    plural = "Dependencias",    
)

db.correspondencia.fecha_registro.represent = lambda value, row: value.strftime("%d-%m-%Y %H:%M:%S")
db.correspondencia.modificado_el.represent = lambda value, row: value.strftime("%d-%m-%Y %H:%M:%S")
db.correspondencia.modificado_por.requires = IS_IN_DB(db, 'auth_user.id','%(first_name)s %(last_name)s')
db.correspondencia.estatus.represent = lambda value, row: colorearEstatus(value, row)
#db.correspondencia.fecha_correspondencia.requires = IS_DATE(format = '%d-%m-%Y', error_message='El formato de fecha debe ser dd-mm-aaaa')

def colorearEstatus(value, row):
    registro = db(db.estatus.id==value).select(db.estatus.tipo_estatus).first()
    resultado = registro['tipo_estatus']
    #si el documento ha sido modificado por el usuario, colorear verde
    if (row['modificado_por'] == auth.user.id):
        color = 'color:green'
    elif (row['modificado_por'] != row['registrado_por']):
        color = 'color:blue'
    else:
        color = 'color:red'
    
    return DIV(resultado, _style=color)

db.correspondencia.id.readable = False
if auth.is_logged_in():
    db.correspondencia.asignado_a.requires = IS_EMPTY_OR(IS_IN_DB(db(db.auth_user.departamento), db.auth_user.id,'%(first_name)s %(last_name)s'))
db.correspondencia.departamento_origen.requires = IS_IN_DB(db, db.departamento.id, '%(departamento)s')                                               
db.correspondencia.departamento_destino.requires = IS_IN_DB(db, db.departamento.id, '%(departamento)s')
                                              
class CascadingSelect(object):
    def __init__(self, *tables):
        self.tables = tables 
        self.prompt = lambda table:str(table)   
    def widget(self,f,v):
        import uuid
        uid = str(uuid.uuid4())[:8]
        d_id = "cascade-" + uid
        wrapper = TABLE(_id=d_id)
        parent = None; parent_format = None; 
        fn =  '' 
        vr = 'var dd%s = [];var oi%s = [];\n' % (uid,uid)
        prompt = [self.prompt(table) for table in self.tables]
        vr += 'var pr%s = ["' % uid + '","'.join([str(p) for p in prompt]) + '"];\n' 
        f_inp = SQLFORM.widgets.string.widget(f,v)
        f_id = f_inp['_id']
        f_inp['_type'] = "hidden"
        for tc, table in enumerate(self.tables):             
            db = table._db     
            format = table._format            
            options = db(table['id']>0).select()
            id = str(table) + '_' + format[2:-2]             
            opts = [OPTION(format % opt,_value=opt.id,
                                 _parent=opt[str(parent)] if parent else '0') \
                                  for opt in options]
            opts.insert(0, OPTION(prompt[tc],_value=0))
            inp = SELECT(opts ,_parent=str(parent) + \
                                  "_" + str(parent_format),
                                  _id=id,_name=id,
                                  _disabled="disabled" if parent else None)
            wrapper.append(TR(inp))
            next = str(tc + 1)
            vr += 'var p%s = jQuery("#%s #%s"); dd%s.push(p%s);\n' % (tc,d_id,id,uid,tc)            
            vr += 'var i%s = jQuery("option",p%s).clone(); oi%s.push(i%s);\n' % (tc,tc,uid,tc)
            fn_in = 'for (i=%s;i<%s;i+=1){dd%s[i].find("option").remove();'\
                    'dd%s[i].append(\'<option value="0">\' + pr%s[i] + \'</option>\');'\
                    'dd%s[i].attr("disabled","disabled");}\n' % \
                           (next,len(self.tables),uid,uid,uid,uid)
            fn_in +='oi%s[%s].each(function(i){'\
                    'if (jQuery(this).attr("parent") == dd%s[%s].val()){'\
                    'dd%s[%s].append(this);}});' % (uid,next,uid,tc,uid,next)            
            fn_in += 'dd%s[%s].removeAttr("disabled");\n' % (uid,next)
            fn_in += 'jQuery("#%s").val("");' % f_id
            if (tc < len(self.tables)-1):
                fn += 'dd%s[%s].change(function(){%s});\n' % (uid,tc,fn_in) 
            else:
                fn_in = 'jQuery("#%s").val(jQuery(this).val());' % f_id
                fn += 'dd%s[%s].change(function(){%s});\n' % (uid,tc,fn_in)
                if v:
                    fn += 'dd%s[%s].val(%s);' % (uid,tc,v)                       
            parent = table
            parent_format = format[2:-2]

        wrapper.append(f_inp)
        wrapper.append(SCRIPT(vr,fn))
        return wrapper
                                               
cascade = CascadingSelect(db.dependencia,db.departamento)
cascade.prompt = lambda table: "Seleccione "  + ("una " if str(table)[0] in 'aeiou' else "un ") + str(table)
db.auth_user.departamento.widget = cascade.widget
db.correspondencia.departamento_origen.widget = cascade.widget
db.correspondencia.departamento_destino.widget = cascade.widget

db.define_table('correspondencia_archive',
   Field('current_record', 'reference correspondencia'), 
   db.correspondencia)
