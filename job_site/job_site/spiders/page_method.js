let count = 0; // Counter to track the number of clicks
const load_pages = LOAD_PAGES; // Injected variable: number of pages to load
const click_timeout = CLICK_TIMEOUT; // Injected variable: timeout between clicks

async function clickLoadMore() {
    while (count < load_pages) { // Keep clicking until the target number of pages is loaded
        const button = document.querySelector('div.show-more'); // Find the "Load More" button
        
        if (button) { // If the button is found, proceed with clicking
            button.scrollIntoView({ behavior: 'smooth', block: 'center' }); // Smoothly scroll the button into view
            button.click(); // Simulate the click on the button
            count++; // Increment the count after each click
            console.log("Clicked, count:", count); // Debug log to show progress

            await new Promise(resolve => setTimeout(resolve, click_timeout)); // Wait for the timeout before clicking again
        } else {
            break; // If no button is found, stop the loop
        }
    }
}
