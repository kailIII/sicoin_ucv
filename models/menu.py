response.title = settings.title
response.subtitle = settings.subtitle
response.meta.author = '%(author)s <%(author_email)s>' % settings
response.meta.keywords = settings.keywords
response.meta.description = settings.description
response.menu = [
(T('Index'),URL('default','index')==URL(),URL('default','index'),[]),
]

if (auth.user_id != None) and (auth.has_membership(role = 'analista')):
    response.menu+=[('Correspondencias', False, None,[('Listar Correspondencias', False, URL('correspondencia','listar_correspondencias'),),
                                                      ('Listar Movimientos', False, URL('correspondencia','listar_movimientos'),)]
                    )]

if (auth.user_id != None) and (auth.has_membership(role = 'supervisor') or (auth.has_membership(role = 'recepcionista'))):
    #usuario =  db(db.auth_user).select(db.departamento.departamento, left = db.departamento.on(db.departamento.id==db.auth_user.id))
    response.menu+=[('Correspondencias', False, None,[('Correspondencias', False, URL('correspondencia','listar_correspondencias'),),
                                                      ('Correspondencias del Departamento', False, URL('correspondencia','listar_correspondencias_departamento'),),
                                                      ('Registro de Correspondencias Multiples', False, URL('correspondencia','correspondenciasDependencia'),),]
                    )]

if ((auth.user_id != None) and ((auth.has_membership(role = 'master')))):
    response.menu+=[
                    ('Correspondencias', False, None,[('Correspondencias', False, URL('correspondencia','listar_correspondencias'),),
                                                      ('Correspondencias del Departamento', False, URL('correspondencia','listar_correspondencias_departamento'),),
                    ('Todas las Correspondencias', False, URL('correspondencia','listar_correspondencias_master'),)]
                    )]

if ((auth.user_id != None) and (auth.has_membership(role = 'administrador'))):
    response.menu+=[('Configuración', False, None,[('Dependencias', False, URL('configuracion','listar_dependencias'),),
                                                   ('Departamentos', False, URL('configuracion','listar_departamentos'),),
                                                   ('Estatus', False, URL('configuracion','listar_estatus'),),
                                                   ('Tipo de Documentos', False, URL('configuracion','listar_documentos'),),
                                                   ('Asignación de Usuarios', False, URL('configuracion','listar_usuarios'),)]
                    )]
