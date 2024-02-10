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
            const channelAge = calculateChannelAge(videos[0].channel_created_age); // Pass channel age in days
            const uploadFrequency = calculateUploadFrequency(videos);

            // Include channel age and upload frequency in the chart title
            const chartTitle = document.createElement('div');
            chartTitle.classList.add('chart-title');

            // Add channel link
            const channelLink = document.createElement('a');
            channelLink.href = videos[0].channel_link;
            channelLink.textContent = `View Channel: ${videos[0].channel_name}`;
            channelLink.target = "_blank"; // Open link in a new tab
            chartTitle.appendChild(channelLink);

            chartTitle.innerHTML += `<br>Channel Age: ${channelAge}, Upload Frequency: ${uploadFrequency}`;

            const canvas = document.createElement('canvas');

            chartContainer.appendChild(chartTitle);
            chartContainer.appendChild(canvas);
            document.getElementById('charts').appendChild(chartContainer);

            new Chart(canvas, {
                type: 'bar',
                data: {
                    // Truncate video titles if they exceed 10 characters
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
                    tooltips: {
                        callbacks: {
                            title: function(tooltipItem, data) {
                                // Return the full video title for the tooltip
                                return videos[tooltipItem[0].index].title;
                            }
                        }
                    },
                    scales: {
                        x: {
                            ticks: {
                                callback: function(value, index, values) {
                                    // Truncate x-axis labels if they exceed 10 characters
                                    return value.length > 10 ? value.substring(0, 10) + '...' : value;
                                }
                            }
                        },
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

function calculateChannelAge(channelAgeInDays) {
    // Calculate channel age in days, months, and years
    const years = Math.floor(channelAgeInDays / 365);
    const months = Math.floor((channelAgeInDays % 365) / 30);
    const days = channelAgeInDays % 30;

    return `${years} years, ${months} months, ${days} days`;
}

function calculateUploadFrequency(videos) {
    // Calculate upload frequency based on the difference between publish dates
    const publishDates = videos.map(video => new Date(video.publishedAt)).sort((a, b) => a - b);
    const timeDifferences = [];
    for (let i = 0; i < publishDates.length - 1; i++) {
        const diff = Math.abs(publishDates[i + 1] - publishDates[i]) / (1000 * 60 * 60 * 24); // convert to days
        timeDifferences.push(diff);
    }
    const averageDiff = timeDifferences.reduce((acc, curr) => acc + curr, 0) / timeDifferences.length;
    return `Avg 1 upload per ${averageDiff.toFixed(2)} days`; // Return the calculated upload frequency
}
