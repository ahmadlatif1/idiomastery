document.addEventListener('DOMContentLoaded', function() {
    const searchBar = document.getElementById('search-bar-main');

    searchBar.addEventListener('input', function() {
        const search = this.value;

        // Fetch suggestions from Django backend
        fetch(`/search_preview/${search}/`)  // Replace with your actual API endpoint
            .then(response => response.json())
            .then(data => {
                // Clear existing options

                const searchOptions = document.getElementById("search-options");
                console.log(searchOptions)
                searchOptions.innerHTML=''
                
                
                res=data['results']
                console.log("test",res)


                for (i=0;i<res.length;i++){
                    console.log("result: ",res[i]['phrase'])
                    let option = document.createElement('option');
                    option.textContent=res[i]['phrase']
                    option.href=("/"+res[i]['id']+"/")

                    console.log(option.innerHTML)
                    searchOptions.appendChild(option)
                    console.log(searchOptions.innerHTML)

                }
            })
            .catch(error => console.error('Error fetching tags:', error)); // Added error handling
    });
});