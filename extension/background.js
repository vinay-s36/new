chrome.runtime.onInstalled.addListener(() => {
    console.log("Sanchalak extension installed.");
});

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.status === "complete" && tab.url) {
        console.log("Tab updated:", tab.url);
        // You can add website analysis logic here
    }
});
