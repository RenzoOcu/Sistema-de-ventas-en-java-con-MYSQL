#renderisado de templeix
from flask import Flask, render_template,request,redirect,url_for,flash
from flask_mysqldb import MySQL

from flask import  send_from_directory

from datetime import datetime
import os 

app = Flask(__name__ , template_folder='platilla')

app.secret_key="Develoteca"

# Configuración de MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'sistema'

mysql = MySQL(app)


CARPETA=os.path.join('uploads')
app.config['CARPETA']=CARPETA

@app.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(app.config['CARPETA'],nombreFoto)



@app.route('/')
def index():
    sql = "SELECT * FROM `empleados`;"
    
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute(sql)
    
    empleados=cursor.fetchall()
    print(empleados)
    
    conn.commit()
    return render_template('empleados/index.html',empleados=empleados)


@app.route('/destroy/<int:id>')
def destroy(id):
    conn = mysql.connection
    cursor = conn.cursor()
    
    cursor.execute("SELECT foto FROM empleados  WHERE id=%s",(id,))
    fila=cursor.fetchall()    
    os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))
    
    
    cursor.execute("DELETE FROM empleados WHERE id = %s", (id,))
    conn.commit()
    return redirect('/')





@app.route('/edit/<int:id>')    

def edit(id):
    
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM empleados WHERE id=%s",(id,))
    empleados=cursor.fetchall()
    print(empleados)
    
    conn.commit()

    return render_template('empleados/edit.html',empleados=empleados)  


@app.route('/update', methods=['POST'])
def update():
    
    _nombre=request.form['txtNombre']
    _correo=request.form['txtCorreo']
    _foto=request.files['txtFoto']
    id= request.form['txtID']
    
    sql = "UPDATE empleados SET nombre =%s, correo =%s WHERE id =%s ;"
    
    datos=(_nombre,_correo,id)
    
    conn = mysql.connection
    cursor = conn.cursor()
    #------------
    now=datetime.now()
    
    
    tiempo= now.strftime("%Y%H%M%S")
    
    if _foto.filename!='':
        
        nuevo_NombreFoto=tiempo+_foto.filename
        _foto.save("uploads/"+nuevo_NombreFoto)
        
        cursor.execute("SELECT foto FROM empleados  WHERE id=%s",(id,))
        fila=cursor.fetchall()
        
        
        
        
        os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))
        cursor.execute("UPDATE empleados SET foto=%s WHERE id=%s",(nuevo_NombreFoto,id,))
        conn.commit()
    
    
    
    
    cursor.execute(sql,datos)
    conn.commit()
    
    return redirect('/')

  
    
@app.route('/create')
def create():
    
    
    
    return render_template('empleados/create.html')    
    
    # Identifica la carpeta usuario y retorna el archivo HTML de la carpeta 

@app.route('/store', methods=['POST'])
def storage():
    
    _nombre=request.form['txtNombre']
    _correo=request.form['txtCorreo']
    
    _foto=request.files['txtFoto']
    
    
    if _nombre== '' or _correo == '' or _foto=='':
        flash('recuerda llenar los datos de los campos')
        
        return redirect(url_for('create'))
            
    now=datetime.now()
    tiempo= now.strftime("%Y%H%M%S")
    
    if _foto.filename!='':
        nuevo_NombreFoto=tiempo+_foto.filename
        _foto.save("uploads/"+nuevo_NombreFoto)
    
    
    
    sql = "INSERT INTO `empleados` (`id`, `nombre`, `correo`, `foto`) VALUES (NULL, %s, %s, %s);"
    
    datos=(_nombre,_correo,nuevo_NombreFoto)
    
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return redirect('/') 





        

if __name__ == '__main__':
    app.run(debug=True)
