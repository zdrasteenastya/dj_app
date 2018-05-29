function uploadFile(){
	document.getElementById('files-input-upload').click();

document.getElementById('files-input-upload').addEventListener('change', function() {
	document.getElementById('fake-file-input-name').value = this.value;
});
}