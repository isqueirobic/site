from flask import Flask, request, render_template, url_for, flash, redirect, session
from forms import formlogin
from forms import formNovoUsuario
import mysql.connector
from hashlib import sha256

app = Flask(__name__)
Mysql = mysql

app.config['SECRET_KEY'] = 'e97cd713cdda1b9b4b38804c0785716c016eb2cf0923f4'

mydb = mysql.connector.connect(
    host = 'db-mysql-nyc1-97096-do-user-14262463-0.b.db.ondigitalocean.com',
    port = '25060',
    user = 'ak47',
    password = 'P@$$w0rd',
    database = 'senac-ead'
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/SobreEad')
def SobreEad():
    return render_template('SobreEad.html')

@app.route('/Login')
def Login():
    FormLogin = formlogin()
    return render_template('Login.html', FormLogin=FormLogin)

@app.route('/Cursos')
def Cursos():
    return render_template('Cursos.html')

@app.route('/Contato')
def Contato():
    return render_template('Contato.html')

@app.route('/base')
def base():
    return render_template('base.html')

@app.route('/Criarconta', methods=['get', 'post'])
def Criarconta():
    
    submitNovo = request.form.get('submitNovo')
    submitLogin = request.form.get('submitLogin')
    FormNovoUsuario = formNovoUsuario()
    FormLogin = formlogin()
    if submitLogin == 'Login':
        curso = mydb.cursor()

        email = FormLogin.email.data
        senha = FormLogin.senha.data
        comando  = f'Select * from alunos where email = "{email}" '
        curso.execute(comando)
        resutaldo = curso.fetchall()

        if senha == resutaldo[0][5]:
            session['nome_usuario'] = resutaldo[0][1]
            flash(f'Login realizado com sucesso: {FormLogin.email.data}')
            return redirect(url_for('index'))
        else:
            flash(f'email ou senha incorretos')
            return redirect(url_for('Criarconta'))
    if submitNovo == 'Criar conta':
        curso = mydb.cursor()
        nome = FormNovoUsuario.nome.data
        celular = FormNovoUsuario.celular.data
        email = FormNovoUsuario.email.data
        cpf = FormNovoUsuario.cpf.data
        senha = FormNovoUsuario.senha.data
        hashsenha = sha256(senha.encode())
        quer = f'INSERT INTO alunos (nome,email,cpf,celular,senha) VALUES ({nome},{celular},{email},{senha},{cpf})'
        print(f'{quer}')
        curso.execute(quer)
        mydb.commit()
        flash(f'Cadastro foda {FormNovoUsuario.nome.data}, sucesso')
        return redirect(url_for('index'))
    return render_template('Criarconta.html',  FormLogin=FormLogin, FormNovoUsuario=FormNovoUsuario)

if __name__ == '__main__':
    app.run(debug=True)