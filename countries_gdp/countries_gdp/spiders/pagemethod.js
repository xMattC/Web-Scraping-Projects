let count = 0;
const load_pages = 3;  // Set the number of times to click the "Show More" button

const handler = () => {
    const button = document.querySelector('.show-more');  // Get the first "Show More" button

    if (button && count < load_pages) {
        button.scrollIntoView();  // Scroll the button into view
        button.click();  // Click the button
        count++;  // Increment the count
    }

    // If the button doesn't exist or we've clicked the desired number of times, stop the interval
    if (count >= load_pages || !button) {
        clearInterval(intervalID);
    }
};

// Call the handler every 1000ms (1 second)
const intervalID = setInterval(handler, 1000);

