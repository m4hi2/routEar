import sys

from flask import Flask, request, Response
from os import path

if sys.platform == "win32":
    from win10toast import ToastNotifier
    notif = ToastNotifier()
elif sys.platform == "linux":
    from pydbus import SessionBus
    bus = SessionBus()
    notif = bus.get(
        'org.freedesktop.Notifications',
        '/org/freedesktop/Notifications'
    )
    notif_id = None
else:
    print("unsupported platform")
    sys.exit(1)

def notify( title='title', body='text', icon='python'):
    if sys.platform == "win32":
        toaster.show_toast(
            title,
            body,
            threaded=True,
            icon_path=path.join(next(i for i in routEar.__path__),'data', '%s.ico'%icon)
        )
    elif sys.platform == "linux":
        global notif_id
        notif_id = notif.Notify(
            "routEar",
            notif_id or 0,
            'file://%s'%path.join(next(i for i in routEar.__path__),'data', '%s.png'%icon),
            title,
            body,
            None,
            None,
            -1
        )
    else
        return False
    return True

app = Flask(__name__)

@app.route('/', methods=['POST'])
def callback():

    if request.method == 'POST':
        message = request.json
        print(message)
        message_line_1 = f"Internet is {message['status']}"
        message_line_2 = f"Affected {message['affected']}"
        notify(message_line_1, message_line_2)
        return Response(status=200)


if __name__ == "__main__":

    app.run(debug=True, host="0.0.0.0", port=8000)
