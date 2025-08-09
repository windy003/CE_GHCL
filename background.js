chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'repoDetected') {
    chrome.storage.local.set({ 
      currentRepo: message.repoInfo,
      tabId: sender.tab.id 
    });
  }
});