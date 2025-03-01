

  fetch('http://localhost:8000/health/', { // not sure if this should be the docs or the health url
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'SHA256:gJAz8nq64XDgCicEqbx1ohBLHGGO6o28ehdKsUXc3jo' // api key? idk if it even needs one
    },
    credentials: 'include'
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response error');
    }
    return response.json();
  })
  .then(data => {
    console.log(data);
  })
  .catch(error => {
    console.error('Fetch error:', error);
  });

