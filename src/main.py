from core import create_tables, insert_cars_bulk
from database import SessionLocal
from scraper import ListCrawler, DetailCrawler


def main():
    print('Creating database tables...')
    create_tables()
    
    print('Scraping car listings...')
    lc = ListCrawler('https://auto.ria.com/uk/search/?indexName=auto&page=0')
    found_cars = lc.get_all_hrefs(stop=1)  # Get URLs from 3 pages
    
    print(f'Found {len(found_cars)} car URLs')

    print('Extracting detailed information...')
    dc = DetailCrawler(found_cars)
    parsed_data = dc.get_all_info() 
    
    print(f'Successfully parsed {len(parsed_data)} cars')
 
    print('Saving to database...')
    with SessionLocal() as db:
        inserted_count = insert_cars_bulk(db, parsed_data)
    
    print(f'Complete: {inserted_count} cars saved to database')


if __name__ == '__main__':
    main()