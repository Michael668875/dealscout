import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import time
import os


BASE_URL = "https://keybumps.com"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def get_soup(url):

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=20
    )

    response.raise_for_status()

    return BeautifulSoup(
        response.text,
        "html.parser"
    )


def get_keyboard_list():

    url = (
        BASE_URL +
        "/mechanical-keyboard-catalog.html"
    )

    soup = get_soup(url)

    keyboards = []


    for a in soup.select("a[href]"):

        href = a["href"]

        if "/keyboard/" not in href:
            continue

        name = a.get_text(
            " ",
            strip=True
        )

        keyboards.append(
            {
                "catalog_name": name,
                "url": urljoin(
                    BASE_URL,
                    href
                )
            }
        )


    df = pd.DataFrame(keyboards)


    df.drop_duplicates(
        subset=["url"],
        inplace=True
    )


    return df



def split_title(title, brand):

    title = title.replace(
        "Mechanical Keyboard",
        ""
    ).strip()


    if brand:

        if title.lower().startswith(
            brand.lower()
        ):

            title = title[
                len(brand):
            ].strip()


    return title




def scrape_keyboard(url):

    soup = get_soup(url)


    data = {
        "url": url
    }


    # Title

    h1 = soup.find("h1")

    if h1:

        data["title"] = h1.get_text(
            " ",
            strip=True
        )


    # Brand

    brand = soup.select_one(
        ".taglist a"
    )


    if brand:

        data["brand"] = brand.get_text(
            strip=True
        )


    else:

        data["brand"] = None



    # Specifications table

    table = soup.select_one(
        "table.spec-table"
    )


    if table:

        for row in table.select("tr"):

            cells = row.select(
                "th, td"
            )


            if len(cells) == 2:

                key = cells[0].get_text(
                    " ",
                    strip=True
                )


                value = cells[1].get_text(
                    " ",
                    strip=True
                )


                data[key] = value



    # clean model name

    data["model"] = split_title(
        data.get("title", ""),
        data.get("brand", "")
    )


    return data





def main():

    print("Getting keyboard list...")

    keyboards = get_keyboard_list()


    print(
        f"Found {len(keyboards)} keyboards"
    )


    results = []


    # resume support

    output_file = "keyboard_models.csv"


    if os.path.exists(output_file):

        old = pd.read_csv(output_file)

        results = old.to_dict(
            "records"
        )

        done = set(
            old["url"]
        )

        print(
            f"Resuming. Already have {len(done)}"
        )

    else:

        done = set()



    for index, row in keyboards.iterrows():


        url = row["url"]


        if url in done:
            continue


        print(
            f"{len(results)+1}/{len(keyboards)}",
            row["catalog_name"]
        )


        try:

            data = scrape_keyboard(
                url
            )

            results.append(
                data
            )


        except Exception as e:

            print(
                "FAILED:",
                url,
                e
            )


        # save regularly

        if len(results) % 25 == 0:

            pd.DataFrame(results).to_csv(
                output_file,
                index=False
            )

            print(
                "Saved progress"
            )


        time.sleep(0.5)



    df = pd.DataFrame(results)

    df.to_csv(
        output_file,
        index=False
    )


    print(
        "DONE"
    )

    print(
        "Saved:",
        len(df)
    )



if __name__ == "__main__":
    main()