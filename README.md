# Web scraper
Automated web scraping application that collects car advertisement data. 
The scraper extracts vehicle and seller information including titles, prices, mileage, seller details, contact numbers, images, license plates, and VIN codes from listing pages. 

Built with **Python**, uses **BeautifulSoup** for HTML parsing and **Selenium** with headless Firefox for dynamic content extraction (phone numbers extraction). Used **Pydantic** for data validation and **SQLAlchemy** to access the **PostgreSQL** via ORM. 

App includes a scheduler for automated daily scraping and database dumps.

Comes containerized with Docker Compose for easy deployment alongside pgAdmin for database management.

### Get the project 

1. `git clone` this repository
2. Run `docker-compose up`
3. Check the logs in the CLI | Access pgAdmin in your browser (included in the compose file)
4. Stop containers: `docker-compose down`
5. Stop containers and clean volumes: `docker-compose down -v`

### Project info

All settings are located in `src/settigs.py`.

- `START_URL` - Starting list-view page for the scraper

- `PAGES_TO_SCRAPE` - Number of list-view pages to collect detail links from

- `SCRAPE_TIME` - Daily scrape time (UTC, Debian Docker container timezone)

- `DUMP_TIME` - Daily database dump time (UTC, Debian Docker container timezone)

- `DUMPS_DIR` - Directory for database dumps

Tweak scheduler in `src/main` - `run_scheduler()` func.
By default scheduler is disabled.

The application scrapes `PAGES_TO_SCRAPE` pages of the site and performs a database dump after the scrape finishes.

All actions are **synchronous**.


### Setup pgadmin

1. Go in your browser to: http://127.0.0.1:5050/
2. Login:
    - Email: `admin@admin.com` 
    - Password: `admin`
3. Go to Object > Register > Server
4. General:
    - Name: `postgres` 
5. Connection:
    - Hostname / address: `db` 
    - Username: `postgres` 
    - Password: `postgres`
6. Click `Save`
7. In the left panel: Servers > postgres > Databases > postgres.
8. Open Query Tool (`Alt + Shift + Q`) or click on the icon.
9. Run any queries. `SELECT * FROM advertisement;` - to see all collected data.