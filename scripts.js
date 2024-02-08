fetch('video_data.json')
            .then(response => response.json())
            .then(data => {
                const channels = {};

                // Iterate over each channel
                Object.entries(data).forEach(([channelId, videos]) => {
                    const viewCounts = videos.map(video => video.viewCount);

                    const chartContainer = document.createElement('div');
                    chartContainer.classList.add('chart-container');

                    const chartTitle = document.createElement('div');
                    chartTitle.classList.add('chart-title');
                    chartTitle.textContent = `View Count Distribution for Channel ${videos[0].channel_name}`;

                    const canvas = document.createElement('canvas');

                    chartContainer.appendChild(chartTitle);
                    chartContainer.appendChild(canvas);
                    document.getElementById('charts').appendChild(chartContainer);

                    new Chart(canvas, {
                        type: 'bar',
                        data: {
                            labels: videos.map(video => video.title),
                            datasets: [{
                                label: `View Count Distribution for Channel ${videos[0].channel_name}`,
                                data: viewCounts,
                                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                                borderColor: 'rgba(54, 162, 235, 1)',
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
                });
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });