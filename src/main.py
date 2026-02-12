import schedule
import time
import subprocess
from datetime import datetime
from pathlib import Path

import settings
from core import create_tables, insert_cars_bulk
from database import SessionLocal
from scraper import ListCrawler, DetailCrawler


def scrape():
    print('Creating database tables...')
    create_tables()
    
    print('Scraping car listings...')
    lc = ListCrawler(settings.START_URL)
    found_cars = lc.get_all_hrefs(pages_to_scrap=settings.PAGES_TO_SCRAP)
    
    print(f'Found {len(found_cars)} car URLs')
    print('Extracting detailed information...')
    dc = DetailCrawler(found_cars)
    parsed_data = dc.get_all_info() 
    
    print(f'Successfully parsed {len(parsed_data)} cars')
 
    print('Saving to database...')
    with SessionLocal() as db:
        inserted_count = insert_cars_bulk(db, parsed_data)
    
    print(f'Complete: {inserted_count} cars saved to database')


def scraping_job():
    print(f'[{datetime.now()}] Daily scraping job...')
    
    scrape()
    
    print(f'[{datetime.now()}] Daily job completed')


def dump_job():
    print(f'[{datetime.now()}] Daily database dump job...')
    
    dumps_dir = Path(settings.DUMPS_DIR)
    dumps_dir.mkdir(exist_ok=True)
    
    # gen file name
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    dump_file = dumps_dir / f'dump_{timestamp}.sql'
    
    # do db dump
    dump_command = [
        'pg_dump',
        '-h', settings.DB_HOST,
        '-p', settings.DB_PORT,
        '-U', settings.DB_USER,
        '-d', settings.DB_NAME,
        '-f', str(dump_file),
        '--no-password'
    ]
    
    print(f'Creating dump: {dump_file}')
    subprocess.run(dump_command, check=True)
    
    print(f'[{datetime.now()}] Dump saved to {dump_file}\n')


def run_scheduler():
    scraping_job()
    dump_job()

    # print('Scheduler started')
    # print(f'Scraping scheduled at: {settings.SCRAPE_TIME}')
    # print(f'Database dump scheduled at: {settings.DUMP_TIME}')

    # schedule.every().day.at(settings.SCRAPE_TIME).do(scraping_job)
    # schedule.every().day.at(settings.DUMP_TIME).do(dump_job)
    
    # while True:
    #     schedule.run_pending()
    #     time.sleep(60)


if __name__ == '__main__':
    run_scheduler()