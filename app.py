from app import create_app
from app.database import init_db

from app.database import init_db, Session
from app.OrderController import OrderController

app = Flask(__name__)
app.config.from_object(Config)
init_db()

logger = logging.getLogger(app.config['LOGGER_NAME'])


def setup_logging():
    """Set up the logger configuration."""
    config_file = app.config['LOGGER_CONFIG_FILE']

    if not os.path.exists(app.config['LOG_DIR']):
        os.makedirs(app.config['LOG_DIR'])

    with open(config_file) as f_in:
        config = json.load(f_in)
    logging.config.dictConfig(config)

@app.route('/')
def hello_world():  # todo put application's code here
    app.logger.info('Hello World')
    return 'Hello World!'


@app.route('/order/<int:id>', methods=['PUT'])
def order_update(id):
    data = request.get_json()
    return OrderController.update(id, data, Session)

    

if __name__ == '__main__':
    app.run(use_reloader=False)
