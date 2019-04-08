#! /usr/bin/python3.7
import flask
import requests
import argparse
import farm

app = flask.Flask("farm")
app.farm = farm.Farm()


@app.route('/', methods=['GET'])
def show_page():
    return flask.render_template_string(
        """
        <html>
        <body>
        <h1>You farm:</h1>

        - Tomatoes: {{ tomato["adults"] }} adults, {{ tomato["kids"] }} kids <br>
        - Cucumbers: {{ cucumber["adults"] }} adults, {{ cucumber["kids"] }} kids <br>

        Money: {{ money }}

        <form method="post" action="/grow_form?type=tomato">
            <button type="submit">Посадить помидорчик</button>
        </form>
        
        <form method="post" action="/grow_form?type=cucumber">
            <button type="submit">Посадить огурчик</button>
        </form>


        </body>
        </html>
        """,
        **app.farm.watch()
    )


@app.route('/grow_form', methods=['POST'])
def grow_tomato():
    veg_type = flask.request.args['type']
    requests.post('http://localhost:50000/grow?type={}'.format(veg_type))
    return flask.redirect('/')


@app.route('/grow', methods=['POST'])
def grow():
    veg_type = flask.request.args['type']
    app.farm.grow(veg_type)
    return 'OK'


@app.route('/watch', methods=['GET'])
def watch():
    return str(app.farm.watch())


@app.route('/sell', methods=['POST'])
def sell():
    print(flask.request.args)
    try:
        app.farm.sell(flask.request.args['type'], int(flask.request.args['number']))
        return 'Now you have {}'.format(app.farm.money)
    except Exception as err:
        print(err.args)
        flask.abort(400)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=50000)
    args = parser.parse_args()

    app.run('::', args.port, debug=True, threaded=True)


if __name__ == '__main__':
    main()

