import re
import yaml

from pathlib import Path

from keyboard_tracker.models import (
    Listing,
    Specs,
    Specification,
    SpecValue,
    CanonBrand,
)


def load_specs_yaml():

    file_path = (
        Path(__file__)
        .resolve()
        .parents[1]
        / "specs.yaml"
    )

    if not file_path.exists():

        raise FileNotFoundError(
            f"Could not find specs.yaml at: {file_path}"
        )

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        return yaml.safe_load(file)


def normalise(value):

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


def matches(title, value):

    title = normalise(title)
    value = normalise(value)

    if not value:
        return False

    pattern = (
        r"(?<!\w)"
        + re.escape(value)
        + r"(?!\w)"
    )

    return re.search(
        pattern,
        title
    ) is not None


def specification_matches(
    title,
    slug,
    specification_data
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

    for value in possible_values:

        if matches(title, value):
            return True

    return False


def add_specification(
    specs,
    specification
):

    if specification is None:
        return

    SpecValue.objects.get_or_create(
        specs=specs,
        specification=specification
    )


def parse_category(
    title,
    specs,
    yaml_data,
    category,
    yaml_category
):

    specifications = yaml_data.get(
        yaml_category,
        {}
    )

    for slug, specification_data in specifications.items():

        if not specification_matches(
            title,
            slug,
            specification_data
        ):
            continue

        specification = (
            Specification.objects.filter(
                slug=slug,
                category=category
            )
            .first()
        )

        if specification is None:
            continue

        add_specification(
            specs,
            specification
        )


def parse_keyboard_specs():

    yaml_data = load_specs_yaml()

    listings = Listing.objects.filter(
        status="ACTIVE"
    )

    brands = CanonBrand.objects.all()

    for listing in listings:

        title = listing.title

        specs, created = Specs.objects.get_or_create(
            listing=listing
        )

        # -------------------------
        # BRAND
        # -------------------------

        title_lower = title.lower()

        for brand in brands:

            if brand.name.lower() in title_lower:

                specs.brand = brand
                specs.save(
                    update_fields=["brand"]
                )

                break

        # -------------------------
        # REMOVE OLD SPEC VALUES
        # -------------------------
        #
        # This makes the parser safe to run
        # repeatedly. Existing relationships
        # are rebuilt from the current title.
        #

        SpecValue.objects.filter(
            specs=specs
        ).delete()

        # -------------------------
        # FEATURES
        # -------------------------

        parse_category(
            title,
            specs,
            yaml_data,
            "feature",
            "features"
        )

        # -------------------------
        # SIZES
        # -------------------------

        parse_category(
            title,
            specs,
            yaml_data,
            "size",
            "sizes"
        )

        # -------------------------
        # SWITCHES
        # -------------------------

        parse_category(
            title,
            specs,
            yaml_data,
            "switch",
            "switches"
        )