import requests
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime, timedelta

def fetch_g2_reviews(company_name, start_date, end_date):
    """Fetch reviews from G2 with pagination and date range optimization."""
    company = company_name.replace(" ", "-")
    base_url = f"https://www.g2.com/products/{company}/reviews"
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9,hi;q=0.8',
        'cache-control': 'max-age=0',
        'cookie': 'events_distinct_id=f2f0bedf-56ac-4c56-9e2d-e046fd8e2797; _gcl_au=1.1.2081274803.1737791778; zfm_cnt_ck_id=bbtzn30ls981737791778028; sp=746b2419-402d-4eff-ad54-237bf2f78269; osano_consentmanager_uuid=3e6ce4c5-0364-4e76-802c-5d25e1a74321; osano_consentmanager=901AGX_AnpN8qMUFBlkti9841-u-d8mLDdhOFptDhwWoAdpl7_va3FZ9AvzOWvLxcKrfeVFsilydDzMle8qXEKE3QtCnf9RfDdbUz92VXO7et18RhvBr0GHKAQHLCokVMRvzWWB1q0P5eWlWZMAOKXpVsRS2bspIstH68bfk18DmePLItvPZTGvWIjfS4JzEOq3hlGvVtoZngEbIMZU9qZQOXe3EDL-ena08Ye73r4nevc4U9N6NVMpmh2q6WyPrjTQ6iGqRTvvE2bVpp7x_rg3kUwUPogOrTK1Ut5wF-mISBNphfa5rXU_wL2NlqgGzhDjujrwYbgg=; zfm_app_9f3XVc=show; zfm_app_S3V5ee=show; zfm_app_3SDj9c=hide; zfm_app_u1h4JN=show; _fbp=fb.1.1737791780658.19896388274093281; __adroll_fpc=2a5d1bcf072d89294717856e7d1755e3-1737791780671; loginNudgeShown=true; zfm_beh_u1h4JN=hide; block%3Asidebar-default=1; amplitude_session=1738149164891; _g2_session_id=15361968c4967bd26c5ed198f72e5711; __cf_bm=BjKuzo1h1oovX9QmOv7Fc6MJoCg4YPnCrYL_sKhXbk8-1738149165-1.0.1.1-Ok3uffzgeU2K9e4QF9.hULXNzLG.XcdVeR_tFKZAVJbwzc5AJ8RAnMKhQqgxJsFduY_O_qWkqZ7QbBiMzHa8WA; _sp_ses.6c8b=*; cf_clearance=pgbRrHLjkxWATKhk1MLiXdAp0ZfXYUrRMbTYHmsPkoU-1738149166-1.2.1.1-WYFciLxmpdZW8RJJfWKocasPcKlohagqjJdrm0twsxKOVPDDZ04jJGhRp4It6jYMlZFf597NpOpS7hZdfXeGA4bki5guRZTW6xXoGrQiK3UxWeooQz0CpDsS8dyYCgY_dPBtOFaK60.rcjq7..BuDZ6MJjG8OkzeS.ipl3qiVvQukTcUdpkSerpfdh40FsW0RS6ebrdp.Irs7wuCegE3lzwu8A_XM_YFdJQ6xtL87vz4k4IrMoh8w44LJ1s73bGMaJGa6.KwTfq8nGBT1iL4CikJUZlBEJJeHlioYaXHRng; zfm_usr_sess_ck_id=auhdpv9wgif1738149165633; _gid=GA1.2.1592813140.1738149166; _ga_MFZ5NDXZ5F=GS1.1.1738149165.6.1.1738149406.51.0.0; _ga=GA1.2.1299734727.1737791778; AWSALB=Ddmwg3q/Y+I8HSaTfdI0I2tFVdi/rjee5UNxFb+fJOwhVlUlwiwFMihVOszfZizOG1ZpQ42UBJWybVcs8QfdNxBmAip05wC4INsfQqaYFmtxMvWvUF2jC8VhkOHT; AWSALBCORS=Ddmwg3q/Y+I8HSaTfdI0I2tFVdi/rjee5UNxFb+fJOwhVlUlwiwFMihVOszfZizOG1ZpQ42UBJWybVcs8QfdNxBmAip05wC4INsfQqaYFmtxMvWvUF2jC8VhkOHT; __ar_v4=C6MKFN32KVBHZAS4DKYVVW%3A20250124%3A14%7CEEPCTRZ5RNC6ZCBB2PJM4J%3A20250124%3A14%7CNBMTYK27EJFT3GYAV7FM56%3A20250124%3A14; datadome=uf2IF0zD9_82u0JAQPddbMMHICKTQSotK1Bl3xsAkzFLGStsrvKWXKrVFCob~RXQEHKpc91fDfVoVLZZoR6g2J2ZLt4jxWehOdTf7Uj2cdvGxQBDWYvs5NIP3~WJQSCs; _gat=1; _sp_id.6c8b=e65c48e1-64d7-49c0-bf70-60c26e03d7dd.1737791777.7.1738149703.1737823959.28413533-28b8-4dee-a557-c8d9e1ae046a.a45b289c-921c-48ab-943c-f74b0ff1d4fd.353fe8b2-b254-4854-8f5a-6224532621a9.1738149165575.32; datadome=A9fbrOWVHaGQj3_YOMky7E5WIWDAGLjfL6w78WsWdxztjtMMZ4Blvctpbt4dKTu8Z~v3T31OrZaTd1X4f6C0Bpu9rfl5N776WcN3CTXJRhha2jxOKEGChmjpAiQFKVhs; AWSALB=t2qiOt4zfSvGqwfJaTt7lrULubDcMfxXrLNIrZK81hjIYTnre5voGh6NkRwMzXZBZT1qvIJeR84CUnrSr44hqFtV/ZNKC3jLMK8AugdmQ8rIH/ehnKD+mZdRlLT1; AWSALBCORS=t2qiOt4zfSvGqwfJaTt7lrULubDcMfxXrLNIrZK81hjIYTnre5voGh6NkRwMzXZBZT1qvIJeR84CUnrSr44hqFtV/ZNKC3jLMK8AugdmQ8rIH/ehnKD+mZdRlLT1',
        'referer': f"https://www.g2.com/products/{company}/reviews",
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'
    }

    reviews = []
    page = 1

    while True:
        url = f"{base_url}?page={page}"
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"Failed to fetch G2 reviews for {company}. Status code: {response.status_code}")
            break

        soup = BeautifulSoup(response.content, 'html.parser')
        review_elements = soup.find_all('div', {'itemprop': 'review'})

        if not review_elements:
            print(f"No more reviews found on page {page}. Stopping pagination.")
            break

        # Track if any review is within the date range
        found_within_date_range = False

        for review in review_elements:
            date_element = review.find('meta', {'itemprop': 'datePublished'})
            if date_element:
                review_date = datetime.strptime(date_element.get('content'), "%Y-%m-%d")
                if review_date < start_date:
                    continue  # Skip reviews older than the start date
                elif review_date > end_date:
                    continue  # Skip reviews newer than the end date
                else:
                    found_within_date_range = True  # Mark that we found a valid review

                title = review.find('div', {'itemprop': 'name'}).text.strip() if review.find('div', {'itemprop': 'name'}) else "No Title"
                description = review.find('div', {'itemprop': 'reviewBody'}).text.strip() if review.find('div', {'itemprop': 'reviewBody'}) else "No Description"
                reviewer_name = review.find('meta', {'itemprop': 'name'}).get('content') if review.find('meta', {'itemprop': 'name'}) else "Anonymous"
                rating = review.find('meta', {'itemprop': 'ratingValue'}).get('content') if review.find('meta', {'itemprop': 'ratingValue'}) else "No Rating"

                reviews.append({
                    "title": title,
                    "description": description,
                    "date": review_date.strftime('%Y-%m-%d'),
                    "reviewer_name": reviewer_name,
                    "rating": rating
                })

        # If no reviews on this page are within the date range, stop pagination
        if not found_within_date_range:
            print(f"No reviews within the date range found on page {page}. Stopping pagination.")
            break

        page += 1

    return reviews

def parse_relative_date(relative_date):
    """Convert relative date text like '5 days ago' to an actual date."""
    now = datetime.now()
    parts = relative_date.split()

    try:
        if "days" in parts or "day" in parts:
            days = int(parts[0])
            return now - timedelta(days=days)
        elif "weeks" in parts or "week" in parts:
            weeks = int(parts[0])
            return now - timedelta(weeks=weeks)
        elif "months" in parts or "month" in parts:
            months = int(parts[0])
            return now - timedelta(days=30 * months)
        elif "years" in parts or "year" in parts:
            years = int(parts[0])
            return now - timedelta(days=365 * years)
        elif "last" in parts:
            if "month" in parts:
                return now - timedelta(days=30)
            elif "year" in parts:
                return now - timedelta(days=365)
            elif "week" in parts:
                return now - timedelta(weeks=1)
        else:
            return None
    except ValueError:
        return None

def fetch_capterra_reviews(company_name, start_date, end_date):
    """Fetch reviews from Capterra."""
    search_url = "https://www.capterra.in/"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome()

    try:
        driver.get(search_url)
        time.sleep(5)

        search_box = driver.find_element(By.ID, "homeSearch")
        search_box.send_keys(company_name)
        search_box.send_keys("\n")
        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        company_links = soup.find_all('a', class_='entry')
        company_link = None

        for link in company_links:
            title = link.find('span', class_='h4 fw-bold')
            if title and company_name.lower() in title.text.lower():
                company_link = link
                break

        if not company_link:
            print(f"Could not find the company '{company_name}' in search results.")
            return []

        href = company_link['href']
        driver.get(f"https://www.capterra.in{href}")
        time.sleep(5)

        reviews = []
        while True:
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            for review in soup.find_all('div', class_='review-card'):
                date_text = review.find('span', class_='ms-2').text.strip() if review.find('span', class_='ms-2') else "No Date"
                date = parse_relative_date(date_text)

                if not date or date < start_date or date > end_date:
                    continue

                title = review.find('h3', class_='h5 fw-bold').text.strip() if review.find('h3', class_='h5 fw-bold') else "No Title"
                description = review.find('p', {'class': 'review-text'}).text.strip() if review.find('p', {'class': 'review-text'}) else "No Description"
                reviewer_name = review.find('div', class_='h5 fw-bold mb-2').text.strip() if review.find('div', class_='h5 fw-bold mb-2') else "Anonymous"
                rating = review.find('span', class_='ms-1').text.strip() if review.find('span', class_='ms-1') else "No Rating"

                reviews.append({
                    "title": title,
                    "description": description,
                    "date": date.strftime('%Y-%m-%d'),
                    "reviewer_name": reviewer_name,
                    "rating": rating
                })

            next_button = soup.find('a', class_='pagination-next')
            if next_button and 'href' in next_button.attrs:
                driver.get(next_button['href'])
                time.sleep(5)
            else:
                break

        return reviews

    finally:
        driver.quit()

def fetch_trustpilot_reviews(company_name, start_date, end_date):
    """Fetch reviews from Trustpilot with pagination and date range optimization."""
    search_url = "https://www.trustpilot.com/"

    # Selenium setup for JavaScript rendering
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome()

    try:
        driver.get(search_url)
        time.sleep(5)

        # Search for the company
        search_box = driver.find_element(By.NAME, "query")
        search_box.send_keys(company_name)
        search_box.send_keys("\n")
        time.sleep(5)

        # Parse search results and find the best match
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        company_links = soup.find_all('a', {'data-business-unit-card-link': 'true'})
        company_link = None

        for link in company_links:
            title = link.find('p', class_='typography_heading-xs__osRhC')
            if title and company_name.lower() in title.text.lower():
                company_link = link
                break

        if not company_link:
            print(f"Could not find the company '{company_name}' in search results.")
            return []

        # Navigate to the company's review page
        href = company_link['href']
        driver.get(f"https://www.trustpilot.com{href}")
        time.sleep(5)

        reviews = []
        while True:
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Parse all reviews on the current page
            found_within_date_range = False
            for review in soup.find_all('article', {'class': 'styles_reviewCard__6j0RQ'}):
                # Extract review date and filter by range
                date_element = review.find('time')
                if date_element:
                    date = datetime.strptime(date_element['datetime'].split('T')[0], '%Y-%m-%d')
                    if date < start_date:
                        continue  # Skip reviews older than the start date
                    elif date > end_date:
                        continue  # Skip reviews newer than the end date
                    else:
                        found_within_date_range = True  # Mark that we found a valid review
                else:
                    continue

                # Extract review details
                title = review.find('h2', {'data-service-review-title-typography': 'true'}).text.strip() if review.find('h2', {'data-service-review-title-typography': 'true'}) else "No Title"
                description = review.find('p', {'data-service-review-text-typography': 'true'}).text.strip() if review.find('p', {'data-service-review-text-typography': 'true'}) else "No Description"
                reviewer_name = review.find('span', {'data-consumer-name-typography': 'true'}).text.strip() if review.find('span', {'data-consumer-name-typography': 'true'}) else "Anonymous"
                rating_element = review.find('div', class_='star-rating_starRating__sdbkn')
                rating = rating_element.find('img')['alt'] if rating_element else "No Rating"

                reviews.append({
                    "title": title,
                    "description": description,
                    "date": date.strftime('%Y-%m-%d'),
                    "reviewer_name": reviewer_name,
                    "rating": rating
                })

            # Stop pagination if no reviews on the page are within the date range
            if not found_within_date_range:
                print(f"No reviews within the date range found on the current page. Stopping pagination.")
                break

            # Check for a "Next" button and navigate to the next page
            next_button = soup.find('a', {'data-pagination-button-next-link': 'true'})
            if next_button and 'href' in next_button.attrs:
                driver.get(f"https://www.trustpilot.com{next_button['href']}")
                time.sleep(5)
            else:
                print(f"No more pages of reviews. Stopping pagination.")
                break

        return reviews

    finally:
        driver.quit()

if __name__ == "__main__":
    source = input("Enter source (g2/capterra/trustpilot): ").lower()

    if source in ["g2", "capterra", "trustpilot"]:
        company_name = input("Enter company name (e.g., zoom): ").lower()
        start_date = datetime.strptime(input("Enter start date (YYYY-MM-DD): "), "%Y-%m-%d")
        end_date = datetime.strptime(input("Enter end date (YYYY-MM-DD): "), "%Y-%m-%d")

        if source == "g2":
            reviews = fetch_g2_reviews(company_name, start_date, end_date)
        elif source == "capterra":
            reviews = fetch_capterra_reviews(company_name, start_date, end_date)
        elif source == "trustpilot":
            reviews = fetch_trustpilot_reviews(company_name, start_date, end_date)

        output_file = f"{source}_reviews.json"
        with open(output_file, "w") as f:
            json.dump(reviews, f, indent=4)
        print(f"Reviews saved to {output_file}.")
    else:
        print("Invalid source provided. Supported sources are g2, capterra, and trustpilot.")
