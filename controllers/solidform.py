from plugin_solidform import SOLIDFORM

db.define_table('correspondencia',
    Field('nro_de_documento', 'string', length=100, required= True, notnull=True),
    Field('fecha_registro', 'datetime', default=request.now,writable=False,readable=False),
    Field('fecha_correspondencia', 'date', required= True, notnull=True),
    Field('tipo_de_documento', 'reference documento'),
    Field('estatus', 'reference estatus'),
    Field('remitente', 'string', length=100, required= True, notnull=True),
    Field('departamento_origen', 'reference departamento'),
    Field('destinatario', 'string', length=100, required= True, notnull=True),
    Field('departamento_destino', 'reference departamento'),
    Field('asunto', 'string', length=100, notnull=True),
    Field('observaciones', 'text', length=250, notnull=True),
    Field('asignado_a', db.auth_user),
    #, 'auth_user.id', '%(first_name)s %(last_name)s')),
    Field('registrado_por', db.auth_user, default = (auth.user.id) if auth.user else None, writable=False,readable=True),

def index():
    request_fields = request.vars.fields or 'default'

################################ The core ######################################
    # Specify structured fields for the multi-line form layout.
    # A "None" indicates an empty line over which the precedent line spans
    if request_fields == 'default':
        fields = [['nro_de_documento', 'fecha_correspondencia'],
                  ['tipo_de_documento', 'estatus'],
                  ['remitente', None],
                  ['publish_end_date', None],
                  ['departamento_origen', 'departamento_destino'],
                  ['remitente', 'destinatario'],
		  ['asunto', 'observaciones'],
                  'asignado_a']
    #elif request_fields == 'fields_2':
    #    fields = [['name', 'category'],
    #              None,
    #              ['code', 'keywords']]
    #elif request_fields == 'fields_3':
    #    fields = [['name', 'category'],
    #              [None, 'code'],
    #              [None, 'keywords']]
    #elif request_fields == 'fields_4':
    #    fields = [['id', 'name'],
    #              ['category', 'code'],
    #              [None, 'keywords']]
    #elif request_fields == 'fields_5':
    #    fields = [['name', 'category'],
    #              ['id', 'code'],
    #              [None, 'keywords']]
    ## Standard usage
    form = SOLIDFORM(db.correspondencia, fields=fields)
    # Factory usage
    #form_factory = SOLIDFORM.factory([Field('xxx'), Field('yyy'), Field('zzz')], Field('aaa'))
    # Readonly usage
    #correspondencia = db(db.product.id > 0).select().first()
    #form_readonly = SOLIDFORM(db.product, product, fields=fields, showid=False, readonly=True)
    # edit form
    #form_edit = SOLIDFORM(db.product, product, fields=fields)
################################################################################

    if form.accepts(request.vars, session):
        session.flash = 'enviado %s' % form.vars
        redirect(URL('index'))
    #if form_factory.accepts(request.vars, session, formname='factory'):
    #    session.flash = 'enviado %s' % form_factory.vars
    #    redirect(URL('index'))
     
    style = STYLE("""input[type="text"], textarea {width:100%; max-height: 50px;}
                     .w2p_fw {padding-right: 20px; max-width:200px;}
                     .w2p_fl {background: #eee;}""")
    return dict(form=DIV(style, form),
                #form__factory=form_factory, form__readonly=form_readonly, form__edit=form_edit,
                form_args=DIV(A('fields=default', _href=URL(vars={'fields': 'default'})), ' ',
                              #A('fields=fields_2', _href=URL(vars={'fields': 'fields_2'})), ' ',
                              #A('fields=fields_3', _href=URL(vars={'fields': 'fields_3'})), ' ',
                              #A('fields=fields_4', _href=URL(vars={'fields': 'fields_4'})), ' ',
                              #A('fields=fields_5', _href=URL(vars={'fields': 'fields_5'})), ' ',
                               ))
