# ProjectPlace

This application is based on Django-PostgreSQL-AWS.
Through this application, users can sell their personal projects in this e-marketplace.

This app has folders:

1. `projectplace` - This folder contains the settings of the application.
2. `project` - This is the application that defines APIs to CRUD projects.

The PostgreSQL database is dockerized. To run the DB Container, run the following command:

```bash
docker run -p 5432:5432 --name projectplacedb -e POSTGRES_PASSWORD=postgres -d postgres
```

To run the application, run the following command:

```bash
python manage.py runserver
```

or

```bash
gunicon --bind 0.0.0.0:8000 --reload projectplace.wsgi
```

The `project` application has following endpoints:

1. `GET /api/v2/projects/project` - This endpoint returns all the projects.

    ```curl
    curl --location 'http://127.0.0.1:8000/api/v2/projects/project/?page=1&page_size=5'
    ```

    ```curl
    curl --location 'http://127.0.0.1:8000/api/v2/projects/project/?page=1&page_size=5&tech=Python&tech=FastAPI'
    ```

    ```curl
    curl --location 'http://127.0.0.1:8000/api/v2/projects/project/?page=1&page_size=5&category=IOS%20Application&category=Web%20Application'
    ```

    Query Params are:

    1. `page` - This is the page number of the projects to be returned. Default is 1.
    2. `page_size` - This is the number of projects to be returned per page. Default is 5 and max is 10.
    3. `priceMin & priceMax` - This is the price range of the projects to be returned. Can be used combinely to give projects in the desired range.
    4. `tech` - This is the tech stack of the projects to be returned. Takes input of the stack name. Ex: Python, Java, FastAPI etc. The inputs must match with the stack name in the database.
    5. `category` - This is the category of the projects to be returned. Takes input of the category name. Ex: Web App, Cloud App etc. The inputs must match with the category name in the database.
    6. `ordering` - The ordering of the result can be done on the basis of price only.To order in descending order, add a `-` before the field name. Ex: `ordering=-price` will return the projects in descending order of price.

2. `POST /api/v2/projects/project` - This endpoint creates a project.

    ```curl
    curl --location 'http://127.0.0.1:8000/api/v2/projects/project/' \
    --form 'uploaded_images=@"/home/shashwat/Pictures/Screenshots/Screenshot from 2024-01-14 00-27-18.png"' \
    --form 'uploaded_images=@"/home/shashwat/Pictures/Screenshots/Screenshot from 2024-01-13 23-59-19.png"' \
    --form 'uploaded_documents=@"/home/shashwat/Pictures/Screenshots/Screenshot from 2024-01-13 23-59-19.png"' \
    --form 'name="Web Scrapper"' \
    --form 'price="500"' \
    --form 'description="This is a web scrapper that can scrape hotel listing websites like oyo, yatra etc. The tech stack used is python, vanillajs."' \
    --form 'application_type="1"' \
    --form 'application_type="3"' \
    --form 'tech_stack="1"' \
    --form 'tech_stack="2"' \
    --form 'tech_stack="3"'
    ```

3. `GET /api/v2/projects/project/<project_id:UUID>` - This endpoint returns a project with given ID.

    ```curl
    curl --location 'http://127.0.0.1:8000/api/v2/projects/project/23ee0495-9b80-4073-a5fc-72ec37006f15'
    ```

4. `PUT /api/v2/projects/project/<project_id:UUID>` - This endpoint updates a project with given ID.

    ```curl
    curl --location --request PUT 'http://127.0.0.1:8000/api/v2/projects/project/3ef2510e-d1fd-4722-8d6a-4e7c18531937' \
    --form 'name="Grocery Store Project"' \
    --form 'description="Sell edible products online easily without any hassle of delivering it."' \
    --form 'price="20000"' \
    --form 'uploaded_images=@"/home/shashwat/Downloads/Typewriter-pana.png"' \
    --form 'uploaded_documents=@"/home/shashwat/IdeaProjects/PotionsAPI/logs.txt"' \
    --form 'uploaded_documents=@"/home/shashwat/IdeaProjects/PotionsAPI/mvnw.cmd"' \
    --form 'application_type="4"' \
    --form 'application_type="1"' \
    --form 'application_type="2"' \
    --form 'tech_stack="2"' \
    --form 'tech_stack="5"' \
    --form 'tech_stack="3"' \
    --form 'deleted_images=""' \
    --form 'deleted_documents=""'
    ```

5. `DELETE /api/v2/projects/project/<project_id:UUID>` - This endpoint deletes a project with given ID.

    ```curl
    curl --location --request DELETE 'http://127.0.0.1:8000/api/v2/projects/project/beb6f7a3-77a6-44c2-add7-0016d2e9307c'
    ```

The Project entity has the following fields -

1. `id` - This is the UUID of the project.
2. `name` - This is the name of the project.
3. `price` - This is the price of the project. The min value is 500 and max value is 999999.
4. `description` - This is the description of the project.
5. `application_type` - This is the application type of the project. Ex: Cloud App, Web App etc. This is a many-to-many field and can have multiple values of the primary keys of the `ApplicationType` entity.
6. `tech_stack` - This is the tech stack of the project. Ex: Python, Java etc. This is a many-to-many field and can have multiple values of the primary keys of the `TechStack` entity.
7. `created_at` - This is the timestamp when the project was submitted into the application.
8. `uploaded_images` - This is the list of images of the project. This is a foreign field having foreign key to the Project model.
9. `uploaded_documents` - This is the list of documents of the project. This is a foreign field having foreign key to the Project model.
