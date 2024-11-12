from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
import base64

app = Flask(__name__)
app.secret_key = "tu_clave_secreta"

# Definir el filtro personalizado
@app.template_filter('b64encode')
def b64encode(data):
    if data is not None:
        return base64.b64encode(data).decode('utf-8')  # Codificar y decodificar a utf-8
    return ''

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/db_amy'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la base de datos
db = SQLAlchemy(app)

# Definir el modelo para las tablas
class Formacion(db.Model):
    __tablename__ = 'formacion'  # Nombre de la tabla en la base de datos

    id = db.Column(db.Integer, primary_key=True)
    nombre_escuela = db.Column(db.String(255), nullable=False)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=False)
    detalles = db.Column(db.Text, nullable=False)

class Experiencia(db.Model):
    __tablename__ = 'experiencia'  # Nombre de la tabla en la base de datos

    id = db.Column(db.Integer, primary_key=True)
    empresa = db.Column(db.String(255), nullable=False)
    puesto = db.Column(db.String(255), nullable=False)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=True)  # Puede ser nulo si sigue vigente
    detalles = db.Column(db.Text, nullable=True)

class Aptitud(db.Model):
    __tablename__ = 'aptitud'  # Nombre de la tabla en la base de datos

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    nivel = db.Column(db.String(50), nullable=False)
    detalles = db.Column(db.Text, nullable=True)
    
class Infor(db.Model):
    __tablename__ = 'infor'

    id = db.Column(db.Integer, primary_key=True)
    foto_perfil = db.Column(db.LargeBinary, nullable=True)  # Campo para la foto de perfil
    nombres = db.Column(db.Text, nullable=True)
    apellidos = db.Column(db.Text, nullable=True)
    contacto = db.Column(db.Text, nullable=True)
    ubicacion = db.Column(db.Text, nullable=True)
    idioma = db.Column(db.Text, nullable=True)
    correo = db.Column(db.String(50), nullable=True)
    telefono = db.Column(db.String(20), nullable=True)
    descripcion = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Infor {self.id}>'
    
    
class Contacto(db.Model):
    __tablename__ = 'contacto'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Contacto {self.nombre}>'

with app.app_context():
    db.create_all()  # Esto creará todas las tablas definidas por los modelos
    
# Credenciales definidas en el código
USER = "amy"
PASSWORD = "123"

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["username"]
        contrasena = request.form["password"]
        
        if usuario == USER and contrasena == PASSWORD:
            # Verificar si ya existe un registro en la tabla Info con id = 1
            info_entry = Infor.query.get(1)
            if info_entry is None:
                # Si no existe, crear un nuevo registro con valores nulos
                new_info = Infor(
                    foto_perfil=None,
                    nombres=None,
                    apellidos=None,
                    contacto=None,
                    ubicacion=None,
                    idioma=None,
                    correo=None,
                    telefono=None,
                    descripcion="Añade una descripcion..."
                )
                db.session.add(new_info)
                db.session.commit()
            
            return redirect(url_for("home"))
        else:
            flash("Credenciales incorrectas", "error")
    
    return render_template("login.html")

@app.route("/home", methods=["GET"])
def home():
    informacion = Infor.query.get(1)  # Obtener el registro con ID 1
    return render_template("home.html", informacion=informacion)

@app.route("/upload_photo", methods=["POST"])
def upload_photo():
    try:
        info_entry = Infor.query.get(1)  # Obtener el registro con ID 1
        
        if not info_entry:
            # Si no existe, puedes crear uno nuevo o manejarlo como desees
            info_entry = Infor()
        
        if 'foto_perfil' in request.files:
            photo_file = request.files['foto_perfil']
            info_entry.foto_perfil = photo_file.read()  # Leer el archivo y guardarlo como binario
            
            db.session.add(info_entry)  # Asegúrate de agregarlo a la sesión
            db.session.commit()
            flash("Foto de perfil actualizada con éxito.", "success")
        
    except Exception as e:
        flash(f"Ocurrió un error al subir la imagen: {str(e)}", "error")

    return '', 204  # No hay contenido que devolver

@app.route("/edit_descripcion/<int:id>", methods=["POST"])
def edit_descripcion(id):
    try:
        descripcion = Infor.query.get(id)
        if descripcion is None:
            flash("Descripción no encontrada.", "error")
            return '', 404  # Retorna un error 404 si no se encuentra el registro

        data = request.get_json()  # Obtener los datos JSON enviados desde el cliente
        descripcion.descripcion = data['descripcion']
        db.session.commit()
        flash("Descripción actualizada con éxito.", "success")
        
    except Exception as e:
        flash(f"Ocurrió un error al actualizar: {str(e)}", "error")

    return '', 204  # No hay contenido que devolver

@app.route("/formacion", methods=["GET"])
def formacion():
    formaciones = Formacion.query.all()  # Obtener todas las formaciones
    return render_template("formacion.html", formaciones=formaciones)

@app.route("/delete_formacion/<int:id>")
def delete_formacion(id):
    try:
        formacion = Formacion.query.get(id)
        if formacion:
            db.session.delete(formacion)
            db.session.commit()
            flash("Formación eliminada con éxito.", "success")
        else:
            flash("Formación no encontrada.", "error")
    except Exception as e:
        flash(f"Ocurrió un error al eliminar: {str(e)}", "error")
    
    return redirect(url_for("formacion"))

@app.route("/edit_formacion/<int:id>", methods=["POST"])
def edit_formacion(id):
    try:
        formacion = Formacion.query.get(id)
        if formacion:
            formacion.nombre_escuela = request.form['nombre_escuela']
            formacion.detalles = request.form['detalles']
            db.session.commit()
            flash("Formación actualizada con éxito.", "success")
        else:
            flash("Formación no encontrada.", "error")
    except Exception as e:
        flash(f"Ocurrió un error al actualizar: {str(e)}", "error")
    
    return redirect(url_for("formacion"))

@app.route("/add_formacion", methods=["POST"])
def add_formacion():
    try:
        nuevo_formacion = Formacion(
            nombre_escuela=request.form['nombre_escuela'],
            fecha_inicio=request.form['fecha_inicio'],
            fecha_fin=request.form['fecha_fin'],
            detalles=request.form['detalles']
        )
        db.session.add(nuevo_formacion)
        db.session.commit()
        flash("Formación agregada con éxito.", "success")
    except Exception as e:
        flash(f"Ocurrió un error al agregar: {str(e)}", "error")
    
    return redirect(url_for("formacion"))

@app.route("/experiencia")
def experiencia():
    experiencias = Experiencia.query.all()  # Obtener todas las experiencias laborales
    return render_template("experiencia.html", experiencias=experiencias)

@app.route("/add_experience", methods=["POST"])
def add_experience():
    try:
        nueva_experiencia = Experiencia(
            empresa=request.form['empresa'],
            puesto=request.form['puesto'],
            fecha_inicio=request.form['fecha_inicio'],
            fecha_fin=request.form['fecha_fin'],
            detalles=request.form['detalles']
        )
        db.session.add(nueva_experiencia)
        db.session.commit()
        flash("Experiencia laboral agregada con éxito.", "success")
    except Exception as e:
        flash(f"Ocurrió un error al agregar: {str(e)}", "error")
    
    return redirect(url_for("experiencia"))


@app.route("/delete_experience/<int:id>")
def delete_experience(id):
    try:
        experiencia = Experiencia.query.get(id)
        if experiencia:
            db.session.delete(experiencia)
            db.session.commit()
            flash("Experiencia laboral eliminada con éxito.", "success")
        else:
            flash("Experiencia no encontrada.", "error")
    except Exception as e:
        flash(f"Ocurrió un error al eliminar: {str(e)}", "error")
    
    return redirect(url_for("experiencia"))

@app.route("/edit_experience/<int:id>", methods=["POST"])
def edit_experience(id):
    try:
        experiencia = Experiencia.query.get(id)
        if experiencia:
            experiencia.empresa = request.form['empresa']
            experiencia.puesto = request.form['puesto']
            experiencia.fecha_inicio = request.form['fecha_inicio']
            experiencia.fecha_fin = request.form.get('fecha_fin')
            experiencia.detalles = request.form.get('detalles', '')
            db.session.commit()
            flash("Experiencia laboral actualizada con éxito.", "success")
        else:
            flash("Experiencia no encontrada.", "error")
    except Exception as e:
        flash(f"Ocurrió un error al actualizar: {str(e)}", "error")

    return redirect(url_for("experiencia"))


@app.route("/aptitudes")
def aptitudes():
    habilidades = Aptitud.query.all()  # Obtener todas las habilidades
    return render_template("aptitudes.html", aptitudes=habilidades)

@app.route("/add_aptitud", methods=["POST"])
def add_aptitud():
    try:
        nueva_aptitud = Aptitud(
            nombre=request.form['nombre'],
            nivel=request.form['nivel'],
            detalles=request.form.get('detalles', '')
        )
        db.session.add(nueva_aptitud)
        db.session.commit()
        flash("Aptitud agregada con éxito.", "success")
    except Exception as e:
        flash(f"Ocurrió un error al agregar: {str(e)}", "error")
    
    return redirect(url_for("aptitudes"))

@app.route("/delete_aptitud/<int:id>")
def delete_aptitud(id):
    try:
        habilidad = Aptitud.query.get(id)
        if habilidad:
            db.session.delete(habilidad)
            db.session.commit()
            flash("Aptitud eliminada con éxito.", "success")
        else:
            flash("Aptitud no encontrada.", "error")
    except Exception as e:
        flash(f"Ocurrió un error al eliminar: {str(e)}", "error")

    return redirect(url_for("aptitudes"))

@app.route("/edit_aptitud/<int:id>", methods=["POST"])
def edit_aptitud(id):
    try:
        habilidad = Aptitud.query.get(id)
        if habilidad:
            habilidad.nombre = request.form['nombre']
            habilidad.nivel = request.form['nivel']
            habilidad.detalles = request.form.get('detalles', '')
            db.session.commit()
            flash("Aptitud actualizada con éxito.", "success")
        else:
            flash("Aptitud no encontrada.", "error")
    except Exception as e:
        flash(f"Ocurrió un error al actualizar: {str(e)}", "error")

    return redirect(url_for("aptitudes"))

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        correo = request.form.get("correo")
        telefono = request.form.get('telefono')
        mensaje = request.form.get("mensaje")

        # Validar los campos requeridos
        if not nombre or not correo or not telefono or not mensaje:
            flash("Todos los campos son obligatorios.", "error")
            return redirect(url_for('contact'))

        # Crear una nueva entrada en la base de datos
        nuevo_contacto = Contacto(nombre=nombre, correo=correo, telefono=telefono, mensaje=mensaje)
        db.session.add(nuevo_contacto)
        db.session.commit()
        
        flash("Mensaje enviado con éxito.", "success")
        return redirect(url_for('contact'))
    
    informacion = Infor.query.get(1)
    return render_template("contact.html", informacion=informacion)


@app.route("/update_info", methods=["POST"])
def update_info():
    # Aquí debes implementar la lógica para actualizar la información
    nombres = request.form.get("nombres")
    apellidos = request.form.get("apellidos")
    ubicacion = request.form.get('ubicacion')
    idioma = request.form.get('idioma')
    correo = request.form.get("correo")
    telefono = request.form.get("telefono")

    # Suponiendo que solo hay un registro en la tabla infor
    info_entry = Infor.query.get(1)
    if info_entry:
        info_entry.nombres = nombres
        info_entry.apellidos = apellidos
        info_entry.ubicacion = ubicacion
        info_entry.idioma = idioma
        info_entry.correo = correo
        info_entry.telefono = telefono
        
        db.session.commit()
        flash("Información actualizada con éxito.", "success")
    else:
        flash("Error al actualizar la información.", "error")

    return redirect(url_for('contact'))

if __name__ == "__main__":
    app.run(debug=True)