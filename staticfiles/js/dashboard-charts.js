document.addEventListener('DOMContentLoaded', function() {
    // User Registration Chart
    new Chart(document.getElementById('userChart'), {
        type: 'line',
        data: {
            labels: userLabels,  // Will be passed from template
            datasets: [{
                label: 'New Users',
                data: userData,  // Will be passed from template
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1,
                fill: false
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

    // Posts Chart
    new Chart(document.getElementById('postChart'), {
        type: 'bar',
        data: {
            labels: postLabels,  // Will be passed from template
            datasets: [{
                label: 'Posts Created',
                data: postData,  // Will be passed from template
                backgroundColor: 'rgb(54, 162, 235)'
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