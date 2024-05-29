#!/bin/sh
# test push
# Execute Flask commands
# flask db init
# flask db migrate -m 'initial'
# flask db upgrade
flask run --host=0.0.0.0 --debug
