# Basic search
python indeed_ca_scraper.py --query "software engineer" --location "Toronto, ON"

# 5 pages, save to JSON, remote only
python indeed_ca_scraper.py --query "data analyst" --location "Vancouver, BC" --pages 5 --format json --remote

# Full-time jobs posted in last 7 days
python indeed_ca_scraper.py --query "nurse" --location "Calgary, AB" --date-posted 7 --job-type fulltime --pages 3

##  