$(document).ready(function() {

	var cfg = {
		position: 'start',
		showNotation: false,
		pieceTheme: "/static/img/chesspieces/wikipedia/{piece}.png",
	};
	var board = ChessBoard('example_board', cfg);

	$('select').material_select();

	$('.board_draw').on('change', function(){
		reload_board();
	});

	$('.player_select').on('change', function(){
		var another;
		if (this.id == 'id_black_id'){
			another = 'id_white_id';
		}
		else{
			another = 'id_black_id';
		}

		if (this.value == $("#"+another).val() && $("#"+another).val() != ''){
			$("#"+this.id).val('').material_select();
			swal({
				icon: "error",
				title: "Error",
				text: "Chosse a diferent player",
			});
		}
	});

	function reload_board(){
		board.destroy();

		cfg.pieceTheme = "/static/img/chesspieces/"+$("#id_piece_theme").val()+"/{piece}.png";
		if ($("#id_board_theme").val() != 'default'){
			cfg.boardTheme =window[$("#id_board_theme").val()];
		}

		board = ChessBoard('example_board', cfg);

		$(window).resize(board.resize);
	}

});