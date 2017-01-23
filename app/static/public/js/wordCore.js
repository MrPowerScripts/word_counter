var wordCore = {
  settings: {
    // API endpoint strings
    epPrefix: '/api/',
    // API Endpoints
    epUrlSubmit: 'urls',
    epUrlData: 'urls/site',
    epUrlUpdated: 'urls/updated',
  },

  unixEpoch: function() {
    return Math.round(new Date().getTime()/1000.0)
  },

  wordProm: function(data) {
    endpoint =  window.location.protocol + "//" +
                window.location.host +
                wordCore.settings.epPrefix + data.endpoint
    return $.ajax({
      type: data.method,
      url: endpoint,
      data: JSON.stringify(data.payload),
      contentType: "application/json",
      dataType: 'json'
    });
  },

  submitUrl: function(url) {
    var request = {}
    request.endpoint = wordCore.settings.epUrlSubmit
    request.payload = {url: url}
    request.method = "POST"
    return wordCore.wordProm(request)
  },

  getSiteData: function(url) {
    var request = {}
    request.endpoint = wordCore.settings.epUrlData
    request.payload = {url: url}
    request.method = "POST"
    return wordCore.wordProm(request)
  },

  getRecentlyUpdated: function() {
    var request = {}
    request.endpoint = wordCore.settings.epUrlUpdated
    request.method = "GET"
    return wordCore.wordProm(request)
  },

  // Thanks stackoverflow
  scaleBetween: function(unscaledNum, minAllowed, maxAllowed, min, max) {
    return (maxAllowed - minAllowed) * (unscaledNum - min) / (max - min) + minAllowed;
  }

};
