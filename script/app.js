
let rowData = [];
let gridOptions;
let map;
let websocket;
let config;

async function loadConfig() {
    try {
        const response = await fetch('config.json');
        config = await response.json();
        return config;
    } catch (error) {
        console.error('Failed to load config:', error);
    }
}

async function init() {
    const cfg = await loadConfig();
    if (!cfg) return;

    initGrid();

    const script = document.createElement('script');
    script.async = true;
    script.defer = true;
    script.src = `https://maps.googleapis.com/maps/api/js?key=${cfg.googleMapsAPIKey}&callback=initMap`;
    document.body.appendChild(script);
}

function initGrid() {
    gridOptions = {
        columnDefs: [
            { field: "rssi", headerName: "RSSI", maxWidth: 100, filter: 'agNumberColumnFilter' },
            { field: "ssid", headerName: "SSID", resizable: true },
            { field: "device", headerName: "Device", minWidth: 150, resizable: true },
            { field: "vendor", headerName: "Vendor", resizable: true },
        ],
        defaultColDef: { sortable: true, filter: true },
        rowSelection: 'multiple',
        animateRows: true,
    };

    const eGridDiv = document.getElementById("myGrid");
    new agGrid.Grid(eGridDiv, gridOptions);
    gridOptions.api.sizeColumnsToFit({
        defaultMinWidth: 100
    });
}

function initMap() {
    const centerOn = new google.maps.LatLng(config.defaultLat, config.defaultLong);
    map = new google.maps.Map(
        document.getElementById('map'),
        {
            center: centerOn,
            zoom: config.defaultZoom
        }
    );
    webSocketConnect();
}

let reconnectInterval = 5000;

function webSocketConnect() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const serverURL = `${protocol}//${window.location.host}/ws`;
    websocket = new WebSocket(serverURL);

    websocket.onopen = function(event) {
        console.log("Websocket connection opened");
    };

    websocket.onclose = function(event) {
        console.log(`Websocket connection closed. Reconnecting in ${reconnectInterval/1000}s...`);
        setTimeout(webSocketConnect, reconnectInterval);
    };

    websocket.onmessage = function(event) {
        try {
            const msg = JSON.parse(event.data);

            if (msg.location && Array.isArray(msg.location)) {
                msg.location.forEach(locData => {
                    let loc;
                    if (locData.lat === 0.0 && locData.lng === 0.0) {
                        loc = new google.maps.LatLng(config.defaultLat, config.defaultLong);
                    } else {
                        loc = new google.maps.LatLng(locData.lat, locData.lng);
                    }
                    new google.maps.Marker({
                        label: msg.ssid,
                        position: loc,
                        map: map
                    });
                });
            }

            rowData.push({ rssi: msg.rssi, ssid: msg.ssid, device: msg.device, vendor: msg.vendor });
            gridOptions.api.setRowData(rowData);
        } catch (e) {
            console.error("Error processing message:", e);
        }
    };

    websocket.onerror = function(event) {
        console.error("Websocket error:", event);
        websocket.close();
    };
}

window.onload = init;
