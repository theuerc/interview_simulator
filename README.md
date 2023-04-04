# Interview Simulator

Interview simulator that uses ChatGPT, Whisper, and Google Text-to-Speech

**Quickstart for Teaching Team:**

1. Clone the repo
```bash
git clone https://github.com/theuerc/interview_simulator
```

2. Run the following commands in the root directory of the repo
```bash
touch dev.db
docker-compose up --build
```

4. Copy a json with your Google Credentials into the project and modify the .env to include the path to that .json file and an OpenAI API Key: 
```bash
# Environment variable overrides for local development
FLASK_APP=autoapp.py
FLASK_DEBUG=1
FLASK_ENV=development
DATABASE_URL=sqlite:////tmp/dev.db
GUNICORN_WORKERS=1
LOG_LEVEL=debug
SECRET_KEY=not-so-secret
# In production, set to a higher number, like 31556926
SEND_FILE_MAX_AGE_DEFAULT=0
# API keys for ChatGPT, Whisper, and Google
OPENAI_API_KEY=[OPENAI_API_KEY]
GOOGLE_APPLICATION_CREDENTIALS=[PATH/TO/GOOGLE/KEY.JSON]
```

3. Open another terminal instance and run the following commands in the root directory of the repo:
```bash
docker-compose run --rm manage db upgrade
docker-compose up flask-dev
```

5. Make a dummy account on the website. These might work:
```bash
username: asdf
email: asdf@gmail.com
password: asdfasdf
```

6. Add a resume and transcript. These were made with ChatGPT:

**Resume:**
```
JONATHAN MYERS
Data Analyst
Harvard University | Class of 2019
Email: jonathan.myers@email.com | Phone: (123) 456-7890

EDUCATION
Harvard University, Cambridge, MA
Bachelor of Science in Statistics, May 2019
Relevant coursework: Data Analysis and Statistical Inference, Regression Analysis, Applied Time Series Analysis, Data Mining and Machine Learning, Bayesian Statistics.

EXPERIENCE
Data Analyst, ABC Corporation, Boston, MA
June 2019 - Present

Conducted data analysis and visualization to support strategic decision-making across the organization
Developed and implemented predictive models to identify patterns and trends in customer behavior
Created reports and dashboards to communicate insights to executive team and stakeholders
Collaborated with cross-functional teams to identify opportunities for process improvement and efficiency gains
Data Science Intern, XYZ Company, Cambridge, MA
May 2018 - August 2018

Conducted exploratory data analysis and modeling to support product development initiatives
Developed predictive models to forecast sales and customer demand
Created data visualizations and dashboards to communicate insights to stakeholders
Conducted research to identify best practices and emerging trends in data science and analytics
SKILLS

Proficient in programming languages such as Python, R, and SQL
Experience with data analysis and visualization tools such as Tableau and Power BI
Knowledge of statistical modeling techniques and machine learning algorithms
Strong analytical and problem-solving skills
Excellent communication and collaboration skills
AWARDS AND HONORS

Dean's List, Harvard College, 2015-2019
National Merit Scholarship Finalist, 2015
Harvard College Research Program Grant Recipient, 2017
REFERENCES
Available upon request.
```
**Job Description**
```
Data Scientist with Bioethics Background

SciCorp is a rapidly growing biotechnology company that focuses on developing innovative solutions to improve human health. We are seeking a highly motivated data scientist with a strong background in bioethics to join our team. The successful candidate will play a key role in developing and implementing data-driven solutions that address ethical issues in biotechnology research and development.

Responsibilities:

Design and implement data collection and analysis strategies to address ethical issues related to biotechnology research and development
Develop predictive models to identify potential ethical issues and their impacts on the company's research and development initiatives
Conduct ethical reviews of research proposals, including analyzing potential risks and benefits to human health, and proposing ethical solutions
Collaborate with cross-functional teams to design and implement ethical guidelines and best practices for research and development initiatives
Stay up-to-date with emerging trends and developments in bioethics and integrate this knowledge into the company's ethical policies and practices
Communicate complex ethical issues and analyses to both technical and non-technical stakeholders, including regulatory bodies and the public
Qualifications:

PhD in bioethics, philosophy, or a related field
Strong background in biotechnology research and development
Experience in data science, including data collection, analysis, and modeling
Knowledge of statistical analysis tools and programming languages such as Python or R
Familiarity with regulatory frameworks related to biotechnology research and development, such as IRB and FDA regulations
Excellent analytical and problem-solving skills
Strong communication and collaboration skills
Ability to work independently and as part of a team in a fast-paced environment
We offer competitive compensation packages, flexible work schedules, and opportunities for growth and development. If you are passionate about using data science to address ethical challenges in biotechnology research and development, we encourage you to apply.

To apply, please submit your CV, cover letter, and any relevant work samples to [insert email address].
```

7. Go to the interview page and click on the "Start Interview" button. Pretend you're being interviewed. Or don't. It's up to you.









----------------




**The next section is the original README.md file from the cookiecutter repo that I used for this project.**



--------------
## Docker Quickstart

This app can be run completely using `Docker` and `docker-compose`. **Using Docker is recommended, as it guarantees the application is run using compatible versions of Python and Node**.

There are three main services:

To run the development version of the app

```bash
docker-compose up flask-dev
```

To run the production version of the app

```bash
docker-compose up flask-prod
```

The list of `environment:` variables in the `docker-compose.yml` file takes precedence over any variables specified in `.env`.

To run any commands using the `Flask CLI`

```bash
docker-compose run --rm manage <<COMMAND>>
```

Therefore, to initialize a database you would run

```bash
docker-compose run --rm manage db init
docker-compose run --rm manage db migrate
docker-compose run --rm manage db upgrade
```

A docker volume `node-modules` is created to store NPM packages and is reused across the dev and prod versions of the application. For the purposes of DB testing with `sqlite`, the file `dev.db` is mounted to all containers. This volume mount should be removed from `docker-compose.yml` if a production DB server is used.

Go to `http://localhost:8080`. You will see a pretty welcome screen.

### Running locally

Run the following commands to bootstrap your environment if you are unable to run the application using Docker

```bash
cd interview_simulator
pipenv install --dev
pipenv shell
npm install
npm run-script build
npm start  # run the webpack dev server and flask server using concurrently
```

Go to `http://localhost:5000`. You will see a pretty welcome screen.

#### Database Initialization (locally)

Once you have installed your DBMS, run the following to create your app's
database tables and perform the initial migration

```bash
flask db init
flask db migrate
flask db upgrade
```

## Deployment

When using Docker, reasonable production defaults are set in `docker-compose.yml`

```text
FLASK_ENV=production
FLASK_DEBUG=0
```

Therefore, starting the app in "production" mode is as simple as

```bash
docker-compose up flask-prod
```

If running without Docker

```bash
export FLASK_ENV=production
export FLASK_DEBUG=0
export DATABASE_URL="<YOUR DATABASE URL>"
npm run build   # build assets with webpack
flask run       # start the flask server
```

## Shell

To open the interactive shell, run

```bash
docker-compose run --rm manage db shell
flask shell # If running locally without Docker
```

By default, you will have access to the flask `app`.

## Running Tests/Linter

To run all tests, run

```bash
docker-compose run --rm manage test
flask test # If running locally without Docker
```

To run the linter, run

```bash
docker-compose run --rm manage lint
flask lint # If running locally without Docker
```

The `lint` command will attempt to fix any linting/style errors in the code. If you only want to know if the code will pass CI and do not wish for the linter to make changes, add the `--check` argument.

## Migrations

Whenever a database migration needs to be made. Run the following commands

```bash
docker-compose run --rm manage db migrate
flask db migrate # If running locally without Docker
```

This will generate a new migration script. Then run

```bash
docker-compose run --rm manage db upgrade
flask db upgrade # If running locally without Docker
```

To apply the migration.

For a full migration command reference, run `docker-compose run --rm manage db --help`.

If you will deploy your application remotely (e.g on Heroku) you should add the `migrations` folder to version control.
You can do this after `flask db migrate` by running the following commands

```bash
git add migrations/*
git commit -m "Add migrations"
```

Make sure folder `migrations/versions` is not empty.

## Asset Management

Files placed inside the `assets` directory and its subdirectories
(excluding `js` and `css`) will be copied by webpack's
`file-loader` into the `static/build` directory. In production, the plugin
`Flask-Static-Digest` zips the webpack content and tags them with a MD5 hash.
As a result, you must use the `static_url_for` function when including static content,
as it resolves the correct file name, including the MD5 hash.
For example

```html
<link rel="shortcut icon" href="{{static_url_for('static', filename='build/favicon.ico') }}">
```

If all of your static files are managed this way, then their filenames will change whenever their
contents do, and you can ask Flask to tell web browsers that they
should cache all your assets forever by including the following line
in ``.env``:

```text
SEND_FILE_MAX_AGE_DEFAULT=31556926  # one year
```

## Heroku

Before deploying to Heroku you should be familiar with the basic concepts of [Git](https://git-scm.com/) and [Heroku](https://heroku.com/).

Remember to add migrations to your repository. Please check `Migrations`_ section.

Since the filesystem on Heroku is ephemeral, non-version controlled files (like a SQLite database) will be lost at least once every 24 hours. Therefore, a persistent, standalone database like PostgreSQL is recommended. This application will work with any database backend that is compatible with SQLAlchemy, but we provide specific instructions for Postgres, (including the required library `psycopg2-binary`).

**Note:** `psycopg2-binary` package is a practical choice for development and testing but in production it is advised to use the package built from sources. Read more in the [psycopg2 documentation](http://initd.org/psycopg/docs/install.html?highlight=production%20advised%20use%20package%20built%20from%20sources#binary-install-from-pypi).

If you keep your project on GitHub you can use 'Deploy to Heroku' button thanks to which the deployment can be done in web browser with minimal configuration required.
The configuration used by the button is stored in `app.json` file.

<a href="https://heroku.com/deploy" style="display: block"><img src="https://www.herokucdn.com/deploy/button.svg" title="Deploy" alt="Deploy"></a>
    <br>

Deployment by using [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli):

* Create Heroku App. You can leave your app name, change it, or leave it blank (random name will be generated)

    ```bash
    heroku create interview_simulator
    ```

* Add buildpacks

    ```bash
    heroku buildpacks:add --index=1 heroku/nodejs
    heroku buildpacks:add --index=1 heroku/python
    ```

* Add database addon which creates a persistent PostgresSQL database. These instructions assume you're using the free [hobby-dev](https://elements.heroku.com/addons/heroku-postgresql#hobby-dev) plan. This command also sets a `DATABASE_URL` environmental variable that your app will use to communicate with the DB.

    ```bash
    heroku addons:create heroku-postgresql:hobby-dev --version=11
    ```

* Set environmental variables (change `SECRET_KEY` value)

    ```bash
    heroku config:set SECRET_KEY=not-so-secret
    heroku config:set FLASK_APP=autoapp.py
    heroku config:set SEND_FILE_MAX_AGE_DEFAULT=31556926
    ```

* Please check `.env.example` to see which environmental variables are used in the project and also need to be set. The exception is `DATABASE_URL`, which Heroku sets automatically.

* Deploy on Heroku by pushing to the `heroku` branch

    ```bash
    git push heroku main
    ```
