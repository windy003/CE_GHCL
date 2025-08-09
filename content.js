function extractRepoInfo() {
  const url = window.location.href;
  const repoMatch = url.match(/github\.com\/([^\/]+)\/([^\/\?#]+)/);
  
  if (repoMatch) {
    const owner = repoMatch[1];
    const repo = repoMatch[2];
    const repoUrl = `https://github.com/${owner}/${repo}`;
    const cloneUrl = `${repoUrl}.git`;
    
    return {
      owner,
      repo,
      url: repoUrl,
      cloneUrl,
      isRepo: true
    };
  }
  
  return { isRepo: false };
}

function getRepoStars() {
  const starElement = document.querySelector('#repo-stars-counter-star');
  return starElement ? starElement.textContent.trim() : 'N/A';
}

function getRepoLanguage() {
  const langElement = document.querySelector('[data-ga-click*="language"]');
  return langElement ? langElement.textContent.trim() : 'N/A';
}

function createCodeLineDisplay() {
  const display = document.createElement('div');
  display.id = 'code-line-display';
  display.style.cssText = `
    position: fixed;
    top: 80px;
    left: 20px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 15px 20px;
    border-radius: 10px;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    font-size: 14px;
    font-weight: 500;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    z-index: 10000;
    opacity: 0;
    transform: translateX(-20px);
    transition: all 0.3s ease;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
  `;
  
  display.innerHTML = `
    <div style="display: flex; align-items: center; gap: 10px;">
      <div style="width: 8px; height: 8px; background: #4CAF50; border-radius: 50%; animation: pulse 2s infinite;"></div>
      <span id="line-count-text">正在统计代码行数...</span>
    </div>
  `;
  
  const style = document.createElement('style');
  style.textContent = `
    @keyframes pulse {
      0%, 100% { opacity: 1; }
      50% { opacity: 0.5; }
    }
  `;
  document.head.appendChild(style);
  
  document.body.appendChild(display);
  
  setTimeout(() => {
    display.style.opacity = '1';
    display.style.transform = 'translateX(0)';
  }, 100);
  
  return display;
}

async function fetchCodeLines(repoInfo) {
  try {
    const result = await chrome.storage.local.get(['serverUrl']);
    let serverUrl = result.serverUrl;
    
    if (!serverUrl) {
      return null;
    }
    
    // 确保URL格式正确
    if (!serverUrl.startsWith('http://') && !serverUrl.startsWith('https://')) {
      serverUrl = 'https://' + serverUrl;
    }
    
    const response = await fetch(serverUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        repoUrl: repoInfo.url,
        cloneUrl: repoInfo.cloneUrl,
        owner: repoInfo.owner,
        repo: repoInfo.repo,
        stars: repoInfo.stars,
        language: repoInfo.language
      })
    });
    
    if (response.ok) {
      const result = await response.json();
      return result.lines || null;
    }
  } catch (error) {
    console.error('获取代码行数失败:', error);
  }
  
  return null;
}

async function showCodeLineCount() {
  const repoInfo = extractRepoInfo();
  if (!repoInfo.isRepo) return;
  
  repoInfo.stars = getRepoStars();
  repoInfo.language = getRepoLanguage();
  
  const display = createCodeLineDisplay();
  const textElement = document.getElementById('line-count-text');
  
  const lines = await fetchCodeLines(repoInfo);
  
  if (lines) {
    textElement.textContent = `代码总行数: ${lines.toLocaleString()} 行`;
  } else {
    const result = await chrome.storage.local.get(['serverUrl']);
    if (!result.serverUrl) {
      textElement.textContent = '请先配置服务器地址';
    } else {
      textElement.textContent = '服务器连接失败';
    }
  }
  
  setTimeout(() => {
    display.style.opacity = '0';
    display.style.transform = 'translateX(-20px)';
    setTimeout(() => {
      display.remove();
    }, 300);
  }, 5000);
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'getRepoInfo') {
    const repoInfo = extractRepoInfo();
    
    if (repoInfo.isRepo) {
      repoInfo.stars = getRepoStars();
      repoInfo.language = getRepoLanguage();
    }
    
    sendResponse(repoInfo);
  }
});

const repoInfo = extractRepoInfo();
if (repoInfo.isRepo) {
  chrome.runtime.sendMessage({ 
    action: 'repoDetected', 
    repoInfo 
  });
  
  setTimeout(() => {
    showCodeLineCount();
  }, 1000);
}