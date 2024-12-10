// Function to activate a specific tab programmatically
function navigateToTab(tabId) {
  // Check if the tab exists
  const tabElement = document.getElementById(tabId);

  if (tabElement) {
    // Initialize the Bootstrap Tab component on the tab
    var myTab = new bootstrap.Tab(tabElement);
    // Show the selected tab
    myTab.show();
  }
}
