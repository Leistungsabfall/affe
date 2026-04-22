document.getElementById('current-year').textContent = String(new Date().getFullYear());

function copyToClipboard(button) {
  if (button.disabled) {
    return;
  }

  button.disabled = true;
  const codeBlock = button.parentElement.querySelector('pre.code');
  const text = codeBlock.textContent;
  navigator.clipboard.writeText(text).then(() => {
    const originalContent = button.innerHTML;
    button.innerHTML = '<span class="copy-checkmark" aria-hidden="true">✓</span>';

    // Show tooltip
    let tooltip = button.querySelector('.copy-tooltip');
    if (!tooltip) {
      tooltip = document.createElement('span');
      tooltip.className = 'copy-tooltip';
      tooltip.textContent = 'Copied to clipboard';
      button.appendChild(tooltip);
    }
    tooltip.classList.add('show');

    setTimeout(() => {
      button.innerHTML = originalContent;
      button.disabled = false;
    }, 2000);
  }).catch(err => {
    console.error('Failed to copy:', err);
    button.disabled = false;
  });
}

async function showLatestVersion() {
  const versionElement = document.getElementById('version');
  const versionRegex = /^[0-9]+\.[0-9]+\.[0-9]+$/;

  try {
    let version = null;
    try {
      const response = await fetch('https://data.jsdelivr.com/v1/packages/gh/Leistungsabfall/affe/resolved?specifier=latest');
      if (!response.ok) {
        throw new Error(`jsdelivr returned ${response.status}`);
      }
      const release = await response.json();
      if (versionRegex.test(release.version)) {
        version = release.version;
      }
    } catch {
      console.error('Failed to fetch latest version from jsdelivr, falling back to GitHub API');
    }

    if (version) {
      versionElement.textContent = version;
      return;
    }

    const response = await fetch('https://api.github.com/repos/Leistungsabfall/affe/releases/latest', {
      headers: {
        Accept: 'application/vnd.github+json',
      },
    });

    if (!response.ok) {
      throw new Error(`GitHub API returned ${response.status}`);
    }

    const release = await response.json();
    version = (release.tag_name || '').trim();
    if (!version) {
      throw new Error('Missing tag_name in GitHub API response');
    }

    versionElement.textContent = version;
  } catch (err) {
    console.error('Failed to fetch latest version:', err);
    versionElement.classList.add('text-danger');
    versionElement.innerHTML = '<b>Error:</b> Could not fetch latest version due to<br>GitHub API rate limits, try again later.';
  }
}

showLatestVersion()
