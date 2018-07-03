# Google Analytics

This project includes a Google Analytics set up with custom events for CSV downloads and clicking Organization links, to track what data users are looking at/searching for. To make use of Google Analytics, you will have to create your own Google Analytics account and plug your new UA code in the `gtag('config')` function in `templates/includes/head.html`. Everything else should work automatically.

Two custom events are included to help track how users are interacting with the product. 

## CSV Download

There are two events for CSV downloads: full CSV & specific domain CSV. This are categorized under "Download" actions.

## Filtering by Organization

There is one event for searching/filtering, which is triggered when a user clicks on a "Show domains" link on the Organization view of the dashboard. It tracks which Organizations the users are most interested in, and are categorized under "Search" actions. Please note that this doesn't track users manually inputting searches in the search bar. 
