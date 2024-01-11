$(document).ready(function() {
    // AJAX request to fetch data from the server
    $.get('/get_data', function(response) {
        // Extract timestamp and price from the data
        var timestamps = response.data.map(function(point) {
            return new Date(point.time).getTime();
        });

        var prices = response.data.map(function(point) {
            return point.price;
        });

        // Create Highcharts chart
        Highcharts.chart('chart-container', {
            title: {
                text: 'CS:GO Skin Prices'
            },
            xAxis: {
                type: 'datetime',
                title: {
                    text: 'Time'
                }
            },
            yAxis: {
                title: {
                    text: 'Price'
                }
            },
            series: [{
                name: 'Price',
                data: prices,
                pointStart: timestamps[0],
                pointInterval: 24 * 3600 * 1000 // Assuming data is daily
            }]
        });
    });
});