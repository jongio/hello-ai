$(document).ready(() => {
    const $quoteDisplay = $('#quote'); // Cache the selector

    // Define a function to fetch and display a quote
    const fetchQuote = () => {
        $quoteDisplay.text('Loading quote...'); // Display loading text

        $.ajax({
            url: '/quote',
            type: 'GET',
            success: (data) => {
                $quoteDisplay.text(data.quote || 'No quote found.'); // Display fetched quote
            },
            error: (error) => {
                console.error('Error fetching new quote:', error);
                $quoteDisplay.text('Error fetching new quote.'); // Display error message
            }
        });
    };

    // Initial fetch and setup click handler for subsequent fetches
    fetchQuote();
    $('#fetch-quote').on('click', fetchQuote);
});
