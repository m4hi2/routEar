"""This is the main module."""


import sys

from os import path
from flask import Flask, request, Response

PLT = sys.platform

if PLT == "win32":
    from win10toast import ToastNotifier
    toaster = ToastNotifier()
elif PLT == "linux":
    from contextlib import closing
    from jeepney import DBusAddress, new_method_call
    from jeepney.io.blocking import open_dbus_connection
    NOTIFIER = DBusAddress('/org/freedesktop/Notifications',
                           bus_name='org.freedesktop.Notifications',
                           interface='org.freedesktop.Notifications')
    NOTIF_ID = None

elif PLT == "darwin":
    import pync
else:
    print("unsupported platform")
    sys.exit(1)


def notify(title='title', body='text', icon='python'):
    """Notifier function."""
    if PLT == "win32":
        toaster.show_toast(
            title,
            body,
            threaded=True,
            icon_path=path.join(
                path.dirname(__file__), 'data', '%s.ico' % icon)
        )
    elif PLT == "linux":
        reply = None

        with closing(open_dbus_connection(bus='SESSION')) as bus:
            msg = new_method_call(NOTIFIER, 'Notify', 'susssasa{sv}i',
                                  (
                                      "routEar",
                                      NOTIF_ID or 0,
                                      'file://%s' % path.join(path.dirname(__file__),
                                                              'data', '%s.png' % icon),
                                      title,
                                      body,
                                      [], {},
                                      -1,
                                  ))
            reply = bus.send_and_get_reply(msg)
        globals()['NOTIF_ID'] = reply.body[0] if reply else None
    elif PLT == "darwin":
        pync.notify(
            f"{title} \n {body}",
            title="routEar"
        )

    else:
        return False
    return True


app = Flask(__name__)


@app.route('/', methods=['POST'])
def callback():
    """Flask app route for /."""
    if request.method == 'POST':
        message = request.json
        print(message)
        message_line_1 = f"Internet is {message['status']}"
        message_line_2 = f"Affected {message['affected']}"
        notify(message_line_1, message_line_2)
        return Response(status=200)

    return Response(status=403)


def main():
    """Start the flask app on port 8000."""
    app.run(debug=True, host="0.0.0.0", port=8000)
