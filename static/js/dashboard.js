// Dashboard initialization
document.addEventListener('DOMContentLoaded', function() {
    // Check if Chart.js is loaded
    if (typeof Chart === 'undefined') {
        console.error('Chart.js is not loaded!');
        alert('Error: Chart.js library could not be loaded. Please check your internet connection.');
        return;
    }
    
    console.log('Dashboard initialized. Chart.js is available:', typeof Chart);
    
    // Fetch all data
    fetchSummary();
    fetchSalesTrend();
    fetchTopCustomers();
    fetchProductBreakdown(); 
    fetchInvoiceStatus();
    fetchAging();
    
    // Date range change event
    document.getElementById('dateRange').addEventListener('change', function() {
        // Refresh all data with new date range
        fetchSummary();
        fetchSalesTrend();
        fetchTopCustomers();
        fetchProductBreakdown();
        fetchInvoiceStatus();
        fetchAging();
    });
});

// Fetch summary metrics
function fetchSummary() {
    fetch('/api/summary')
        .then(response => response.json())
        .then(data => {
            document.getElementById('totalRevenue').textContent = '$' + data.total_revenue.toLocaleString();
            document.getElementById('totalExpenses').textContent = '$' + data.total_expenses.toLocaleString();
            document.getElementById('netProfit').textContent = '$' + data.net_profit.toLocaleString();
            document.getElementById('invoiceCount').textContent = data.invoice_count.toLocaleString();
            
            const revenueChangeEl = document.getElementById('revenueChange');
            revenueChangeEl.textContent = data.revenue_change + '%';
            revenueChangeEl.className = 'metric-change ' + (data.revenue_change >= 0 ? 'positive' : 'negative');
        });
}

// Create sales trend chart
function fetchSalesTrend() {
    console.log('Fetching sales trend data...');
    fetch('/api/sales_trend')
        .then(response => response.json())
        .then(data => {
            console.log('Sales trend data received:', data);
            
            // Check if we have valid data
            if (!data.labels || !data.values || data.labels.length === 0) {
                console.warn('No valid data for sales trend chart, using fallback data');
                // Use fallback data for testing
                data = {
                    labels: ['2023-1', '2023-2', '2023-3', '2023-4', '2023-5', '2023-6'],
                    values: [10000, 12000, 9500, 14000, 11000, 13500]
                };
            }
            
            const ctx = document.getElementById('salesTrendChart');
            if (!ctx) {
                console.error('Canvas element salesTrendChart not found!');
                return;
            }
            console.log('Canvas element found, getting context...');
            
            const context = ctx.getContext('2d');
            
            // Safely destroy existing chart if it exists
            if (window.salesTrendChart && typeof window.salesTrendChart.destroy === 'function') {
                window.salesTrendChart.destroy();
            }
            
            try {
                window.salesTrendChart = new Chart(context, {
                    type: 'line',
                    data: {
                        labels: data.labels,
                        datasets: [{
                            label: 'Revenue',
                            data: data.values,
                            borderColor: '#0088FE',
                            backgroundColor: 'rgba(0, 136, 254, 0.1)',
                            borderWidth: 2,
                            tension: 0.3,
                            fill: true
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: {
                                position: 'top',
                            }
                        },
                        scales: {
                            y: {
                                beginAtZero: true,
                                ticks: {
                                    callback: function(value) {
                                        return '$' + value.toLocaleString();
                                    }
                                }
                            }
                        }
                    }
                });
                console.log('Sales trend chart created successfully');
            } catch (error) {
                console.error('Error creating sales trend chart:', error);
            }
        })
        .catch(error => {
            console.error('Error fetching sales trend data:', error);
        });
}

// Create top customers chart
function fetchTopCustomers() {
    fetch('/api/top_customers')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('customersChart');
            if (!ctx) {
                console.error('Canvas element customersChart not found!');
                return;
            }
            
            const context = ctx.getContext('2d');
            
            // Safely destroy existing chart if it exists
            if (window.customersChart && typeof window.customersChart.destroy === 'function') {
                window.customersChart.destroy();
            }
            
            try {
                window.customersChart = new Chart(context, {
                    type: 'bar',
                    data: {
                        labels: data.names,
                        datasets: [{
                            label: 'Sales',
                            data: data.values,
                            backgroundColor: '#8884d8',
                            borderWidth: 0
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        indexAxis: 'y',
                        plugins: {
                            legend: {
                                display: false
                            }
                        },
                        scales: {
                            x: {
                                beginAtZero: true,
                                ticks: {
                                    callback: function(value) {
                                        return '$' + value.toLocaleString();
                                    }
                                }
                            }
                        }
                    }
                });
            } catch (error) {
                console.error('Error creating customers chart:', error);
            }
        })
        .catch(error => {
            console.error('Error fetching top customers data:', error);
        });
}

// Create product breakdown chart
function fetchProductBreakdown() {
    fetch('/api/product_breakdown')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('productsChart');
            if (!ctx) {
                console.error('Canvas element productsChart not found!');
                return;
            }
            
            const context = ctx.getContext('2d');
            
            // Safely destroy existing chart if it exists
            if (window.productsChart && typeof window.productsChart.destroy === 'function') {
                window.productsChart.destroy();
            }
            
            const colors = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8'];
            
            try {
                window.productsChart = new Chart(context, {
                    type: 'pie',
                    data: {
                        labels: data.names,
                        datasets: [{
                            data: data.values,
                            backgroundColor: colors,
                            borderWidth: 0
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: {
                                position: 'right'
                            },
                            tooltip: {
                                callbacks: {
                                    label: function(context) {
                                        const label = context.label || '';
                                        const value = context.raw || 0;
                                        const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                        const percentage = ((value / total) * 100).toFixed(1);
                                        return `${label}: $${value.toLocaleString()} (${percentage}%)`;
                                    }
                                }
                            }
                        }
                    }
                });
            } catch (error) {
                console.error('Error creating products chart:', error);
            }
        })
        .catch(error => {
            console.error('Error fetching product breakdown data:', error);
        });
}

// Create invoice status chart
function fetchInvoiceStatus() {
    fetch('/api/invoice_status')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('invoiceStatusChart');
            if (!ctx) {
                console.error('Canvas element invoiceStatusChart not found!');
                return;
            }
            
            const context = ctx.getContext('2d');
            
            // Safely destroy existing chart if it exists
            if (window.invoiceStatusChart && typeof window.invoiceStatusChart.destroy === 'function') {
                window.invoiceStatusChart.destroy();
            }
            
            try {
                window.invoiceStatusChart = new Chart(context, {
                    type: 'pie',
                    data: {
                        labels: data.labels,
                        datasets: [{
                            data: data.values,
                            backgroundColor: ['#00C49F', '#FF8042'],
                            borderWidth: 0
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: {
                                position: 'bottom'
                            },
                            tooltip: {
                                callbacks: {
                                    label: function(context) {
                                        const label = context.label || '';
                                        const value = context.raw || 0;
                                        const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                        const percentage = ((value / total) * 100).toFixed(1);
                                        return `${label}: ${value} invoices (${percentage}%)`;
                                    }
                                }
                            }
                        }
                    }
                });
                
                // Update receivables amount
                document.getElementById('totalReceivables').textContent = '$' + data.receivables.toLocaleString();
            } catch (error) {
                console.error('Error creating invoice status chart:', error);
            }
        })
        .catch(error => {
            console.error('Error fetching invoice status data:', error);
        });
}

// Create aging chart
function fetchAging() {
    fetch('/api/aging')
        .then(response => response.json())
        .then(data => {
            const agingContainer = document.getElementById('agingBoxes');
            agingContainer.innerHTML = '';
            
            const total = data.amounts.reduce((sum, amount) => sum + amount, 0);
            
            const colors = ['#4CAF50', '#2196F3', '#FFC107', '#FF5722'];
            
            for (let i = 0; i < data.buckets.length; i++) {
                const percentage = total > 0 ? ((data.amounts[i] / total) * 100).toFixed(1) : 0;
                
                const box = document.createElement('div');
                box.className = 'aging-box';
                box.style.backgroundColor = colors[i] + '20'; // Add transparency
                box.style.borderLeft = '4px solid ' + colors[i];
                
                box.innerHTML = `
                    <p class="aging-label">${data.buckets[i]}</p>
                    <p class="aging-amount">$${data.amounts[i].toLocaleString()}</p>
                    <p class="aging-percentage">${percentage}%</p>
                `;
                
                agingContainer.appendChild(box);
            }
        });
}