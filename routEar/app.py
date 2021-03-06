import sys

from flask import Flask, request, Response
from os import path

plt = sys.platform

if plt == "win32":
    from win10toast import ToastNotifier
    toaster = ToastNotifier()
elif plt == "linux":
    from contextlib import closing
    try:
        from jeepney import DBusAddress, new_method_call
        from jeepney.io.blocking import open_dbus_connection
    except (ImportError, ModuleNotFoundError):
        import subprocess as sp
        notifier, notif_id = None, None
    else:
        notifier = DBusAddress('/org/freedesktop/Notifications',
                               bus_name='org.freedesktop.Notifications',
                               interface='org.freedesktop.Notifications')
        notif_id = None

elif plt == "darwin":
    import pync
else:
    print("unsupported platform")
    sys.exit(1)


def notify(title='title', body='text', icon='python'):
    if plt == "win32":
        global toaster
        toaster.show_toast(
            title,
            body,
            threaded=True,
            icon_path=path.join(
                path.dirname(__file__), 'data', '%s.ico' % icon)
        )
    elif plt == "linux":
        global notif_id
        reply = None

        with closing(open_dbus_connection(bus='SESSION')) as bus:
            msg = new_method_call(notifier, 'Notify', 'susssasa{sv}i',
                                  (
                                      "routEar",
                                      notif_id or 0,
                                      'file://%s' % path.join(path.dirname(__file__),
                                                              'data', '%s.png' % icon),
                                      title,
                                      body,
                                      [], {},
                                      -1,
                                  ))
            reply = bus.send_and_get_reply(msg)
        notif_id = reply.body[0] if reply else None
    elif plt == "darwin":
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

    if request.method == 'POST':
        message = request.json
        print(message)
        message_line_1 = f"Internet is {message['status']}"
        message_line_2 = f"Affected {message['affected']}"
        notify(message_line_1, message_line_2)
        return Response(status=200)


def main(args=None):
    app.run(debug=True, host="0.0.0.0", port=8000)
