
function navigateTo(page) {
  switch (page) {
    case 'videos':
      window.location.href = '/videos';
      break;
    case 'about':
      window.location.href = '/about';
      break;
    case 'blogs':
      window.location.href = '/blogs';
      break;
    case 'consulting':
      window.location.href = '/consulting';
      break;
    case 'tools':
      window.location.href = '/tools';
      break;
    case 'contact':
      window.location.href = '/contact';
      break;
    case 'projects':
      window.location.href = '/projects';
      break;
    default:
      console.error('Invalid navigation target:', page);
  }
}

window.navigateTo = navigateTo;