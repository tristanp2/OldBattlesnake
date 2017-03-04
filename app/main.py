import bottle
import os
import random
import numpy as np

from snake import Snake

ID = "2c4d4d70-8cca-48e0-ac9d-03ecafca0c98"
taunts = [ "you momma so fat" ]

@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
    data = bottle.request.json
    game_id = data['game_id']

    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    # TODO: Do things with data

    return {
        'color': '#00FF00',
        'taunt': 'lets get it on!',
        'head_url': head_url,
        'name' : 'if !dead then drink++'
    }


@bottle.post('/move')
def move():
    data = bottle.request.json
    print "Received move ..." #request:{}".format(data)
    
    board_width = data['width']
    board_height = data['height']
    me = Snake(ID, board_height, board_width)

    print "Created snake with id = ", ID 

    blockades =  np.array(map(lambda x: extend_head(x,me), data["snakes"])).flatten()
    print "No go areas: {}".format(blockades)

    #TODO limit based to first N food or based on threshold
    food = map(tuple, data["food"])
    food.sort(manhattan) 
    print "Food @ {}".format(food)

    move = me.gather_food(food, blockades)

    #directions = ['up', 'down', 'left', 'right']
     

    return {
        'move': move, #random.choice(directions),
        'taunt': random.choice(taunts)
    }

def extend_head(snake, me):
    coords = map(tuple, snake["coords"])
    print "Have snake: {} -> {}".format(snake["id"], coords)
    head = (x,y) = coords[0]
   
    if snake["id"] == ID:
        print "Setting head position to {}".format(head)
        me.head = head
    
    coords.extend([(x+1, y), (x, y-1), (x-1, y), (x, y+1)])
    return coords

def manhattan(xy):
    (x1,y1) = xy
    (x2,y2) = my_snake.position
    dx = abs(x1-x2)
    dy = abs(y1-y2)
    return dx + dy

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
