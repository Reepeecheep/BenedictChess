$('document').ready(function(){

	var board = '';
	var promote_square = '';

	$('.modal').modal({
		dismissible: false, 
	});

	if (winner != 'None'){
		$("#whoplay").hide();
		$("#winner").show();
	}

	//var active_pice = '';

	// uscf wikipedia alpha",
	/*
	function clickGetPositionBtn() {
		console.log("Current position as an Object:");
		console.log(board.position());

		console.log("Current position as a FEN string:");
		console.log(board.fen());
	}
	*/

	function insert_into_database(data){
		var aux_winner = data.valid[3];
		$.ajax({
			url: '/match/insert_move/',
			data: {
				'match_id': id,
				'notation': data.move,
				'fen': board.fen(),
				'turn': turn,
				'piece': data.piece,
				'source': data.source,
				'castling': castling,
			},
			type: 'post',
			dataType: 'json',
			//async: false,
			success: function (data) {
				castling = data.castling;
			}
		});
		if (aux_winner == false){
			change_turn();
		}
		else{
			swal({
				icon: "success",
				title: "Congrats",
				text: "Congrats " + turn + " wins",
			}).then((value) => {
				location.reload();
			});
		}
	}

	function calculate_attack(source, target, promote, board_pos){
		var valid;
		$.ajax({
			url: '/match/calculate_attack/',
			data: {
				'source': source,
				'target': target,
				'piece': board_pos[source],
				'board_fen': ChessBoard.objToFen(board_pos),
				'promote': promote,
				'match_id': id
			},
			type: 'post',
			dataType: 'json',
			async: false,
			success: function (data) {
				if (data.valid[0] == false){
					valid = false
				}
				else{
					board.position(data.valid[2], false);
					valid = true;
					if (data.valid[1] == 'Promote'){
						promote_square = target + '_' + board_pos[source];
						$('#modal1').modal('open');
					}
					else{
						if ($("#last_move").length != 0){
							$("#last_move").html(data.move);
							$("#last_move").attr('id', null);
							//document.getElementById('last_move').remove();
						}
						else {
							$(".table-moves").append("<tr><td>"+data.move+"</td><td id='last_move'></td></tr>");
						}
						insert_into_database(data)
					}
				}
			}
		});
		return valid;
	}

	function change_turn(){
		if (turn === 'black'){
			turn = 'white';
		}
		else{
			turn = 'black';
		}

		//board.orientation(turn);
		$("#whoplay").html(turn + ' moves');
	}

	var onChange = function(oldPos, newPos) {
		/*
		console.log("Old position: " + ChessBoard.objToFen(oldPos));
		console.log("New position: " + ChessBoard.objToFen(newPos));
		console.log("--------------------");
		console.log(oldPos);
		console.log(newPos);
		*/
		// Change Orientation
	};

	var onDragStart = function(source, piece, position, orientation) {
		//if ((orientation === 'white' && piece.search(/^w/) === -1) || (orientation === 'black' && piece.search(/^b/) === -1)) {
		//	return false;
		//}
		if ((turn === 'white' && piece.search(/^w/) === -1) || (turn === 'black' && piece.search(/^b/) === -1) || winner != 'None'){
			return false;
		}
	};

	var onDrop = function(source, target) {
		var board_pos = board.position();
		var valid;
		if (board_pos.hasOwnProperty(target)){
			return 'snapback';
		}

		valid = calculate_attack(source, target, 0, board_pos);

		if (valid == false){
  			Materialize.toast("<span><i class='medium material-icons'>announcement</i>&nbsp;&nbsp;Ilegal Move!</span>", 3000, 'rounded red accent-1');
			return 'snapback';
		}
		else{
			Materialize.Toast.removeAll();
		}
	};

	$(".promote").on('click', function(){
		var data = promote_square.split("_");
		var pos = board.position();

		if (data[1].includes('w')){
			pos[data[0]] = 'w'+this.id.replace('Img','');
		}
		else{
			pos[data[0]] = 'b'+this.id.replace('Img','');
		}
		promote_square = '';
		board.position(pos);
		
		calculate_attack(data[0], data[0], 1, board.position());
	});
	/*
	function pieceTheme(piece) {
		// wikipedia theme for white pieces
		if (piece.search(/w/) !== -1) {
		return '/static/img/chesspieces/wikipedia/' + piece + '.png';
		}

		// alpha theme for black pieces
		return '/static/img/chesspieces/uscf/' + piece + '.png';
	}
	*/
	//orientation: 'black',
	
	// Probar Alfiles
	var alfiles = {a1: 'wB',d7: 'wB',h3: 'wB',a4: 'bK',b4: 'wK',a1: 'bB',a8: 'wB',c5: 'wB',g1: 'bB',f5: 'bB',e5: 'bB'};
	
	// Probar Coronación
	var coronar = {c7: 'wP',e2: 'bP',g7: 'wN',b8: 'bN'};
	
	// Probar Rocas
	var torres = {a8: 'wR',c8: 'wR',f8: 'wR',h6: 'wR',e2: 'bR',a1: 'bR',e3: 'bQ'};
	
	// Probar Reinas
	var reinas = {a8: 'wQ',f8: 'wQ',h6: 'wN',e2: 'bK',a8: 'bQ',a1: 'bB',d6: 'bP',e3: 'bQ'};
	
	// Probar Peones
	var peones = {'a1':'wP','c2':'wP','d2':'wP','e2':'wP','f4':'wP','g3':'wP','a7':'bP','c7':'bP','d7':'bP','e3':'bP','f5':'bP','g6':'bP'};
	
	// Probar Reyes
	var reyes = {a1: 'bK',a8: 'bK',a3: 'wK',a5: 'wK',b4: 'wP',d3: 'wP',d8: 'wK',e1: 'wB',e7: 'wK'};
	
	var cfg = {
		pieceTheme: "/static/img/chesspieces/"+piecetheme+"/{piece}.png",
		draggable: true,
		position: init_position,
		orientation: turn,
		onChange: onChange,
		onDragStart: onDragStart,
		onDrop: onDrop
	};

	if (boardtheme != 'default'){
		cfg.boardTheme = window[boardtheme];
	}

	board = ChessBoard('board', cfg);

	$(window).resize(board.resize);

	$('#flipOrientationBtn').on('click', board.flip); //board.orientation('black'|'white');
	/*
	$("#cambiartema").on('click', board.pieceTheme="/static/img/chesspieces/alpha/{piece}.png");
	
	$('#getPositionBtn').on('click', clickGetPositionBtn);

	$('#setRuyLopezBtn').on('click', function() {
		board.position('r1bqkbnr/pppp1ppp/2n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R');
	});
	
	$('#setRookCheckmateBtn').on('click', function() {
		board.position({
			a4: 'bK',
			c4: 'wK',
			a7: 'wR'
		});
	});

	$('#reiniciar').on('click', board.start);

	$('#borrar').on('click', board.clear);

	$('#move1Btn').on('click', function() {
		board.move('e2-e8');
	});
	*/
})