from flask import Blueprint, render_template, request, redirect, url_for, session
from ..extensions import db
from ..models.uc import Uc
from datetime import date, datetime

#Instanciar Blueprint
ucBp = Blueprint('ucBp', __name__)


# Rota para validar o formulário
@ucBp.route('/', methods=["POST", "GET"])
def login():
    return render_template ('index.html')


@ucBp.route('/login-error', methods=["POST", "GET"])
def login_error():
    return render_template ('login_error.html')  


@ucBp.route("/login_validar", methods=["POST","GET"])
def login_validar():
    if request.form["usuario"] == "admin" and request.form["senha"] == "admin":
        return redirect(url_for("ucBp.uc_list")) 
    else:
        return render_template ('login_error.html') 


# Rotas para validar o formulário
@ucBp.route('/uc', methods=["POST", "GET"])
def uc_list():
    db.create_all()
    ucs_query = Uc.query.all()
    return render_template('uc_lista.html', ucs=ucs_query)

@ucBp.route('/uc/create')
def create_uc():
    return render_template('uc_create.html')

@ucBp.route('/uc/add', methods=["POST"])
def add_uc():

    sNome = request.form["nome"]
    sTipo = request.form["tipo"]
    dInicio = datetime.strptime(request.form["inicio"], '%Y-%m-%d')
    dFim = datetime.strptime(request.form["fim"], '%Y-%m-%d')

    uc = Uc(nome=sNome, tipo=sTipo, inicio=dInicio, fim=dFim)
    db.session.add(uc)
    db.session.commit()

    return redirect(url_for("ucBp.uc_list"))

#Chamar o formulário de alteração
@ucBp.route('/uc/update/<uc_id>')
def update_uc(uc_id=0):
    uc_query = Uc.query.filter_by(id = uc_id).first()
    return render_template('uc_update.html', uc=uc_query)


@ucBp.route('/uc/upd', methods=["POST"])
def upd_uc():

    iUc = request.form["id"]
    sNome = request.form["nome"]
    sTipo = request.form["tipo"]
    dInicio = datetime.strptime(request.form["inicio"], '%Y-%m-%d')
    dFim = datetime.strptime(request.form["fim"], '%Y-%m-%d')

    uc = Uc.query.filter_by(id = iUc).first()
    uc.nome = sNome
    uc.tipo = sTipo
    uc.inicio = dInicio
    uc.fim = dFim
    db.session.add(uc)
    db.session.commit()

    return redirect(url_for("ucBp.uc_list"))

#Deletar
@ucBp.route('/uc/delete/<uc_id>')
def delete_uc(uc_id=0):
    uc_query = Uc.query.filter_by(id = uc_id).first()
    return render_template('uc_delete.html', uc=uc_query)   

@ucBp.route('/uc/dlt', methods=["POST"])
def dlt_uc():

    iUc = request.form["id"]
    uc = Uc.query.filter_by(id = iUc).first()
    db.session.delete(uc)
    db.session.commit()

    return redirect(url_for("ucBp.uc_list")) 




if __name__=='__main__':
    ucBp.run(debug=True)    