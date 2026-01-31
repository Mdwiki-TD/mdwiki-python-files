import logging
import time

import requests
from apis import cat_cach

logger = logging.getLogger(__name__)


all_pages = cat_cach.from_cache()

logger.info(f"Found {len(all_pages)} pages")

success_count = 0
failure_count = 0

for title in all_pages:
    url = f"https://medwiki.toolforge.org/new_html/index.php?title={title}"
    try:
        response = requests.get(url, timeout=30)

        # Check HTTP status code
        if response.status_code == 200:
            logger.info(f"✓ SUCCESS: {title} - Status: {response.status_code}")
            success_count += 1
            # Process successful response
            # content = response.text
        else:
            logger.info(f"✗ FAILED: {title} - Status: {response.status_code}")
            failure_count += 1

        # Alternative: Use raise_for_status() to raise exception for 4xx/5xx
        response.raise_for_status()

        time.sleep(0.5)  # Rate limiting

    except requests.exceptions.Timeout:
        logger.info(f"✗ TIMEOUT: {title}")
        failure_count += 1
    except requests.exceptions.ConnectionError:
        logger.info(f"✗ CONNECTION ERROR: {title}")
        failure_count += 1
    except requests.exceptions.HTTPError as e:
        logger.info(f"✗ HTTP ERROR: {title} - {e}")
        failure_count += 1
    except requests.RequestException as e:
        logger.info(f"✗ REQUEST ERROR: {title} - {e}")
        failure_count += 1

logger.info(f"\nSummary: {success_count} successful, {failure_count} failed")
