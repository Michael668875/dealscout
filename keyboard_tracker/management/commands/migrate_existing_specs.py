# USE THIS TO MIGRATE EXISTING SPECS FIELDS TO THE NEW SCHEMA

import re
import yaml

from pathlib import Path

from django.core.management.base import BaseCommand

from keyboard_tracker.models import (
    Specs,
    Specification,
    SpecValue,
)


class Command(BaseCommand):

    help = (
        "Migrates existing Specs fields into "
        "Specification and SpecValue records."
    )


    def normalise(self, value):

        if value is None:
            return ""

        value = str(value).lower().strip()

        value = re.sub(
            r"[-_]",
            " ",
            value
        )

        value = re.sub(
            r"\s+",
            " ",
            value
        )

        return value


    def load_yaml(self):

        file_path = (
            Path(__file__)
            .resolve()
            .parents[2]
            / "specs.yaml"
        )

        if not file_path.exists():

            raise FileNotFoundError(
                f"Could not find specs.yaml at: "
                f"{file_path}"
            )

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return yaml.safe_load(file)


    def find_specification(
        self,
        value,
        category,
        yaml_data
    ):

        normalised_value = self.normalise(
            value
        )

        category_mapping = {
            "feature": "features",
            "size": "sizes",
            "switch": "switches",
        }

        yaml_category = category_mapping[
            category
        ]

        specifications = yaml_data.get(
            yaml_category,
            {}
        )

        for slug, specification_data in (
            specifications.items()
        ):

            possible_values = [
                slug,
                specification_data.get(
                    "name",
                    ""
                ),
            ]

            possible_values.extend(
                specification_data.get(
                    "aliases",
                    []
                )
            )

            for possible_value in possible_values:

                if (
                    self.normalise(
                        possible_value
                    )
                    == normalised_value
                ):

                    return (
                        Specification.objects.filter(
                            slug=slug,
                            category=category
                        )
                        .first()
                    )

        return None


    def add_specification(
        self,
        specs,
        specification
    ):

        if specification is None:
            return False

        _, created = (
            SpecValue.objects.get_or_create(
                specs=specs,
                specification=specification
            )
        )

        return created


    def handle(self, *args, **options):

        yaml_data = self.load_yaml()

        feature_fields = [
            "low_profile",
            "hall_effect",
            "optical",
            "hot_swap",
            "gasket_mount",
            "knob",
            "wireless",
            "bluetooth",
            "qmk",
            "via",
            "iso",
            "ansi",
            "barebones",
            "rgb",
        ]


        created_count = 0
        processed_count = 0


        all_specs = Specs.objects.all()


        self.stdout.write(
            f"Found {all_specs.count()} "
            f"Specs records."
        )


        for specs in all_specs:

            processed_count += 1

            self.stdout.write(
                f"\nProcessing Listing ID "
                f"{specs.listing_id}"
            )


            # -------------------------
            # BOOLEAN FEATURES
            # -------------------------

            for field_name in feature_fields:

                if getattr(
                    specs,
                    field_name,
                    False
                ):

                    specification = (
                        Specification.objects.filter(
                            slug=field_name,
                            category="feature"
                        )
                        .first()
                    )

                    if specification is None:

                        self.stdout.write(
                            self.style.WARNING(
                                f"  Missing feature "
                                f"Specification: "
                                f"{field_name}"
                            )
                        )

                        continue


                    created = (
                        self.add_specification(
                            specs,
                            specification
                        )
                    )


                    if created:

                        created_count += 1

                        self.stdout.write(
                            self.style.SUCCESS(
                                f"  Added feature: "
                                f"{specification.name}"
                            )
                        )


            # -------------------------
            # LAYOUT SIZE
            # -------------------------

            if specs.layout_size:

                specification = (
                    self.find_specification(
                        specs.layout_size,
                        "size",
                        yaml_data
                    )
                )


                if specification:

                    created = (
                        self.add_specification(
                            specs,
                            specification
                        )
                    )


                    if created:

                        created_count += 1

                        self.stdout.write(
                            self.style.SUCCESS(
                                f"  Added size: "
                                f"{specification.name}"
                            )
                        )

                else:

                    self.stdout.write(
                        self.style.WARNING(
                            f"  Could not match size: "
                            f"{specs.layout_size}"
                        )
                    )


            # -------------------------
            # SWITCH TYPE
            # -------------------------

            if specs.switch_type:

                specification = (
                    self.find_specification(
                        specs.switch_type,
                        "switch",
                        yaml_data
                    )
                )


                if specification:

                    created = (
                        self.add_specification(
                            specs,
                            specification
                        )
                    )


                    if created:

                        created_count += 1

                        self.stdout.write(
                            self.style.SUCCESS(
                                f"  Added switch: "
                                f"{specification.name}"
                            )
                        )

                else:

                    self.stdout.write(
                        self.style.WARNING(
                            f"  Could not match switch: "
                            f"{specs.switch_type}"
                        )
                    )


        self.stdout.write("")


        self.stdout.write(
            self.style.SUCCESS(
                "Migration complete."
            )
        )


        self.stdout.write(
            f"Processed: "
            f"{processed_count} Specs records"
        )


        self.stdout.write(
            f"Created: "
            f"{created_count} SpecValue records"
        )