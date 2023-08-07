// renderer.js

const { ipcRenderer } = require('electron');

ipcRenderer.on('scrapedData', (event, scrapedData) => {
    const sneakerContainer = document.getElementById('sneakerContainer');
    scrapedData.forEach(sneaker => {
        const sneakerElement = document.createElement('div');
        sneakerElement.className = 'sneaker';
        sneakerElement.innerHTML = `
            <h2>${sneaker.title}</h2>
            <p><strong>Color:</strong> ${sneaker.color}</p>
            <p><strong>Availability:</strong> ${sneaker.availability}</p>
            <p><strong>Link:</strong> <a href="${sneaker.link}">${sneaker.link}</a></p>
        `;
        sneakerContainer.appendChild(sneakerElement);
    });
});
