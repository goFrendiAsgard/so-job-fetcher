from lxml import html
import requests, json, sys, datetime, time

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
            'company_loc': company_location.replace('- \r\n', ''),
            'remote': job_remote,
            }
        result.append(row)
    return result

def dump_now(query=''):
    query = '&' + query if query != '' else ''
    webpage = requests.get('https://stackoverflow.com/jobs?_123=456' + query)
    tree = html.fromstring(webpage.content)
    pages = tree.xpath('//div[contains(@class,"pagination")]/a[contains(@class,"job-link")]/text()')
    max_page = int(pages[-2]) if len(pages) > 2 else 1
    result = []
    for i in range(max_page):
        url = 'https://stackoverflow.com/jobs?_123=456&pg=' + str(i+1) + query
        print('URL: ' + url)
        result = result + scrap(url)
        print('Job count: ' + str(len(result)))
    file_name = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d %H%M%S') + query + '.json'
    json_file = open(file_name, 'w')
    json_file.write(json.dumps(result, sort_keys=True, indent=4))
    json_file.close()
    print('Dumped to json')

if __name__ == '__main__':
    query = sys.argv[1] if len(sys.argv)>1 else ''
    dump_now(query)
