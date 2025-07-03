let stockList = [];

async function fetchStocks() {
    const res = await fetch('./static/stocks.json');
    stockList = await res.json();
}

function setupAutocomplete() {
    const input = document.querySelector('input[name="company"]');
    const dropdown = document.createElement('div');
    dropdown.style.border = '1px solid #ccc';
    dropdown.style.position = 'absolute';
    dropdown.style.background = '#fff';
    dropdown.style.zIndex = 1000;
    dropdown.style.width = input.offsetWidth + 'px';
    dropdown.style.maxHeight = '200px';
    dropdown.style.overflowY = 'auto';
    dropdown.style.display = 'none';

    input.parentNode.appendChild(dropdown);

    input.addEventListener('input', () => {
        const val = input.value.toLowerCase();
        dropdown.innerHTML = '';

        if (!val) {
            dropdown.style.display = 'none';
            return;
        }

        const filtered = stockList.filter(stock =>
            stock.name.toLowerCase().includes(val) ||
            stock.symbol.toLowerCase().includes(val)
        ).slice(0, 10); // Limit results

        filtered.forEach(stock => {
            const div = document.createElement('div');
            div.textContent = `${stock.name} (${stock.symbol})`;
            div.style.padding = '5px';
            div.style.cursor = 'pointer';
            div.addEventListener('click', () => {
                input.value = stock.name;
                dropdown.style.display = 'none';
            });
            dropdown.appendChild(div);
        });

        dropdown.style.display = filtered.length ? 'block' : 'none';
    });

    document.addEventListener('click', (e) => {
        if (!input.contains(e.target)) {
            dropdown.style.display = 'none';
        }
    });
}



// =================== GRAPH POPUP LOGIC ===================

function drawChart() {
    const ctx = document.getElementById('stockChart').getContext('2d');

    // Get data from embedded JSON
    const chartData = JSON.parse(document.getElementById('chart-data').textContent);

    const labels = chartData.map(article => article.title.slice(0, 40) + '...');
    const values = chartData.map(article => {
        const match = article.stock_change.match(/([+-]?[0-9.]+)/);
        return match ? parseFloat(match[1]) : 0;
    });

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Stock % Change',
                data: values,
                backgroundColor: values.map(v => v > 0 ? '#28a745' : v < 0 ? '#dc3545' : '#6c757d')
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            return `Change: ${context.raw.toFixed(2)}%`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: '% Change'
                    }
                }
            }
        }
    });
}

function setupGraphPopup() {
    const showBtn = document.getElementById('showGraphBtn');
    const popup = document.getElementById('graphPopup');
    const closeBtn = document.getElementById('closePopup');

    if (showBtn) {
        showBtn.addEventListener('click', () => {
            popup.style.display = 'flex';
            drawChart();
        });
    }

    if (closeBtn) {
        closeBtn.addEventListener('click', () => {
            popup.style.display = 'none';
        });
    }
}


window.onload = async function () {
    await fetchStocks();
    setupAutocomplete();
    setupGraphPopup();
};