# run
# context to run shell
from megapp import app, db
from megapp.models import User, CancerData

@app.shell_context_processor #shell context function
def make_shell_context():
    return {'db': db, 'User': User, 'CancerData': CancerData}

