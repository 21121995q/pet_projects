document.addEventListener('DOMContentLoaded', () => {
    const searchForm = document.getElementById('search-form');
    const searchInput = document.getElementById('search-input');
    const resultsContainer = document.getElementById('results-container');
    const posCount = document.getElementById('pos-count');
    const negCount = document.getElementById('neg-count');
    const neutCount = document.getElementById('neut-count');

    searchForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const query = searchInput.value;
        if (query) {
            const response = await fetch(`/search?query=${encodeURIComponent(query)}`);
            const data = await response.json();
            updateSentimentSummary(data.sentiment_counts);
            displayResults(data.videos);
        }
    });

    function updateSentimentSummary(counts) {
        posCount.textContent = `Pos: ${counts.Positive}`;
        negCount.textContent = `Neg: ${counts.Negative}`;
        neutCount.textContent = `Neut: ${counts.Neutral}`;
    }

    function displayResults(data) {
        resultsContainer.innerHTML = '';
        if (data.error) {
            resultsContainer.innerHTML = `<p>${data.error}</p>`;
            return;
        }
        
        data.forEach(video => {
            const videoElement = document.createElement('div');
            videoElement.classList.add('video');

            const videoTitle = document.createElement('h3');
            videoTitle.textContent = video.title;

            const videoLikes = document.createElement('p');
            videoLikes.textContent = `Likes: ${video.likes}`;

            const commentsList = document.createElement('ul');
            video.comments.forEach(comment => {
                const commentElement = document.createElement('li');
                
                const commentText = document.createElement('p');
                commentText.classList.add('comment-text');
                commentText.textContent = `${comment.text} (Likes: ${comment.likes})`;

                const sentimentDefault = document.createElement('p');
                sentimentDefault.classList.add('comment-sentiment');
                sentimentDefault.textContent = `Default Model: ${comment.sentiments.default}`;

                const sentimentSiebert = document.createElement('p');
                sentimentSiebert.classList.add('comment-sentiment');
                sentimentSiebert.textContent = `SiEBERT Model: ${comment.sentiments.siebert}`;

                const sentimentBert = document.createElement('p');
                sentimentBert.classList.add('comment-sentiment');
                sentimentBert.textContent = `BERT Model: ${comment.sentiments.bert}`;

                commentElement.appendChild(commentText);
                commentElement.appendChild(sentimentDefault);
                commentElement.appendChild(sentimentSiebert);
                commentElement.appendChild(sentimentBert);
                commentsList.appendChild(commentElement);
            });

            videoElement.appendChild(videoTitle);
            videoElement.appendChild(videoLikes);
            videoElement.appendChild(commentsList);
            resultsContainer.appendChild(videoElement);
        });
    }
});

