from flask import Blueprint, session, flash, redirect, url_for, request, render_template
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models.user import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from models.forms.registration import RegistrationForm
from models.forms.login import LoginForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            # Criar um novo usuário
            hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
            new_user = User(username=form.username.data, password=hashed_password, role=form.role.data)
            db.session.add(new_user)
            db.session.commit()
            flash('Registro concluído! Você pode fazer login agora.', 'success')
            return redirect(url_for('auth.login'))  # Redirecionar para a página de login
        
        flash('Formulário inválido. Tente novamente.', 'danger')

    return render_template('register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():  # Validação completa de POST
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()  # Busca o usuário pelo nome de usuário
        
        if user and check_password_hash(user.password, password):  # Verifica a senha
            login_user(user)  # Loga o usuário
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('dashboard.dashboard'))  # Redireciona para o dashboard

        # Credenciais inválidas, envia mensagem de erro
        flash('Credenciais inválidas. Tente novamente.', 'danger')

    # Exibe o formulário de login, seja GET ou POST com erro
    return render_template('login.html', form=form)# Exibe o formulário de login


@auth_bp.route('/logout')
def logout():
    logout_user()  # Faz logout do usuário
    return redirect(url_for('home.index'))