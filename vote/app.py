from flask import Flask, render_template, request, make_response, g
from redis import Redis
import os
import socket
import random
import json
import logging
from werkzeug.middleware.dispatcher import DispatcherMiddleware

# Environment variables for vote options
option_a = os.getenv('OPTION_A', "Cats")
option_b = os.getenv('OPTION_B', "Dogs")
hostname = socket.gethostname()

# Create the actual vote app
vote_app = Flask(__name__)

# Logging setup
gunicorn_error_logger = logging.getLogger('gunicorn.error')
vote_app.logger.handlers.extend(gunicorn_error_logger.handlers)
vote_app.logger.setLevel(logging.INFO)

# Redis connection
def get_redis():
    if not hasattr(g, 'redis'):
        g.redis = Redis(host="redis", db=0, socket_timeout=5)
    return g.redis

# Main route
@vote_app.route("/", methods=['POST', 'GET'])
def hello():
    voter_id = request.cookies.get('voter_id')
    if not voter_id:
        voter_id = hex(random.getrandbits(64))[2:-1]

    vote = None

    if request.method == 'POST':
        redis = get_redis()
        vote = request.form['vote']
        vote_app.logger.info('Received vote for %s', vote)
        data = json.dumps({'voter_id': voter_id, 'vote': vote})
        redis.rpush('votes', data)

    resp = make_response(render_template(
        'index.html',
        option_a=option_a,
        option_b=option_b,
        hostname=hostname,
        vote=vote,
    ))
    resp.set_cookie('voter_id', voter_id)
    return resp

# Wrap the app under /app for ALB routing
application = DispatcherMiddleware(Flask(__name__), {
    '/app': vote_app
})

# Local dev entry point (not used in production)
if __name__ == "__main__":
    vote_app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
