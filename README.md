# platform-input for sentilo noise

To bring up service:

Note: the environment variables file config.env must be at root folder and
the ssl root cert (pem file) should be in folder /platform_in

dev config (flask dev server):

    docker-compose up
    send PUT requests to localhost:5000/cesva/v1 with sentilo noise data
    should return success or failure response

prod config (nginx+gunicorn)

    docker-compose -f docker-compose.prod.yml up

2,3,4 same as previous but port  for prod is 1337

example PUT data:
```json
{
	"sensors": [{
			"sensor": "TA120-T246174-N",
			"observations": [{
				"value": "38.7",
				"timestamp": "12/03/2020T12:26:58UTC"
			}]
		},
		{
			"sensor": "TA120-T246174-O",
			"observations": [{
				"value": "false",
				"timestamp": "12/03/2020T12:26:58UTC"
			}]
		},
		{
			"sensor": "TA120-T246174-U",
			"observations": [{
				"value": "false",
				"timestamp": "12/03/2020T12:26:58UTC"
			}]
		},
		{
			"sensor": "TA120-T246174-S",
			"observations": [{
				"value": "029.9,0,1;029.8,0,1;030.0,0,1;030.2,0,1;030.0,0,1;030.2,0,1;030.1,0,1;034.5,0,1;050.0,0,0;046.2,0,0;035.9,0,0;030.3,0,1;030.5,0,1;030.6,0,1;030.5,0,1;030.2,0,1;030.0,0,1;030.0,0,1;029.8,0,1;029.8,0,1;029.6,0,1;029.6,0,1;029.7,0,1;029.9,0,1;033.8,0,1;046.7,0,0;032.4,0,1;030.8,0,1;030.3,0,1;029.9,0,1",
				"timestamp": "12/03/2020T12:26:58UTC"
			}]
		}
	]
}
```


