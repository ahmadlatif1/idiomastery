document.addEventListener('DOMContentLoaded', function() {
    const searchBar = document.getElementById('search-bar');
    const tagOptions = document.getElementById('tag-options');

    searchBar.addEventListener('input', function() {
        const search = this.value;

        // Fetch suggestions from Django backend
        fetch(`/search_tags/${search}/`)  // Replace with your actual API endpoint
            .then(response => response.json())
            .then(data => {
                // Clear existing options
                tagOptions.innerHTML = '';
                console.log('tags',data['tags'])
                tags=data['tags']
                for (let i = 0; i < tags.length; i++) {
                    console.log("item",tags[i]); // Debugging line to check the item value
                    let option = document.createElement('option');
                    option.value =tags[i];  // Adjust 'data[item].name' based on your data structure
                    tagOptions.appendChild(option);
                    console.log("children",tagOptions.children); // Debugging line to check the option value
                }
            })
            .catch(error => console.error('Error fetching tags:', error)); // Added error handling
    });
});