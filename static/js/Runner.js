$(document).ready(function () {
  let state = [0, "x", 2, 3, "o", "o", 6, 7, "x"];

  let board = new Board("#game", state);
  board.drawState();
});