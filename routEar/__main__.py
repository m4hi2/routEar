import sys
from . import app

def main(args=None):
    global app
    app.run(debug=True, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    sys.exit(main())
