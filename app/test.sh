my_snake_server_url="localhost:8080"

curl $my_snake_server_url/start \
         -X POST \
              -H "Content-Type: application/json" \
                   --data @- <<-REQUEST_BODY
{"width":20,"height":20,"game_id":"a2facef2-b031-44ba-a36c-0859c389ef96"} 
REQUEST_BODY


curl $my_snake_server_url/move \
         -X POST \
         -H "Content-Type: application/json" \
         --data @- <<-REQUEST_BODY
{
  "you": "2c4d4d70-8cca-48e0-ac9d-03ecafca0c98",
  "width": 10,
  "turn": 0,
  "snakes": [
    {
      "taunt": "git gud",
      "name": "my-snake",
      "id": "2c4d4d70-8cca-48e0-ac9d-03ecafca0c98",
      "health_points": 93,
      "coords": [
        [
          0,
          0
        ],
        [
          0,
          0
        ],
        [
          0,
          0
        ]
      ]
    }
  ],
  "height": 10,
  "game_id": "a2facef2-b031-44ba-a36c-0859c389ef96",
  "food": [
    [2,2],[ 1,1 ] 
  ],
  "dead_snakes": [
    {
      "taunt": "gotta go fast",
      "name": "other-snake",
      "id": "83fdf2b9-c8d0-44f4-acb2-0c506139079e",
      "health_points": 50,
      "coords": [
        [
          5,
          0
        ],
        [
          5,
          0
        ],
        [
          5,
          0
        ]
      ]
    }
  ]
}
REQUEST_BODY

