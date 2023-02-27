# Financial App

This app gathers data about securities (IBM and APPL to start). It uses Python Django and Django REST framework for  serving the application and API, PostgreSQL for database storage, and Docker for containerization.

# Getting Started
This project utilizes Docker, so please make sure you have it installed already

1. If you do not have an API key for Alphavantage, please get one at https://www.alphavantage.co/support/#api-key
2. In `finance/finance/`, rename `.env.example` to `.env`, and change the value of `ALPHAVANTAGE_API_KEY` to your api key
3. In your terminal in the repository root directory, run 
```
docker-compose build
```
4. After building, in the same terminal run 
```
docker-compose up -d
```
5. Now that your docker instance is running, we next need to find the container that is running our backend service. Either through the Docker desktop app or from using `docker ps` in your terminal, find the container ID for our backend instance, the name should be `python_assignment-web-1` . After locating the container ID, open up an interactive terminal in it with 
```
docker exec -it <container image> bash
```
6. Now inside the docker container, we need to run our database migrations with 
 ```
python finance/manage.py migrate
```
7. finally, we need to seed our data by running 
```
python get_raw_data.py
```
 That's it! You can now try going to see your new data on your local server with by going to `http://localhost:8000/api/financial_data`
