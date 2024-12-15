<h1 align="center">TiStyle Shop</h1>


This project is an e-commerce platform built using Django, designed to provide users with an intuitive and seamless shopping experience. The application allows users to browse and search for products, add them to their shopping cart, and securely complete their purchases via Stripe. Additionally, the platform features a robust user system, allowing customers to mark favorite products, leave reviews, and rate items to assist other shoppers in making informed decisions.

The project integrates Celery for handling asynchronous tasks such as sending promotional emails to subscribers. The application also leverages PostgreSQL as the database system to store all necessary data and ensure scalability for future growth. Docker is used to containerize the application, providing a consistent environment across development, testing, and production stages.

## Installation

### Clone the Repository

```bash
git clone git@github.com:saywin/tistyle.git
cd tistyle_shop
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Setup Database

```
export DB_HOST=<your_db_hostname>
export DB_NAME=<your_db_name>
export DB_USER=<your_db_username>
export DB_PASSWORD=<your_db_password>
export SECRET_KEY=<your secret key>
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
python manage.py createsuperuser
```

# Setup Celery and Celery Beat
```
export CELERY_BROKER_URL=<your_celery_brocker_url>
export CELERY_RESULT_BACKEND=<your_result_url>
celery -A library_manage worker -l INFO --pool=solo
celery -A library_manage beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

# Run with docker

Docker should be installed (you can download it here: https://www.docker.com/)

```shell
docker-compose build
docker-compose up
docker compose ps
docker exec -it your_image_name sh
- Create new admin user. `docker-compose run app sh -c "python manage.py createsuperuser`;
- Run tests using different approach: `docker-compose run conf sh -c "pytest"`;
```

# Getting access

To access the API endpoints, follow these steps:

1. Go to one of the following URLs:
   - [Register user](http://127.0.0.1:8000/users/registration/)

2. Type in your Email & Password. For example:
   - Email address: admin@example.com
   - Password: 1qazcde3

## Technologies used

- **Django**: A high-level Python web framework that promotes rapid development and clean, pragmatic design.
- **PostgreSQL**: A powerful, open-source relational database management system used to store application data.
- **Celery**: A distributed task queue that allows asynchronous task execution, used for sending promotional emails to subscribers.
- **Docker**: A platform for developing, shipping, and running applications in containers, ensuring consistent environments across different stages.
- **Stripe**: A payment gateway integrated for handling online transactions securely.
- **HTML/CSS**: Standard markup and styling languages used to create the front-end of the application.
- **Bootstrap**: A front-end framework for responsive design and building user interfaces.
- **Shopping Cart**: Functionality to manage products added to the user's cart before checkout.
- **Favorites**: Feature allowing users to mark and save their favorite products.
- **Product Reviews & Ratings**: Users can leave reviews and rate products to help others make purchasing decisions.
- **Search**: A search feature to find products based on various parameters.

