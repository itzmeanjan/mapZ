// this is a simple tile map server implementation, built with Express, serves tiles indentified by combination of zoom_level, row_id and column_id
const express = require('express');
const app = express(); // express app's instance gets created here
const join = require('path').join;
const exists = require('fs').exists; // only importing `exists` method
let tile_path = '/path-to-tile/';
app.get('/tile/:zoom/:row/:col.png', (req, res) => {
    // this is the path we're listening to
    // where zoom, request param, gives us zoom level for that tile requested
    // row, gives row number of tile to be served
    // col, gives column number of tile to be served
    console.log(`\t[+]Incoming request from --- ${req.ip}`);
    var target_path = join(tile_path, `${req.params.zoom
        }_${req.params.row}_${req.params.col}.png`); // this is requested tile
    exists(target_path, (e) => {
        if (e) {
            res.status(200).type('png').sendFile(target_path, {
                headers: {
                    'x-timestamp': Date.now(),
                    'x-sent': true
                },
                dotfiles: 'deny' // setting header
            }, (err) => {
                if (err)
                    console.log(`\t\t[!]${err}`); // denotes error
            });
            // sets status code
            // sets Content-Type field in Header
            // sends tile
        }
        else {
            res.status(404).json({ err: 'Illegal tile requested' }); // if requested tile is not available
        }
    });
});
app.listen(8000, '0.0.0.0', () => {
    // tms listens at 0.0.0.0:8000, so that it can be accessed via both localhost and devices present in local network
    console.log('[+]Tile Map Server listening at - `0.0.0.0: 8000`\n');
});