import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def scrape_speeches(person, start_date):
    base_url = 'https://www.federalreserve.gov/newsevents/speech/{}{}a.htm'

    # Start and end dates for scraping
    start_date = start_date 
    end_date = datetime.now()

    # List to store the URLs of Powell's speeches
    speeches = []

    # Iterate through dates and construct URLs
    current_date = start_date
    while current_date <= end_date:
        # Format the current date as part of the URL
        url_date = current_date.strftime('%Y%m%d')

        # Construct the URL for the current date
        url = base_url.format(person, url_date)

        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find the section containing speech links
            speech_section = soup.find('div', id="article")
            if speech_section:
                content = "\n".join([p.get_text(separator=' ') for p in speech_section.find_all('p')])
                file_name = f"data/{person}/{url_date}.txt"

                with open(file_name, 'w', encoding='utf-8') as file:
                    for line in content:
                        file.write(str(line))

                    file.close()
            else:
                # No speeches found for the current date, continue to the next date
                pass

        # Move to the next date
        current_date += timedelta(days=1)

    return speeches

if __name__ == "__main__":
    scrape_speeches("powell", datetime(2018, 2, 13))
