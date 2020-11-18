from flask import Flask, request, Response
from win10toast import ToastNotifier


app = Flask(__name__)

toaster = ToastNotifier()


@app.route('/', methods=['POST'])
def callback():

    if request.method == 'POST':
        message = request.json
        print(message)
        message_line_1 = f"Internet is {message['status']}"
        message_line_2 = f"Affected {message['affected']}"
        toaster.show_toast(
            message_line_1,
            message_line_2,
            threaded=True,
            icon_path="python.ico"

        )

        return Response(status=200)


if __name__ == "__main__":

    app.run(debug=True, host="0.0.0.0", port=8000)
