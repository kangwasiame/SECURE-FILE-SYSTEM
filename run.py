from app import create_app
from typing import cast

app = create_app()

if __name__ == '__main__':
    app.run(
        debug=True,
        host=cast(str, app.config['HOST']),
        port=cast(int, app.config['PORT']),
    )