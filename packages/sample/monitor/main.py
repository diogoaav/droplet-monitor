import requests
import time

# Define your DigitalOcean API token
DO_API_TOKEN = 'YOUR_DIGITALOCEAN_API_TOKEN'

# Define the tag name you want to filter droplets by
TAG_NAME = 'your_tag_name'

# Define the Grafana endpoint and API key
GRAFANA_ENDPOINT = 'http://localhost:3000/api/datasources/proxy/YOUR_GRAFANA_DATA_SOURCE_ID/write'
GRAFANA_API_KEY = 'YOUR_GRAFANA_API_KEY'

def fetch_droplets():
    url = f'https://api.digitalocean.com/v2/droplets?tag_name={TAG_NAME}'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {DO_API_TOKEN}'
    }
    response = requests.get(url, headers=headers)
    droplets = response.json().get('droplets', [])
    return droplets

def push_to_grafana(metric_name, value):
    data = f'{metric_name} value={value} {int(time.time())}'
    headers = {
        'Content-Type': 'text/plain',
        'Authorization': f'Bearer {GRAFANA_API_KEY}'
    }
    response = requests.post(GRAFANA_ENDPOINT, headers=headers, data=data)
    if response.status_code != 204:
        print(f'Failed to push metric to Grafana: {response.text}')

def main():
    droplets = fetch_droplets()
    for droplet in droplets:
        droplet_id = droplet['id']
        # Example: Fetch CPU usage metric
        cpu_usage = fetch_cpu_usage(droplet_id)
        # Push CPU usage metric to Grafana
        push_to_grafana(f'droplet.{droplet_id}.cpu_usage', cpu_usage)
        # Repeat similar steps for other metrics (e.g., memory usage, disk usage, etc.)

if __name__ == "__main__":
    main()

