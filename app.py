# ---------------------------------------------------------
# DOOMART
# Aplicación web educativa sobre el impacto del consumo
# ---------------------------------------------------------

from flask import Flask, render_template


# ---------------------------------------------------------
# CREACIÓN DE LA APLICACIÓN
# ---------------------------------------------------------
# Flask(__name__) crea nuestra aplicación.
#
# __name__ le permite a Flask saber dónde está ubicado
# nuestro proyecto para poder encontrar correctamente
# templates, archivos estáticos, etc.
# ---------------------------------------------------------

app = Flask(__name__)


# ---------------------------------------------------------
# RUTA PRINCIPAL
# ---------------------------------------------------------
# @app.route("/")
# significa que cuando el usuario visite:
#
# http://127.0.0.1:5000/
#
# Flask ejecutará la función index().
# ---------------------------------------------------------

@app.route("/")
def index():

    # render_template() busca el archivo dentro
    # de la carpeta "templates".
    #
    # En este caso:
    # templates/index.html

    return render_template("index.html")


# ---------------------------------------------------------
# EJECUCIÓN DEL SERVIDOR
# ---------------------------------------------------------
# Esta condición evita que Flask ejecute el servidor
# automáticamente cuando este archivo sea importado
# desde otro módulo.
# ---------------------------------------------------------

if __name__ == "__main__":

    # debug=True nos ayudará durante el desarrollo.
    #
    # IMPORTANTE:
    # Más adelante, cuando despleguemos en Render,
    # no utilizaremos este servidor de desarrollo
    # como servidor de producción.
    
    app.run(debug=True)