// Replace with the URL to your deployed Cloud Function
var functionUrl = "https://your.cloudfunctions.net"

// This function will be called when the form is submitted
function onFormSubmit() {

  // The event is a FormResponse object:
  // https://developers.google.com/apps-script/reference/forms/form-response
  // https://developers.google.com/apps-script/guides/triggers/events#form-submit_1
  var formResponses = FormApp.getActiveForm().getResponses();
  console.log('formResponses length ==> ', formResponses.length);
  var formResponse = formResponses[formResponses.length-1];
  
  // Gets all ItemResponses contained in the form response
  // https://developers.google.com/apps-script/reference/forms/form-response#getItemResponses()
  var itemResponses = formResponse.getItemResponses();

  // Gets the actual response strings from the array of ItemResponses
  var responses = itemResponses.map(function getResponse(itemResponse) { return itemResponse.getResponse(); });
  console.log(JSON.stringify({'responses': responses }));

  // Post the payload as JSON to our Cloud Function  
  var options = {
                  'method' : 'post',
                  'contentType': 'application/json',
                  'payload' : JSON.stringify({'responses': responses })
                };
  
  console.log('json ===> ', options);
  
  var requestResponse = UrlFetchApp.fetch(functionUrl, options);
  console.log('responseHttp ===>', requestResponse.getContentText());
}
