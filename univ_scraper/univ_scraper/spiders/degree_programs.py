"""Scrape standalone Bachelor of Science programs from the CSUF catalog."""

import re
from pathlib import Path
import unicodedata

import scrapy


PROJECT_ROOT = Path(__file__).resolve().parents[3]


class DegreeProgramsSpider(scrapy.Spider):
    name = "degree_programs"
    custom_settings = {
        "FEEDS": {
            str(PROJECT_ROOT / "data" / "raw" / "csuf_bs_degrees.json"): {
                "format": "json",
                "overwrite": True,
                "encoding": "utf8",
            }
        }
    }

    async def start(self):
        """Parse locally saved program pages; do not request the live catalog."""
        pages = sorted((PROJECT_ROOT / "docs" / "degree_html" / "CSUF").glob("*.html"))

        for page in pages:
            yield scrapy.Request(
                page.as_uri(),
                callback=self.parse_program,
            )

    def parse_program(self, response):
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

        slug = unicodedata.normalize("NFKD", major).encode("ascii", "ignore").decode()
        slug = re.sub(r"[^a-zA-Z0-9]+", "-", slug).strip("-").lower()
        year_slug = catalog_year or "unknown"

        yield {
            "id": f"csuf-bs-{slug}-{year_slug}",
            "record_type": "degree_program",
            "university": "California State University, Fullerton",
            "major": major,
            "degree": "Bachelor of Science",
            "catalog_year": catalog_year,
            "total_units": total_units,
            "core_courses": core_courses,
            "elective_courses": elective_courses,
            "concentrations": [],
        }
