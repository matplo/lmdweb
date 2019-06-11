$('#newPageModal').on('hidden.bs.modal', function () {
 location.reload();
})

function save_to_file() {
	// $.post('/submit_edit/test-data')};
	var copyText = document.getElementById("editor").value;
	var fname = document.getElementById("editLabel").innerText;
	var data = { path : fname, edit : copyText, new : "no"};
	console.log(data);
	$.post("/submitedit", {
	  doc: JSON.stringify(data)
	});
};

function newPage() {
	var x = document.getElementById("newfname").value;
	var copyText = "title: " + x + "\ndescription: a collection of interesting things...\nusers: mp\npublished: someday\ntemplate: page.html\ntags: [general]";
	var fname = x;
	var data = { path : fname, edit : copyText, new : "yes"};
	console.log(data);
	$.post("/submitedit", {
		doc: JSON.stringify(data)
	});
};
