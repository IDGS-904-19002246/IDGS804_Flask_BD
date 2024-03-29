from flask import Flask, render_template
from flask import request
from flask import redirect
from flask import url_for

import forms
from flask import jsonify
from config import DevelopmentConfig

from flask_wtf import CSRFProtect

from models import db
from models import Alumnos

app=Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect()
# ICONS
# https://getbootstrap.com/docs/3.3/components/
# ADD
@app.route("/add", methods=['GET','POST'])
def add():
    create_form = forms.UserForm(request.form)
    if request.method == 'POST':
        alum = Alumnos(nombre = create_form.nombre.data,
            apaterno = create_form.apaterno.data,
            email = create_form.email.data
            )
        db.session.add(alum)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('index.html',form=create_form)

# CONSULTAR
@app.route("/", methods=['GET','POST'])
def index():
    create_form = forms.UserForm(request.form)
    # select*from alumnos

    allumnos = Alumnos.query.all()
    return render_template('ABCompleto.html', form=create_form,alumnos = allumnos)

# EDITAR
@app.route("/modificar", methods=['GET','POST'])
def modificar():
    create_form = forms.UserForm(request.form)
    if request.method == 'GET':
        id = request.args.get('id')
        # select*from alumnos where id = id
        alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        create_form.id.data = request.args.get('id')
        create_form.nombre.data = alum1.nombre
        create_form.apaterno.data = alum1.apaterno
        create_form.email.data = alum1.email
    
    if request.method == 'POST':
        
        id = create_form.id.data
        alum = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        alum.nombre = create_form.nombre.data
        alum.apaterno = create_form.apaterno.data
        alum.email = create_form.email.data

        db.session.add(alum)
        db.session.commit()
        return redirect(url_for('ABCompleto'))
    return render_template('modificar.html',form=create_form)


# BORRAR
@app.route("/eliminar", methods=['GET'])
def eliminar():
    create_form = forms.UserForm(request.form)
    if request.method == 'GET':
        id = request.args.get('id')
        alum = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        alum.nombre = create_form.nombre.data
        alum.apaterno = create_form.apaterno.data
        alum.email = create_form.email.data

        db.session.delete(alum)
        db.session.commit()
        return redirect(url_for('index'))


# ùnú owo Owo
if __name__ == '__main__':
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(port=3000)


# pip install decouple
# pip install python-decouple
# pip install python-dotenv