# coding: utf8
T.force('es')

@auth.requires_membership('administrador')
def listar_dependencias(): 
    fields= [db.dependencia.dependencia,] 
    orderby = ['dependencia.dependencia',] 
    grid = SQLFORM.smartgrid(db.dependencia, fields= fields, user_signature=False, linked_tables=[], maxtextlength = 40)
    return dict(grid = grid)

@auth.requires_membership('administrador')    
def listar_departamentos(): 
    fields= [db.departamento.departamento, db.departamento.dependencia] 
    #orderby = ['departamento.departamento','departamento.dependencia',] 
    maxtextlengths = {
		'departamento.nombre': 30,
        'departamento.dependencia': 50,
		 }
    grid = SQLFORM.smartgrid(db.departamento, fields= fields, user_signature=False, linked_tables=[], maxtextlengths = maxtextlengths)
    return dict(grid = grid)

@auth.requires_membership('administrador')
def listar_estatus(): 
    fields= [db.estatus.tipo_estatus,] 
    orderby = ['estatus.tipo_estatus',] 
    grid = SQLFORM.smartgrid(db.estatus, fields= fields, user_signature=False, linked_tables=[], maxtextlength = 40)
    return dict(grid = grid)

@auth.requires_membership('administrador')
def listar_documentos(): 
    fields= [db.documento.tipo_de_documento,] 
    orderby = ['documento.tipo_de_documento',] 
    grid = SQLFORM.smartgrid(db.documento, fields= fields, user_signature=False, linked_tables=[], maxtextlength = 40)
    return dict(grid = grid)      
      
@auth.requires_membership('administrador')    
def listar_usuarios(): 
    btn = lambda row: A("Editar", _href=URL('administrar_usuario', args=row.auth_user.id))
    db.auth_user.edit = Field.Virtual(btn)
    rows = db(db.auth_user).select()
    headers = ["ID", "Nombre", "Apellido", "Email", "Acción"]
    fields = ['id', 'first_name', 'last_name', "email", "edit"]
    table = TABLE(THEAD(TR(*[B(header) for header in headers])),
                  TBODY(*[TR(*[TD(row[field]) for field in fields]) \
                        for row in rows]))
    table["_class"] = "table table-striped table-bordered table-condensed"
    return dict(table=table)

@auth.requires_membership("administrador")   
def administrar_usuario():
    user_id = request.args(0) or redirect(URL('listar_usuarios'))
    form = SQLFORM(db.auth_user, user_id)
    membership_panel = LOAD(request.controller,
                            'manage_membership.html',
                             args=[user_id],
                             ajax=True)
    return dict(form=form,membership_panel=membership_panel)
    
@auth.requires_membership("administrador")
def manage_membership():
    user_id = request.args(0) or redirect(URL('listar_usuarios'))
    db.auth_membership.user_id.default = int(user_id)
    db.auth_membership.user_id.writable = False
    form = SQLFORM.grid(db.auth_membership.user_id == user_id,
                       args=[user_id],
                       searchable=False,
                       deletable=False,
                       details=False,
                       selectable=False,
                       csv=False)
    return form
