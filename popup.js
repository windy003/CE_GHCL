document.addEventListener('DOMContentLoaded', async () => {
  const serverUrlInput = document.getElementById('server-url');
  const saveBtn = document.getElementById('save-btn');
  const statusDiv = document.getElementById('status');

  async function loadStoredServerUrl() {
    const result = await chrome.storage.local.get(['serverUrl']);
    if (result.serverUrl) {
      serverUrlInput.value = result.serverUrl;
    }
  }

  async function saveServerUrl() {
    const serverUrl = serverUrlInput.value.trim();
    
    if (!serverUrl) {
      showStatus('请输入服务器地址', 'error');
      return;
    }

    try {
      await chrome.storage.local.set({ serverUrl: serverUrl });
      showStatus('配置已保存', 'success');
    } catch (error) {
      showStatus('保存失败', 'error');
    }
  }

  function showStatus(message, type = 'info') {
    statusDiv.textContent = message;
    statusDiv.className = `status ${type}`;
    statusDiv.style.display = 'block';
    
    setTimeout(() => {
      statusDiv.style.display = 'none';
    }, 2000);
  }

  saveBtn.addEventListener('click', saveServerUrl);
  
  await loadStoredServerUrl();
});