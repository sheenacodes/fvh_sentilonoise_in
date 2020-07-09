# platform-input for sentilo noise

experimental work
designing Endpoints for platform to injest data and send it to apache kafka

To bring up service:

Note: the environment variables file config.env must be at root folder and
the ssl root cert (pem file) should be in folder /platform_in

dev config (flask dev server):

1. docker-compose up
2. send PUT requests to localhost:5000/cesva/v1 with sentilo noise data
3. should return success or failure response

prod config (nginx+gunicorn)

1. docker-compose -f docker-compose.prod.yml up

2,3,4 same as previous but port  for prod is 1337



