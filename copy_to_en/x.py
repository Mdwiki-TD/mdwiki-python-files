import requests
import time
from apis import cat_cach

all_pages = cat_cach.from_cache()

print(f"Found {len(all_pages)} pages")

success_count = 0
failure_count = 0

for title in all_pages:
    url = f"https://medwiki.toolforge.org/new_html/index.php?title={title}"
    try:
        response = requests.get(url, timeout=30)

        # Check HTTP status code
        if response.status_code == 200:
            print(f"✓ SUCCESS: {title} - Status: {response.status_code}")
            success_count += 1
            # Process successful response
            # content = response.text
        else:
            print(f"✗ FAILED: {title} - Status: {response.status_code}")
            failure_count += 1

        # Alternative: Use raise_for_status() to raise exception for 4xx/5xx
        response.raise_for_status()

        time.sleep(0.5)  # Rate limiting

    except requests.exceptions.Timeout:
        print(f"✗ TIMEOUT: {title}")
        failure_count += 1
    except requests.exceptions.ConnectionError:
        print(f"✗ CONNECTION ERROR: {title}")
        failure_count += 1
    except requests.exceptions.HTTPError as e:
        print(f"✗ HTTP ERROR: {title} - {e}")
        failure_count += 1
    except requests.RequestException as e:
        print(f"✗ REQUEST ERROR: {title} - {e}")
        failure_count += 1

print(f"\nSummary: {success_count} successful, {failure_count} failed")
