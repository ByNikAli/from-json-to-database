import json
from datetime import datetime
from django.core.management.base import BaseCommand
from dashboard.models import DashboardData

class Command(BaseCommand):
    help = 'Load JSON data into the DashboardData model'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to the JSON file')

    def handle(self, *args, **kwargs):
        json_file = kwargs['json_file']

        try:
            with open(json_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File not found: {json_file}"))
            return
        except json.JSONDecodeError as e:
            self.stdout.write(self.style.ERROR(f"JSON decoding error: {e}"))
            return
        
        for item in data:
            # Extract data from JSON
            end_year = item.get('end_year', '')
            if not end_year:
                end_year = 0
            elif not isinstance(end_year, (int, float)):
                intensity = 0
            intensity = item.get('intensity', 0)
            
            # Check if intensity is not empty and is numeric
            if not intensity:
                intensity = 0
            elif not isinstance(intensity, (int, float)):
                intensity = 0
            sector = item.get('sector', '')
            topic = item.get('topic', '')
            insight = item.get('insight', '')
            url = item.get('url', '')
            region = item.get('region', '')
            start_year = item.get('start_year', '')
            if not start_year:
                start_year = 0
            elif not isinstance(start_year, (int, float)):
                intensity = 0
            impact = item.get('impact', '')
            added = item.get('added', '')
            published = item.get('published', '')
            country = item.get('country', '')
            relevance = item.get('relevance', 0)
            if not relevance:
                relevance = 0
            elif not isinstance(relevance, (int ,float)):
                relevance = 0
            pestle = item.get('pestle', '')
            source = item.get('source', '')
            title = item.get('title', '')
            likelihood = item.get('likelihood', 0)
            if not likelihood:
                likelihood = 0
            elif not isinstance(likelihood, (int, float)):
                likelihood = 0            


            try:
                # Parse and convert the 'added' and 'published' datetime strings
                added = datetime.strptime(item.get('added', ''), '%B, %d %Y %H:%M:%S')
                published = datetime.strptime(item.get('published', ''), '%B, %d %Y %H:%M:%S')
            except ValueError:
                self.stdout.write(self.style.ERROR(f"Invalid datetime format for item: {item}"))
                continue

            # Create the DashboardData object here
            DashboardData.objects.create(
                end_year=end_year,
                intensity=intensity,
                sector=sector,
                topic=topic,
                insight=insight,
                url=url,
                region=region,
                start_year=start_year,
                impact=impact,
                added=added,
                published=published,
                country=country,
                relevance=relevance,
                pestle=pestle,
                source=source,
                title=title,
                likelihood=likelihood
            )

            self.stdout.write(self.style.SUCCESS(f"Successfully loaded data for '{title}'"))
