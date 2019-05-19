function appendRow(appendBtn) {

	if(appendBtn.value === "append"){
		let tbl = document.getElementById("tbl");
		if (!tbl) return;

		const rownum = tbl.rows.length;
		const newrow = tbl.insertRow(rownum);

		//append columns
		const chara_name = newrow.insertCell(0);
		chara_name.innerHTML = '{{form1.characterName}}';

		const roleSelector = newrow.insertCell(1);
		roleSelector.innerHTML = '{% spaceless %}{{form1.characterRole}}{% endspaceless %}';

		const addBtn = newrow.insertCell(2);
		addBtn.innerHTML = '<input class="appendBtn" type="button" value="append" onclick="appendRow(this)" id="appendBtn' + rownum +'" name="appendBtn' + rownum +'">';

		//set focus into the recent appended input
		const addedInput = document.getElementById("name" + rownum);
		if (addedInput)
			addedInput.focus();

		appendBtn.value = "delete";
	}
	else{
		deleteRow(appendBtn)
		appendBtn.value = "append";
	}

}

function deleteRow(delbtn){

	if (!delbtn) return;

	let tbl = document.getElementById("tbl");

	const delrow = delbtn.parentNode.parentNode;
	tbl.deleteRow(delrow.sectionRowIndex);

	// reidentify
	for (let i = 1; i < tbl.rows.length; i++) {
		for (let j = 0; j < tbl.rows[1].cells.length; j++) {
			let cell = tbl.rows[i].cells[j].firstElementChild;
			let cellclass = cell.className;
			cell.setAttribute("id", cellclass + i);
			cell.setAttribute("name", cellclass + i);
		}
	}

}
