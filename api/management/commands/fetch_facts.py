from django.core.management.base import BaseCommand
from api.models import AgricKnowledge

class Command(BaseCommand):
    help = 'Seed the database with initial agricultural knowledge facts'

    def handle(self, *args, **options):
        facts = [
            {"title": "Did you know?", "content": "Crop rotation helps improve soil fertility and reduce the risk of pests and diseases."},
            {"title": "Agricultural Fact", "content": "Honeybees play a crucial role in pollinating crops, contributing to the production of many fruits and vegetables."},
            {"title": "Did you know?", "content": "The practice of intercropping involves growing two or more crops together for mutual benefit."},
            {"title": "Interesting Fact", "content": "Cover crops, like clover and rye, help prevent soil erosion and add nutrients to the soil."},
            {"title": "Agricultural Fact", "content": "Ladybugs are natural predators of aphids and can be used for biological pest control."},
            {"title": "Did you know?", "content": "Composting organic waste at the farm can create nutrient-rich compost for plants."},
            {"title": "Agricultural Fact", "content": "Healthy soil is a key component of sustainable agriculture."},
            {"title": "Did you know?", "content": "Drip irrigation systems can significantly reduce water usage in agriculture."},
            {"title": "Interesting Fact", "content": "Pulses, like lentils and chickpeas, enrich the soil by fixing nitrogen."},
            {"title": "Agricultural Fact", "content": "Agroforestry combines trees and shrubs with crops for ecological and economic benefits."},
            {"title": "Did you know?", "content": "The use of cover crops can suppress weed growth and improve soil structure."},
            {"title": "Agricultural Fact", "content": "Certain plants, like marigolds, can be used to repel pests from crops."},
            {"title": "Did you know?", "content": "Crop diversity is essential for building resilience against pests and climate change."},
            {"title": "Interesting Fact", "content": "Aquaponics combines aquaculture and hydroponics for sustainable food production."},
            {"title": "Agricultural Fact", "content": "No-till farming helps retain soil moisture and reduce erosion."},
            {"title": "Did you know?", "content": "Bees are crucial pollinators for many fruit and vegetable crops."},
            {"title": "Agricultural Fact", "content": "Companion planting involves growing different plants together to benefit each other."},
            {"title": "Did you know?", "content": "The practice of grafting can be used to improve plant resistance and yield."},
            {"title": "Interesting Fact", "content": "Vermicomposting uses worms to decompose organic waste into nutrient-rich compost."},
            {"title": "Agricultural Fact", "content": "Certain herbs, like basil and mint, can be effective natural pesticides."},
            {"title": "Did you know?", "content": "Precision agriculture uses technology to optimize crop yields and reduce inputs."},
            {"title": "Agricultural Fact", "content": "Integrated Pest Management (IPM) emphasizes ecological approaches to pest control."},
            {"title": "Did you know?", "content": "Agrotourism promotes farm visits and experiences for the public."},
            {"title": "Interesting Fact", "content": "Soil health is crucial for plant nutrition and overall ecosystem health."},
            {"title": "Agricultural Fact", "content": "Heirloom seeds are traditional varieties that are open-pollinated and often passed down through generations."},
            {"title": "Did you know?", "content": "Green manure involves growing crops that are later incorporated into the soil to improve fertility."},
            {"title": "Agricultural Fact", "content": "Permaculture design principles aim for sustainable and self-sufficient agricultural systems."},
            {"title": "Did you know?", "content": "The use of beneficial insects, like ladybugs, can help control harmful pests."},
            {"title": "Interesting Fact", "content": "Crop rotation can break pest and disease cycles in agriculture."},
            {"title": "Agricultural Fact", "content": "Vertical farming utilizes vertical space for efficient and sustainable crop production."},
            {"title": "Did you know?", "content": "Aquaculture is the farming of fish, shellfish, and aquatic plants in controlled environments."},
            # Add more facts as needed
        ]

        for fact_data in facts:
            AgricKnowledge.objects.create(**fact_data)

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database with agricultural knowledge facts.'))