function addtag(idiomId) {
    const tag = document.getElementById('search-bar').value;
    const id = document.getElementById('idiom-id').value; // Assuming you have a hidden input with the idiom ID
    fetch(`/add_tag/${tag}/${id}/`, { // Ensure your URL pattern in urls.py matches this
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('Tag added:', data);
        // Update the tag list on the page (example)
        const tagList = document.getElementById('tag-list');
        const newTagElement = document.createElement('div');
        newTagElement.classList.add('tag');
        newTagElement.textContent = data.tag;
        tagList.appendChild(newTagElement);

        // Clear the search bar
        document.getElementById('search-bar').value = '';
    })
    .catch(error => {
        console.error('Error adding tag:', error);
        alert('Failed to add tag.'); // Basic error feedback
    });
}

// Helper function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
