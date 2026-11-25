"""Scrape standalone Bachelor of Science programs from the CSUF catalog."""

import re
from pathlib import Path
import unicodedata

import scrapy


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_INPUT_DIR = PROJECT_ROOT / "docs" / "degree_html" / "CSUF"


class DegreeProgramsSpider(scrapy.Spider):
    name = "degree_programs"
    custom_settings = {
        "FEEDS": {
            str(PROJECT_ROOT / "data" / "raw" / "degree_programs.json"): {
                "format": "json",
                "overwrite": True,
                "encoding": "utf8",
            }
        }
    }

    async def start(self):
        """Parse locally saved program pages; do not request the live catalog."""
        input_dir = Path(self.input_dir).expanduser()
        if not input_dir.is_absolute():
            input_dir = Path.cwd() / input_dir
        pages = sorted(input_dir.glob("*.html"))
        if not pages:
            self.logger.warning("No HTML files found in %s", input_dir)

        for page in pages:
            yield scrapy.Request(
                page.as_uri(),
                callback=self.parse_program,
                cb_kwargs={"university": self.university},
            )

    def parse_program(self, response, university):
        title = response.css("#acalog-page-title::text").get()
        if not title:
            title = response.css("title::text").get(default="")
            title = re.sub(r"^Program:\s*|\s*-\s*California State University Fullerton$", "", title)
        title = " ".join(title.split())

        # Keep only standalone B.S. records, even if unrelated HTML files are
        # later added to this directory.
        if "concentration" in title.casefold() or not re.search(
            r"(?:,|\s)B\.S\.$", title
        ):
            return

        major = re.sub(r"(?:,|\s)B\.S\.$", "", title).strip().rstrip(",")
        catalog_name = " ".join(
            response.css("#acalog-catalog-name::text").getall()
        ).strip()
        catalog_year_match = re.search(r"(\d{4}-\d{4})", catalog_name)
        catalog_year = catalog_year_match.group(1) if catalog_year_match else None

        total_units = None
        for heading in response.xpath("//h2 | //h3 | //h4 | //h5 | //h6"):
            heading_text = " ".join(heading.xpath(".//text()").getall())
            total_match = re.search(r"total\s*\((\d+)\s*units?\)", heading_text, re.I)
            if total_match:
                total_units = int(total_match.group(1))

        concentrations = []
        concentration_headings = response.xpath(
            '//*[self::h2 or self::h3 or self::h4 or self::h5 or self::h6]'
            '[contains(translate(normalize-space(string(.)), '
            '"ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "concentration")]'
        )
        for heading in concentration_headings:
            for link in heading.xpath('following-sibling::ul[1]//a'):
                concentration = " ".join(link.xpath(".//text()").getall())
                concentration = " ".join(concentration.replace("\xa0", " ").split())
                concentration = re.sub(
                    rf"^{re.escape(major)}\s*,?\s*B\.S\.\s*,?\s*",
                    "",
                    concentration,
                    flags=re.I,
                )
                concentration = re.sub(r"\s+Concentration$", "", concentration, flags=re.I)
                if concentration and concentration not in concentrations:
                    concentrations.append(concentration)

        core_courses = []
        elective_courses = []
        for course_link in response.css("li.acalog-course a"):
            label = course_link.attrib.get("aria-label", "")
            course_text = " ".join(course_link.xpath(".//text()").getall())
            course_text = " ".join(course_text.replace("\xa0", " ").split())
            if not course_text:
                course_text = re.sub(r"^View course details for\s*", "", label).strip()

            course_match = re.match(
                r"^([A-Z]{2,6}\s+\d{3}[A-Z]?)\s*[-–]\s*(.+?)\s*(?:\(\s*\d+(?:\s*[-–]\s*\d+)?\s*\))?$",
                course_text,
            )
            if not course_match:
                continue

            previous_heading = course_link.xpath(
                "preceding::*[self::h2 or self::h3 or self::h4 or self::h5 or self::h6][1]"
            )
            section = " ".join(previous_heading.xpath(".//text()").getall()).casefold()
            destination = elective_courses if "elective" in section else core_courses
            course_name = f"{course_match.group(1)} - {course_match.group(2).strip()}"
            if course_name not in destination:
                destination.append(course_name)

        def make_slug(value):
            value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
            return re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()

        school_slug = make_slug(university)
        major_slug = make_slug(major)
        year_slug = catalog_year or "unknown"
        source_url = response.xpath(
            '//comment()[contains(., "saved from url=")]/text()'
        ).re_first(r"saved from url=\(\d+\)(https?://[^\s]+)")
        
        yield {
            "id": f"{school_slug}-bs-{major_slug}-{year_slug}",
            "record_type": "degree_program",
            "university": university,
            "major": major,
            "degree": "Bachelor of Science",
            "catalog_year": catalog_year,
            "total_units": total_units,
            "core_courses": core_courses,
            "elective_courses": elective_courses,
            "concentrations": concentrations,
            "source_url": source_url,
        }

    def __init__(
        self,
        input_dir=str(DEFAULT_INPUT_DIR),
        university="California State University, Fullerton",
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.input_dir = input_dir
        self.university = university
