const express = require('express');
const app = express();
const path = require('path');
let home_page = path.join(__dirname, 'static', 'index.html');
app.get('/', (req, res) => {
    console.log(`\t[+]Incoming request from --- ${req.ip}`);
    res.status(200).contentType('html').sendFile(home_page, (err) => {
        if (err)
            console.log(`\t\t[!]${err}`); // denotes error
    });
});
app.listen(8001, '0.0.0.0', () => {
    console.log('[+]Mapping Application Server listening at - `0.0.0.0: 8001`\n');
});