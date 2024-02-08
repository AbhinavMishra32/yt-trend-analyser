fetch('video_data.json')
    .then(response => response.json())
    .then(data => {
        const channels = {};

        // Iterate over each channel
        Object.entries(data).forEach(([channelId, videos]) => {
            const viewCounts = videos.map(video => video.viewCount);

            const chartContainer = document.createElement('div');
            chartContainer.classList.add('chart-container');

            // Calculate channel age and upload frequency
            const channelAge = videos[0].channel_age;
            const uploadFrequency = calculateUploadFrequency(videos);

            // Include channel age and upload frequency in the chart title
            const chartTitle = document.createElement('div');
            chartTitle.classList.add('chart-title');
            chartTitle.textContent = `View Count Distribution for Channel ${videos[0].channel_name} (Age: ${channelAge}, Upload Frequency: ${uploadFrequency})`;

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

function calculateUploadFrequency(videos) {
    // Calculate upload frequency based on the difference between publish dates
    const publishDates = videos.map(video => new Date(video.publishedAt));
    const timeDifferences = [];
    for (let i = 0; i < publishDates.length - 1; i++) {
        const diff = Math.abs(publishDates[i] - publishDates[i + 1]);
        timeDifferences.push(diff);
    }
    const averageDiff = timeDifferences.reduce((acc, curr) => acc + curr, 0) / timeDifferences.length;
    // Convert averageDiff to a human-readable format (e.g., days, months, etc.)
    // This conversion logic depends on your specific requirements and preferences
    return averageDiff; // Return the calculated upload frequency
}
