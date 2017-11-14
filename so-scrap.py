from lxml import html
import requests, json, sys

def scrap(url):
    # get the tree
    webpage = requests.get(url)
    tree = html.fromstring(webpage.content)
    # create result
    job_list = tree.xpath('//div[contains(@class,"-job-item")]')
    result = []
    for job in job_list:
        job_summary = job.xpath('.//div[contains(@class,"-job-summary")]')[0]
        job_title = job_summary.xpath('.//a[@class="job-link"]/text()')[0]
        job_tag = job.xpath('.//a[contains(@class,"post-tag")]/text()')
        job_posted = job.xpath('.//p[contains(@class,"-posted-date")]/text()')[0].strip()
        job_company = job.xpath('.//div[contains(@class,"-company")]')[0]
        company_name = job_company.xpath('.//div[contains(@class,"-name")]/text()')[0].strip()
        company_location = job_company.xpath('.//div[contains(@class,"-location")]/text()')[0].strip()
        job_remote = len(job.xpath('.//span[contains(@class,"-remote")]/text()'))
        row = {
            'title': job_title,
            'tag': job_tag,
            'posted_date': job_posted,
            'company_name': company_name,
            'company_loc': company_location,
            'remote': job_remote,
            }
        result.append(row)
    return result

def dump_now():
    webpage = requests.get('https://stackoverflow.com/jobs')
    tree = html.fromstring(webpage.content)
    pages = tree.xpath('//div[contains(@class,"pagination")]/a[contains(@class,"job-link")]/text()')
    max_page = int(pages[-2]) if len(pages) > 2 else 1
    result = []
    for i in range(max_page):
        url = 'https://stackoverflow.com/jobs?pg='+str(i+1)
        print('URL: ' + url)
        result = result + scrap(url)
        print('Job count: ' + str(len(result)))
    json_file = open('stack-overflow-now.json', 'w')
    json_file.write(json.dumps(result, sort_keys=True, indent=4))
    json_file.close()
    print('Dumped to json')

if __name__ == '__main__':
    if len(sys.argv) == 1 or sys.argv[2] == 'now':
        dump_now()
