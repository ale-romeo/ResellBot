const axios = require('axios');
const cheerio = require('cheerio');

async function scrapeSneakerInfo() {
    const scrapedData = [];

    for (let product = 1; product <= 100; product++) {
        const url = `https://kith.com/collections/sneakers?page=${product}`;
        let sold_out = false;

        try {
            const response = await axios.get(url);
            const $ = cheerio.load(response.data);

            const productItem = $(`li.collection-product:nth-child(${product})`);
            if (!productItem.length) {
                break;
            }

            const productCard = productItem.find('.product-card');
            const productTitle = productCard.find('.product-card__information a .product-card__title').text().trim();
            const productColor = productCard.find('.product-card__information a .product-card__color').text().trim();
            const productAvailability = productCard.find('.product-card__information a span.sold-out').length ? 'SOLD OUT' : 'AVAILABLE';
            const productLink = 'https://kith.com' + productCard.find('.product-card__information a').attr('href');

            const sneakerInfo = {
                title: productTitle,
                color: productColor,
                availability: productAvailability,
                link: productLink,
            };

            scrapedData.push(sneakerInfo);
        } catch (error) {
            console.error('Error scraping:', error);
        }
    }

    return scrapedData;
}

module.exports = { scrapeSneakerInfo };
