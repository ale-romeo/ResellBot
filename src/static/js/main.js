// main.js

const { app, BrowserWindow, ipcMain } = require('electron');
const { scrapeSneakerInfo } = require('./scraper'); // Create scraper.js as mentioned below

let mainWindow;

app.on('ready', () => {
    mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: true
        }
    });

    mainWindow.loadFile('index.html');

    const scrapedData = scrapeSneakerInfo(); // Call your scraping function here
    mainWindow.webContents.send('scrapedData', scrapedData);
});
