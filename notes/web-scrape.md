# Web-Scraping Notes 
Notes for the web-scraping portion

https://fullerton.catalog.acalog.com/content.php?catoid=101&navoid=15150

## To Run
Since you can only run the scraper from its directory, remember to go up a directory first.  
The scraper goes through the entire directory of HTML's.  

``` bash
uv run scrapy crawl degree_programs \
-a input_dir="../docs/degree_html/CSUF" \
-a university="CSU Fullerton" \
-O ../data/raw/csuf_bs_degrees.json
```

## Degree Program Structure Difference
This is looking strictly at Bachelor degrees in stem, without concentration.  
CSUFs structure for the degree programs vary. This is taking note in the beginning structure and similarities/differences.

Basic Courses 
* Biochemistry
* Chemistry

Core Requirements
* Biological Science
* Human Services 

Courses 
* Civil Engineering
* Computer Engineering 
* Computer Science 

Degree Requirements
* Electrical Engineering 
* Engineering 
* Mechanical Engineering 
* Nursing 

Required
* Communicative Disorders
* Geology

Prerequisite Requirements...
* Kinesiology

Lower Division 
* Physics

Prerequisite
* Public Health 


# Conflict (1)
* Using Scrapy, the spider responsible for scraping the data did not work because of CSUF's AWS Web Application Firewall forced it to return a verification page.  
 
 ## Solution
 Manually print the STEM degrees as a pdf or save as an html file and run the spider on that batch.  

