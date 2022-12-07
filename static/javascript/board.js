var chessboard = document.getElementById('chessboard');
for (var i = 0; i < 17; i++) {
   for (var j = 0; j < 17; j++) {
      var chessSquare = document.createElement('div');
      chessSquare.className = 'chess-square';
      if ((i+j)%2==0){
         chessSquare.style.backgroundColor = '#000';
      }
      chessboard.appendChild(chessSquare);
   }
}