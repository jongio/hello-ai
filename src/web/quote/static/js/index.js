$(document).ready(function () {
    // Define a function to fetch a quote
    function fetchQuote() {
        // Display a loading message where the quote will be
        $('#quote').text('Loading quote...');

        $.ajax({
            url: '/quote',
            type: 'GET',
            success: function (data) {
                // Once the quote is fetched, display it
                $('#quote').text(data.quote || 'No quote found.');
            },
            error: function (error) {
                // If there's an error, show an error message
                console.error('Error fetching new quote:', error);
                $('#quote').text('Error fetching new quote.');
            }
        });
    }

    // Call fetchQuote on page load
    fetchQuote();

    // Bind fetchQuote to button click event
    $('#fetch-quote').click(function () {
        fetchQuote();
    });
});

