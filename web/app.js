// WebSocket ke Python dashboard_ws.py
const ws = new WebSocket("ws://localhost:8765");

let priceLabels = [];
let priceData = [];

let ohlcLabels = [];
let ohlcData = [];  // candlestick

ws.onmessage = (event) => {
    const msg = JSON.parse(event.data);

    if (msg.type === "price") {
        priceLabels.push(new Date(msg.timestamp * 1000).toLocaleTimeString());
        priceData.push(msg.price);

        if (priceLabels.length > 30) {
            priceLabels.shift();
            priceData.shift();
        }
        priceChart.update();
    }

    if (msg.type === "ohlc") {
        ohlcLabels.push(new Date(msg.interval_end).toLocaleTimeString());
        ohlcData.push({
            o: msg.open,
            h: msg.high,
            l: msg.low,
            c: msg.close
        });

        if (ohlcLabels.length > 30) {
            ohlcLabels.shift();
            ohlcData.shift();
        }
        ohlcChart.update();
    }
};

// Price Line Chart
const priceChart = new Chart(document.getElementById("priceChart"), {
    type: "line",
    data: {
        labels: priceLabels,
        datasets: [{
            label: "BTC Price",
            data: priceData,
        }]
    }
});

// OHLC Candlestick Chart
const ohlcChart = new Chart(document.getElementById("ohlcChart"), {
    type: "bar",
    data: {
        labels: ohlcLabels,
        datasets: [{
            label: "OHLC",
            data: ohlcData
        }]
    }
});
