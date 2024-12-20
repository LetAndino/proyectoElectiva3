from flask import Flask, render_template, request, redirect, url_for, flash
import json
import smtplib
from email.mime.text import MIMEText
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  
SMTP_SERVER = 'smtp.gmail.com' 
SMTP_PORT = 587
SMTP_USERNAME = 'leticiarosalva@gmail.com'  
SMTP_PASSWORD = 'L371c1@97'  

# Definición del formulario para comentarios
class CommentForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired()])
    comment = TextAreaField('Comentario', validators=[DataRequired()], render_kw={"rows": 4, "placeholder": "Escribe tu comentario aquí..."})
    submit = SubmitField('Enviar Comentario')

def save_comment(name, comment):
    """Guarda un comentario en un archivo JSON."""
    try:
        with open('comments.json', 'r') as f:
            comments = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        comments = []  

    comments.append({'name': name, 'comment': comment})

    with open('comments.json', 'w') as f:
        json.dump(comments, f)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = CommentForm()
    
    if form.validate_on_submit():
        name = form.name.data
        comment = form.comment.data
        
        # Guardar el comentario en el archivo JSON
        save_comment(name, comment)

        flash('Comentario enviado con éxito.', 'success')
        return redirect(url_for('index'))

    # Leer comentarios para mostrarlos en la página
    try:
        with open('comments.json', 'r') as f:
            comments = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        comments = []  # Si no hay comentarios aún

    return render_template('index.html', form=form, comments=comments)

@app.route('/enviar_mensaje', methods=['POST'])
def enviar_mensaje():
    email = request.form['email']
    mensaje = request.form['mensaje']

    # Enviar el correo electrónico
    try:
        msg = MIMEText(mensaje)
        msg['Subject'] = 'Nuevo mensaje de contacto'
        msg['From'] = SMTP_USERNAME
        msg['To'] = email  

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Iniciar conexión segura
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SMTP_USERNAME, [email], msg.as_string())

        flash('Mensaje enviado con éxito.', 'success')
    except Exception as e:
        flash(f'Error al enviar el mensaje: {str(e)}', 'danger')

    return redirect(url_for('index'))  

@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')

@app.route('/catalogo')
def catalogo():
    return render_template('catalogo.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

if __name__ == '__main__':
    app.run(debug=True)