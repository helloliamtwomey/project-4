// Wait for the document to load before running any JavaScript
$(document).ready(function() {

  // Handle form submission
  $("#questionnaire-form").submit(function(event) {
    // Prevent the default form submission behavior
    event.preventDefault();

    // Serialize the form data into an object
    var formData = $(this).serializeObject();

    // Send a POST request to the server with the form data
    $.post("/predict", formData, function(data) {
      // Display the result in a popup
      alert(data);
    });
  });

});