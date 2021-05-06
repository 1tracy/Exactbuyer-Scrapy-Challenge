import scrapy

class AngelSpider(scrapy.Spider):
    name="angel"

    def start_requests(self):
        urls = []

        for i in range(27): 
            temp_str = 'https://new-york.opendi.us/L/110_'+str(i+1)+'.html'
            urls.append(temp_str)
        
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        '''
        We want to extract the following:
        - name
        - address
        - number of ratings
        - phone number
        '''
        names = response.css('h3[class="yxt-name serp-listing__name is_blue is_bold no-margin pb-20"]::text').extract()
        addresses = response.css('span[class="yxt-address is_block"]::text').extract()
        num_ratings = response.css('span[class="is_gray font-small"]::text').extract()
        details_link = response.css('button[class="serp-listing__more js-link mui-btn mui-btn-small mui-btn-primary"]::attr(href)').extract()

        items_length = len(names)

        for i in range(len(names)):
            names[i] = names[i].strip()
            addresses[i] = addresses[i].strip()
            num_ratings[i] = num_ratings[i].strip()[1:-1]
            url = response.urljoin(details_link[i])

            partial = {'Name' : names[i], 'Address' : addresses[i], 'Ratings' : num_ratings[i]}
            yield scrapy.Request(url, callback = self.parse_contents, meta={'partial_item': partial})

    def parse_contents(self, response):
        #This is a helper function that crawls the link extracted from the 'details' button
        #to get the phone number.

        item = response.meta['partial_item']
        
        phone_number = response.css('span[class="yxt-phone-main"]::text').extract()
        phone_numbers = []
        
        for k in range(len(phone_number)):
            temp = ''
            for j in phone_number[k]:
                if j.isnumeric():
                    temp+=j

            item['Phone Number'] = temp
            yield item

