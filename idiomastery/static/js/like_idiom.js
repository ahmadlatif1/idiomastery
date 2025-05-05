// Example JavaScript (using jQuery for brevity)
function likeIdiom(idiomId) {
    $.ajax({
        url: `/like_idiom/${idiomId}/`, // Replace with your actual URL
        type: 'POST', // Or PUT, depending on your preference
        headers: {
           'X-CSRFToken': getCookie('csrftoken')  // Include CSRF token for security
        },
        success: function(response) {
            console.log(response.message); // Log the success message
            // Update the score on the page
            $('#idiom-score-' + idiomId).text(response.score);
            // Optionally, update the like button appearance based on response.liked
               var button = $('#idiom-like-button-' + idiomId);
                if (response.liked) {
                    button.find('i').removeClass('bi-heart').addClass('bi-heart-fill').css('color', 'red');
                } else {
                    button.find('i').removeClass('bi-heart-fill').addClass('bi-heart').css('color', ''); // Reset color to default
                }
        },
        error: function(xhr, status, error) {
            console.error("Error liking idiom:",status, error);
            if (xhr.status === 401) {
                alert("Please log in to like this idiom.");
            } else {
                alert("An error occurred.");
            }
        }
    });
}






// Helper function to get CSRF token from cookies (required for Django POST requests)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}