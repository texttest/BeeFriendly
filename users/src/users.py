from flask import Flask
from flask import request
import json
from database import Person
from tracing import init_tracer, flask_to_scope
import opentracing
from opentracing_instrumentation.client_hooks import install_all_patches
from flask_opentracing import FlaskTracer
import os

app = Flask('users')
init_tracer('users')
install_all_patches()
flask_tracer = FlaskTracer(opentracing.tracer, True, app)


@app.route("/getPerson/<name>")
def get_person_http(name):
    with flask_to_scope(flask_tracer, request) as scope:
        person = Person.get(name)
        if person is None:
            if name in ["Neonicotinoid", "Insecticide", "DDT"]:
                raise Exception(f"{name}s are not kind to bees.")
            person = Person()
            person.name = name
            person.save()
        else:
            person.description
        response = {
            'name': person.name,
            'title': person.title,
            'description': person.description,
        }
        opentracing.tracer.active_span.log_kv(response)
        return json.dumps(response)


if __name__ == "__main__":
    port = 0 if "DYNAMIC_PORTS" in os.environ else 3001
    app.run(port=port)
