title: Just a text input
published: true
description: "This is simply to have a text input - example use with grammarly... Note: nothing is saved anywhere... use clipboard."
date: 2018-03-28
tags: [tools]
template: page.html


<div class="row">
	<div class="col-sm-2"></div>
	<div class="col-sm-8">
		<div class="panel panel-default">
			<div class="panel-heading">
				<h3 class="panel-title">
				<button type="button" style="width:100%;" class="btn btn-primary" onclick="text_area_copy_to_clipboard()">Copy to clipboard</button>
				Enter your text below - remember to use the clipboard...
				</h3>
			</div>
			<div class="panel-body">
				<textarea class='autoExpand' style="width:100%;height:100%" rows='10' data-min-rows='10' placeholder='Your text here...' id="editarea"></textarea>
			</div>
			<div class="panel-footer">
			<button type="button" style="width:100%;" class="btn btn-primary" onclick="text_area_copy_to_clipboard()">Copy to clipboard</button>
			</div>
		</div>
		<div class="col-sm-2"></div>
	</div>
</div>

