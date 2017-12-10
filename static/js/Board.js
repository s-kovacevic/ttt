class Board {
  constructor(id, state) {
    this.state = state;
    this.board = $(id);
  }

  drawState() {
    for (let i=0; i < this.state.length; i++) {
      if (!Number.isInteger(this.state[i])) {
        this.board.find("#" + i + "-" + this.state[i]).toggle();
      }
    }
  }

}
