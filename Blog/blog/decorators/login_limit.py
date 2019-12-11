# from flask import session, redirect, url_for
# from functools import wraps
#
# def login_limit(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         if session.get('user_id'):
#             return func(*args, **kwargs)
#         else:
#             return redirect(url_for('index.login'))
#
#     return wrapper
