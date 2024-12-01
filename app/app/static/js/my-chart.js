function drawCateChart(labels, data) {
    const ctx = document.getElementById('cateStats');

  new Chart(ctx, {
    type: 'pie',
    data: {
      labels: labels,
      datasets: [{
        label: 'Số lượng',
        data: data,
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}

function drawRevenueChart(labels, data){
     const ctx = document.getElementById('revenues');

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'doanh thu',
        data: data,
        borderWidth: 1,
        backgroundColor: [
            'rgba(255, 99, 132, 0.5)', // Màu phần 1
            'rgba(54, 162, 235, 0.5)', // Màu phần 2
            'rgba(255, 206, 86, 0.5)'  // Màu phần 3
        ],
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}