import socketio
import eventlet
import eventlet.wsgi
from flask import Flask, render_template
from gpiozero import LED

sio = socketio.Server()
app = Flask(__name__)

#led = LED(7)
lampStatus = False;
def switchLamp():
    global lampStatus
    if (lampStatus == True):
        led.on()
        lampStatus = False
    else:
        led.off()
        lampStatus = True
    print lampStatus

@app.route('/')
def index():
    """Serve the client-side application."""
    return render_template('./index.html')

@sio.on('change')
def change(sid, environ):
    print("change ", sid)
    switchLamp()

if __name__ == '__main__':
    # wrap Flask application with engineio's middleware
    app = socketio.Middleware(sio, app)

    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('', 8000)), app)