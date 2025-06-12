# order status tracking app
This application simulates an online food ordering service that allows for customers to order from a wider range of restaurants and cuisines.

The events are order requests and payment requests. Customers are able to place an order anytime during the day; however, we expect a peak of orders during the nighttime since most people are off work. This could reach as many as 1000 requests per minutes for both requests (i.e., requests and payment). We implemeted the microservice architecture to distribute and handle different resources, such as receiver server, data server and processing server. Each of the services/servers can be developed, deployed, and maintained independently.
The requests are stored to allow the following:
* Automatic fulfillment and submission of orders
* Manual viewing payments by restaurants
* Analysis of the data for restaurants to have better preparation and prediction for busy peak times. 

Users of the system are customers (i.e., those placing an order/food) and restaurants (i.e., receiving payments and orders)

###### Technologies:

- Python
- Connexion
- MySQL
- Docker
- React
- Postman
- JMeter
- Microsoft Azure
- Microservices
- Git/Github


