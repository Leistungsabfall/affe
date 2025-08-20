document.getElementById('current-year').textContent = new Date().getFullYear();

fetch('bin/version.txt')
  .then(response => {
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return response.text();
  })
  .then(data => {
    document.getElementById('version').textContent = data;
  })
  .catch(error => {
    console.log('Error reading file:', error);
  });
