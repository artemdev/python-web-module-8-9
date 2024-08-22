# Quotes Scraper

## Technologies
- **Python**
- **MongoEngine**
- **PyMongo**
- **Redis**
- **Faker**
- **Scrapy**
  
## Features
**Web Scraping Execution**
  - Utilized `Scrapy` for web scraping.
  - Successfully scraped the site [http://quotes.toscrape.com](http://quotes.toscrape.com).

**Data Extraction**
  - Generated `quotes.json` containing all information about quotes from all pages of the site.
  - Generated `authors.json` containing information about the authors of the quotes.

**Data Upload**
  - Implemented a script that creates MongoDB database from JSON files.
