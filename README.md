<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#validation">Validation</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This project consists of a Python script that scrapes data from a website about tourist routes in Madrid, stores it in an OpenSearch database, and provides a Jupyter notebook with example queries to retrieve the stored information.



### Built With

1. Python: programming language used for web scraping and interacting with OpenSearch
2. Scrapy: Python framework used for web scraping
3. OpenSearch: search engine used for storing and retrieving scraped data
4. Docker: platform used for containerizing and deploying applications
5. Docker Compose: tool used for defining and running multi-container Docker applications
6. Bash: shell script used for automating the setup process and executing commands
7. Jupyter Notebook: web-based interactive computational environment for creating and sharing documents containing live code, equations, visualizations, and narrative text

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This repository contains a convenient bash script that automates the process of installing dependencies, setting up a database, creating an index, and storing scraped information. By running the run_script.sh file, the user can execute all of these steps with a single command. This makes it easier to quickly set up a fully functional web scraping pipeline without having to go through the tedious process of manually setting up each component.

### Installation


1. Clone the repo
   ```sh
   git clone https://github.com/fjmaco/madridRoutesScraping
   ```
2. Navigate to the prueba folder:
   ```sh
   cd madridRoutesScraping/prueba
   ```
3. Execute the run_script.sh shell script:
   ```js
   ./run_script.sh
   ```

This will start the docker container to host the OpenSearch database, create the required index, scrape the Madrid Routes website, and store the information in the database.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- VALIDATION EXAMPLES -->
## Validation

To validate the execution of the project, run the mvp.ipynb file included in the repository. This Jupyter notebook contains a series of queries that can be executed to retrieve the stored information. Specifically, the queries will fetch the first result of an "etapa" (stage), the first result of a "ruta" (route), the first itinerary, and finally display the step-by-step instructions for that itinerary. Running these queries successfully will indicate that the project has been executed and the data has been successfully stored and indexed in the OpenSearch database.

<p align="right">(<a href="#readme-top">back to top</a>)</p>




<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

