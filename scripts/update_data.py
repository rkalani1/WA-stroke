#!/usr/bin/env python3
"""
Data collection script for Washington State Stroke Neurologists
Combines data from:
1. CMS NPPES (National Provider Identifier) API
2. Washington State Department of Health Physician Database
"""

import json
import requests
import time
from datetime import datetime
from typing import List, Dict, Optional
import os
import sys

# Try geocoding with multiple fallbacks
try:
    from geopy.geocoders import Nominatim
    from geopy.exc import GeocoderTimedOut, GeocoderServiceError
    GEOCODING_AVAILABLE = True
except ImportError:
    GEOCODING_AVAILABLE = False
    print("Warning: geopy not available. Install with: pip install geopy")


class NeurologistDataCollector:
    def __init__(self):
        self.neurologists = []
        self.seen_npis = set()

        if GEOCODING_AVAILABLE:
            self.geolocator = Nominatim(user_agent="wa-stroke-neurologist-map")
        else:
            self.geolocator = None

    def geocode_address(self, address: str, city: str, state: str = "WA", zip_code: str = "") -> Optional[tuple]:
        """Geocode an address to latitude/longitude"""
        if not self.geolocator:
            return None

        # Construct full address
        full_address = f"{address}, {city}, {state} {zip_code}".strip()

        try:
            time.sleep(1)  # Rate limiting for Nominatim
            location = self.geolocator.geocode(full_address, timeout=10)
            if location:
                return (location.latitude, location.longitude)

            # Try without street address
            simple_address = f"{city}, {state} {zip_code}".strip()
            location = self.geolocator.geocode(simple_address, timeout=10)
            if location:
                return (location.latitude, location.longitude)

        except (GeocoderTimedOut, GeocoderServiceError) as e:
            print(f"Geocoding error for {full_address}: {e}")

        return None

    def fetch_nppes_data(self) -> List[Dict]:
        """
        Fetch neurologist data from NPPES API
        NPPES API documentation: https://npiregistry.cms.hhs.gov/api-page
        """
        print("Fetching data from NPPES...")
        neurologists = []

        # Search parameters for stroke/vascular neurologists in Washington
        search_terms = [
            "Vascular Neurology",
            "Neurology",
        ]

        for search_term in search_terms:
            print(f"Searching NPPES for: {search_term}")

            # NPPES API endpoint
            url = "https://npiregistry.cms.hhs.gov/api/"

            params = {
                'version': '2.1',
                'state': 'WA',
                'taxonomy_description': search_term,
                'limit': 200
            }

            try:
                response = requests.get(url, params=params, timeout=30)
                response.raise_for_status()
                data = response.json()

                if 'results' in data and data['results']:
                    print(f"Found {len(data['results'])} providers for {search_term}")

                    for provider in data['results']:
                        npi = provider.get('number')

                        # Skip duplicates
                        if npi in self.seen_npis:
                            continue
                        self.seen_npis.add(npi)

                        # Extract provider information
                        basic = provider.get('basic', {})

                        # Get primary practice address
                        addresses = provider.get('addresses', [])
                        practice_address = None
                        for addr in addresses:
                            if addr.get('address_purpose') == 'LOCATION':
                                practice_address = addr
                                break

                        if not practice_address and addresses:
                            practice_address = addresses[0]

                        # Check if this is a stroke/vascular neurologist
                        taxonomies = provider.get('taxonomies', [])
                        is_vascular_neuro = False
                        specialty_desc = "Neurology"

                        for tax in taxonomies:
                            desc = tax.get('desc', '').lower()
                            if 'vascular' in desc or 'stroke' in desc:
                                is_vascular_neuro = True
                                specialty_desc = tax.get('desc', 'Vascular Neurology')
                                break

                        # Build neurologist record
                        if practice_address:
                            name_parts = []
                            if basic.get('first_name'):
                                name_parts.append(basic['first_name'])
                            if basic.get('middle_name'):
                                name_parts.append(basic['middle_name'])
                            if basic.get('last_name'):
                                name_parts.append(basic['last_name'])

                            full_name = ' '.join(name_parts)

                            # Add credentials
                            if basic.get('credential'):
                                full_name += f", {basic['credential']}"

                            address_line = practice_address.get('address_1', '')
                            if practice_address.get('address_2'):
                                address_line += f" {practice_address['address_2']}"

                            city = practice_address.get('city', '')
                            zip_code = practice_address.get('postal_code', '')

                            # Geocode
                            coords = self.geocode_address(address_line, city, 'WA', zip_code)

                            neuro_data = {
                                'npi': npi,
                                'name': full_name,
                                'credentials': basic.get('credential', ''),
                                'specialty': specialty_desc,
                                'is_vascular_neurology': is_vascular_neuro,
                                'organization': basic.get('organization_name', ''),
                                'address': address_line,
                                'city': city,
                                'state': 'WA',
                                'zip': zip_code,
                                'phone': practice_address.get('telephone_number', ''),
                                'latitude': coords[0] if coords else None,
                                'longitude': coords[1] if coords else None,
                                'source': 'NPPES'
                            }

                            neurologists.append(neuro_data)

                time.sleep(0.5)  # Rate limiting

            except requests.exceptions.RequestException as e:
                print(f"Error fetching from NPPES: {e}")
                continue

        return neurologists

    def fetch_wa_doh_data(self) -> List[Dict]:
        """
        Fetch data from Washington State Department of Health
        Note: This may require web scraping depending on available APIs
        """
        print("Fetching data from WA DOH...")

        # WA DOH Provider Credential Search
        # https://fortress.wa.gov/doh/providercredentialsearch/

        # Note: The WA DOH database may not have a public API.
        # This is a placeholder for potential scraping or manual data entry.
        # You may need to use Selenium or similar tools for actual scraping.

        print("WA DOH scraping not yet implemented - requires manual setup")
        print("Visit: https://fortress.wa.gov/doh/providercredentialsearch/")

        return []

    def collect_all_data(self):
        """Collect data from all sources"""
        print("Starting data collection...")

        # Collect from NPPES
        nppes_data = self.fetch_nppes_data()
        self.neurologists.extend(nppes_data)

        # Collect from WA DOH
        wa_doh_data = self.fetch_wa_doh_data()
        self.neurologists.extend(wa_doh_data)

        print(f"\nTotal neurologists collected: {len(self.neurologists)}")
        print(f"With coordinates: {sum(1 for n in self.neurologists if n.get('latitude'))}")

    def save_data(self, output_file: str = 'data/neurologists.json'):
        """Save collected data to JSON file"""
        output_data = {
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC'),
            'total_count': len(self.neurologists),
            'neurologists': self.neurologists
        }

        # Ensure directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=2)

        print(f"\nData saved to {output_file}")


def main():
    collector = NeurologistDataCollector()
    collector.collect_all_data()
    collector.save_data()

    print("\n✓ Data collection complete!")


if __name__ == '__main__':
    main()
