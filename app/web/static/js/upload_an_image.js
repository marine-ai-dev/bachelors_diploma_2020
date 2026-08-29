//UPLOAD AN IMAGE
var previewImage = function(event) {
	var preview = document.getElementById('my-image');
	preview.src = URL.createObjectURL(event.target.files[0]);
	preview.style.display = "block";
};
