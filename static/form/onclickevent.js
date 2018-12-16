// let charactorgrapharray = {};
let cellName = ["charanameInp", "select", "addBtn", "delBtn"]
let is_redrawed = false

//appendRow: 登場人物の名前と役割を入力するテーブルに新しく行を追加
function appendRow() {

	let tbl = document.getElementById("tbl");
	if (!tbl) return;

	const rownum = tbl.rows.length;
	const newrow = tbl.insertRow(rownum);

	//append columns
	const chara_name = newrow.insertCell(0);
	chara_name.innerHTML = '<label> <input class="charanameInp" type="text" id="txt1" name="txt1" size="30"></input> </label>';

	const roleSelector = newrow.insertCell(1);
	roleSelector.innerHTML = '<select class="select" id="select1" name="select1"> <option>主人公</option> <option>協力者</option> <option>依頼者</option> <option>犠牲者</option> <option>狂言回し</option> <option>敵</option> <option>ライバル</option> <option>支援者</option> </select>';

	const edtBtn = newrow.insertCell(2);
	edtBtn.innerHTML = '<input class="addBtn" type="button" id="addBtn1" name="addBtn1" value="追加" onclick="appendRow(this)"></input>';

	const delBtn = newrow.insertCell(3);
	delBtn.innerHTML = '<input class="delBtn" type="button" id="delBtn1" name="delBtn1" value="削除" onclick="deleteRow(this)"></input>';

	//set focus into the recent appended input
	const addedInput = document.getElementById("txt" + rownum);
	if (addedInput)
		addedInput.focus();

}

// deleteRow: 削除ボタン該当行を削除
function deleteRow(delbtn) {

	if (!delbtn) return;

	const delrow = delbtn.parentNode.parentNode;
	const wholeTBL = delrow.parentNode;

	if (wholeTBL) wholeTBL.deleteRow(delrow.sectionRowIndex);

	// reidentify
	let tbl = document.getElementById("tbl");
	for (let i = 0; i < tbl.rows.length; i++) {
		for (let j = 0; j < tbl.rows[1].cells.length; j++) {
			let cell = tbl.rows[i].cells[j];
			let cellclass = cell.className;
			if (cellclass !== "table_hedding1" || cellclass !== "table_hedding2"){
				let cell = tbl.rows[i].cells[j].firstElementChild;
				let cellclass = cell.className;
				cell.setAttribute("id", cellName[i] + i);
				cell.setAttribute("name", cellName[i] + i);
			}
		}
	}

}

$(function() {
    $(".loading").addClass("is-hide");
});

$(function(){

	let charanamear = [];
	let yakushoku = [];
	const tbl = document.getElementById("tbl");
	const charanum = tbl.rows.length - 1;
	for (let i=0; i<charanum; i++){
		charanamear.push(document.getElementById('txt' + (i+1)).value);
		yakushoku.push(document.getElementById('select' + (i+1)).value);
	}

	// Ajax button click
  $('#analyze').on('click',function(){
		$.ajax({
			url:$('form#analyze').attr('action'),
      type:'POST',
			dataType: 'json',
			beforeSend:function(){
				// $loading.removeClass("is-hide");
			},
      data:{
				scenario: $('#comment').val(),
				'charanamear[]': charanamear,
				'yakushoku[]': yakushoku,
			},
			traditional: true,
		})
		// Ajax request succeeded
		.done((data) => {
			console.log(response.scenario);
			// $loading.addClass("is-hide");
			// $('#divdiv').show();
			// $('#graphtitle').val(response['title']);
			// $('#graphtitle').show();
			// $('#graph-area').show();
			//
			// const scene = Object.keys(response['graph_scene[]']).map(function (key) {return response['graph_scene[]'][key]});
			// const data = Object.keys(response['charaemotion_graph[]']).map(function (key) {return response['charaemotion_graph[]'][key]});
			// const charactors = Object.keys(response['chara[]']).map(function (key) {return response['chara[]'][key]});
			// const gender = Object.keys(response['seibetu[]']).map(function (key) {return response['seibetu[]'][key]});
			// // const words = Object.keys(response['words[]']).map(function (key) {return response['words[]'][key]});
			// const time = response['time'];
			//
			// console.log("scene=");
			// console.log(scene);
			// console.log("data=");
			// console.log(data);
			// console.log("charactors=");
			// console.log(charactors);
			// console.log("seibetu=");
			// console.log(gender);
			// // console.log("words=");
			// // console.log(words);
			// console.log("times=");
			// console.log(time);
			//
			// let str = document.createTextNode(time);
			// if(!is_redrawed){
			// 		timelabel = document.createElement("p");
			// 		timelabel.id = "timelabel";
			// 		timelabel.appendChild(str);
			// 		document.body.appendChild(timelabel);
			// }else{
			// 		const textlabel = document.getElementById("timelabel");
			// 		textlabel.appendChild(str)
			// }

			//TODO: draw graph
		})
    // Ajax request failed
		.fail((error) => {
      console.log(error);
		})
    .always((data) => {
		});
	});

});
