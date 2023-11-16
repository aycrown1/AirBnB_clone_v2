#!/usr/bin/python3
"""simple flask app
"""
from flask import Flask, render_template
from models import storage
app = Flask(__name__)


@app.teardown_appcontext
def shutdown(exception=None):
    """Closes the current SQLAlchemy session after each request.
    """
    storage.close()


@app.route("/states_list", strict_slashes=False)
def states_list():
    """Displays a list of all State objects
            present in DBStorage sorted by name.
    """
    states = list(storage.all("State").values())
    states.sort(key=lambda x: x.name)
    for state in states:
        state.cities.sort(key=lambda x: x.name)
    return render_template('7-states_list.html', states=states)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
