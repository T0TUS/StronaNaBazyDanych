document.getElementById('toggle-btn').addEventListener('click', function () {
    const sidePanel = document.querySelector('.side-panel');
    const mainContent = document.querySelector('.main-content');
  
    if (sidePanel.style.left === '-250px') {
      sidePanel.style.left = '0';
      mainContent.style.marginLeft = '250px';
    } else {
      sidePanel.style.left = '-250px';
      mainContent.style.marginLeft = '0';
    }
  });
  