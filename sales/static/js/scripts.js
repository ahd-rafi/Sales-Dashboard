document.addEventListener('DOMContentLoaded', function () {
    // Initialize date pickers
    flatpickr("#start_date", {
        dateFormat: "Y-m-d"
    });
    flatpickr("#end_date", {
        dateFormat: "Y-m-d"
    });

    // Bar Chart Initialization (Top Selling Products)
    var barCtx = document.getElementById('salesBarChart').getContext('2d');
    new Chart(barCtx, {
        type: 'bar',
        data: {
            labels: [{% for product in top_products %}"{{ product.product__product_name }}"{% if not forloop.last %}, {% endif %}{% endfor %}],
            datasets: [{
                label: 'Units Sold',
                data: [{% for product in top_products %}{{ product.total_sold }}{% if not forloop.last %}, {% endif %}{% endfor %}],
                backgroundColor: '#3498db'
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    // Line Chart Initialization (Sales Over Time)
    var lineCtx = document.getElementById('salesLineChart').getContext('2d');
    new Chart(lineCtx, {
        type: 'line',
        data: {
            labels: [{% for product in top_products %}"{{ product.product__product_name }}"{% if not forloop.last %}, {% endif %}{% endfor %}],
            datasets: [{
                label: 'Units Sold Over Time',
                data: [{% for product in top_products %}{{ product.total_sold }}{% if not forloop.last %}, {% endif %}{% endfor %}],
                borderColor: '#e74c3c',
                fill: false,
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    // Pie Chart Initialization (Revenue Breakdown by Salesperson)
    var pieCtx = document.getElementById('salesPieChart').getContext('2d');
    new Chart(pieCtx, {
        type: 'pie',
        data: {
            labels: [{% for salesperson in salesperson_revenue %}"{{ salesperson.salesperson }}"{% if not forloop.last %}, {% endif %}{% endfor %}],
            datasets: [{
                data: [{% for salesperson in salesperson_revenue %}{{ salesperson.revenue }}{% if not forloop.last %}, {% endif %}{% endfor %}],
                backgroundColor: ['#3498db', '#e74c3c', '#2ecc71', '#f1c40f', '#9b59b6'],
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Revenue Breakdown by Salesperson',
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                },
                legend: {
                    position: 'top',
                },
                tooltip: {
                    callbacks: {
                        label: function(tooltipItem) {
                            return tooltipItem.label + ': $' + tooltipItem.raw.toFixed(2);
                        }
                    }
                }
            }
        }
    });

    // Total Sales Chart
    var totalSalesCtx = document.getElementById('totalSalesChart').getContext('2d');
    new Chart(totalSalesCtx, {
        type: 'bar',
        data: {
            labels: [{% for sale in total_sales_data %}"{{ sale.date_of_sale }}"{% if not forloop.last %}, {% endif %}{% endfor %}],
            datasets: [{
                label: 'Total Sales Count',
                data: [{% for sale in total_sales_data %}{{ sale.sales_count }}{% if not forloop.last %}, {% endif %}{% endfor %}],
                backgroundColor: '#2ecc71',
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});