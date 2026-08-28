import yaml

from pathlib import Path

from django.core.management.base import BaseCommand

from keyboard_tracker.models import Specification


class Command(BaseCommand):

    help = (
        "Synchronise specifications from "
        "specs.yaml"
    )


    def handle(self, *args, **options):

        file_path = (
            Path(__file__)
            .resolve()
            .parents[2]
            / "specs.yaml"
        )

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            data = yaml.safe_load(file)


        category_mapping = {
            "features": "feature",
            "sizes": "size",
            "switches": "switch",
        }


        for yaml_category, category in (
            category_mapping.items()
        ):

            specifications = data.get(
                yaml_category,
                {}
            )


            for slug, specification_data in (
                specifications.items()
            ):

                name = specification_data["name"]


                specification, created = (
                    Specification.objects.update_or_create(

                        slug=slug,

                        category=category,

                        defaults={
                            "name": name
                        }
                    )
                )


                if created:

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Created: "
                            f"{specification.name}"
                        )
                    )

                else:

                    self.stdout.write(
                        f"Updated: "
                        f"{specification.name}"
                    )


        self.stdout.write(
            self.style.SUCCESS(
                "Specification sync complete."
            )
        )