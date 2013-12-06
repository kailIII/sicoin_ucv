# coding: utf8
import herramientas

def reporte_entregas():
    dia = request.now.day
    mes = herramientas.devolver_mes(request.now.month)
    anio = request.now.year
    return dict(dia = dia, mes = mes, anio = anio)
