var due_date_field = document.getElementById("due_date");
var current_date = new Date();
var iso_date_string = current_date.toISOString().substring(0, 10);
due_date_field.value = iso_date_string;