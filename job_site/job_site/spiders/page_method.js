let count = 0;  // Initialize a counter to track the number of "Load More" clicks
const load_pages = LOAD_PAGES;  // Placeholder for injected Python variable (number of pages to load)
const click_timeout = CLICK_TIMEOUT;  // Placeholder for injected Python variable (timeout between clicks)

async function clickLoadMore() {
    while (count < load_pages) {  // Continue clicking while the count is less than the number of pages
        const button = document.querySelector('div.show-more');  // Find the "Load More" button using its CSS selector

        if (button) {  // If the "Load More" button exists on the page
            button.scrollIntoView({ behavior: 'smooth', block: 'center' });  // Scroll the button into view smoothly
            button.click();  // Click the "Load More" button
            count++;  // Increment the counter after each click
            console.log("Clicked, count:", count);  // Debug log to track how many times the button has been clicked
            await new Promise(resolve => setTimeout(resolve, click_timeout));  // Wait for the specified timeout before the next click
        } else {
            break;  // If no "Load More" button is found, stop the loop
        }
    }
}

clickLoadMore();  // Call the function to start the "Load More" clicking process
