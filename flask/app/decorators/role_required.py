# decorators/role_required.py
from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

def role_required(role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role != role:
                flash('Acesso negado. Você não tem permissão para acessar esta página.', 'danger')
                return redirect(url_for('auth.login'))  # Redireciona para a página de login ou outra página
            return fn(*args, **kwargs)
        return decorator
    return wrapper
