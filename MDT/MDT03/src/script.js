class UI {
  constructor(uiId, cvs, ctx) {
    this.uiId = uiId;
    this.cvs = cvs;
    this.ctx = ctx;

    this.ui = document.getElementById(this.uiId)
  }
}

class ClearButton extends UI {
  constructor(uiId, cvs, ctx, clearButtonId) {
    super(uiId, cvs, ctx);
    this.clearButtonId = clearButtonId;
    this.clearButton = document.getElementById(this.clearButtonId);

    this.clearButton.addEventListener("mousedown", this.clearCanvas);
  }

  clearCanvas = () => {
    this.ctx.clearRect(0, 0, this.cvs.width, this.cvs.height);
    console.log("cleared canvas");
  };
}

class Tool {
  constructor(cvs, ctx) {
    this.cvs = cvs;
    this.ctx = ctx;

    this.newPos = { x: 0, y: 0 };
    this.oldPos = { x: 0, y: 0 };
    this.isDrawing = false;
    this.isTouch = false;

    this.strokeStyle = "white";
    this.linewidth = 20;
    this.lineCap = "round";

    this.cvs.addEventListener("mousedown", this.mouseDown);
    this.cvs.addEventListener("touchstart", this.touchDown);


    this.cvs.addEventListener('mouseup', this.mouseUp);
    this.cvs.addEventListener('mouseout', this.mouseUp);
    this.cvs.addEventListener('touchend', this.touchUp);
    this.cvs.addEventListener('touchcancel', this.touchUp);

    this.cvs.addEventListener('mousemove', this.mouseMove);
    this.cvs.addEventListener('touchmove', this.touchMove);
    this.cvs.addEventListener('mousemove', this.draw);
    this.cvs.addEventListener('touchmove', this.draw);
  }

  mouseDown = (event) => {
    console.log(this.newPos);
    this.isDrawing = true;
    console.log("starting drawing");
  };

  mouseUp = (event) => {
    this.isDrawing = false;
    console.log("stopped drawing");
  };

  mouseMove = (event) => {
    const rect = this.cvs.getBoundingClientRect();
    this.oldPos = this.newPos;

    this.newPos = {
      x: event.clientX - rect.left,
      y: event.clientY - rect.top,
    }
  };

  touchDown = (event) => {
    if (this.isTouch === false) {
      this.touchMove(event);
      this.isTouch = true;
    }
    console.log(this.newPos);
    this.isDrawing = true;
    console.log("starting drawing");
  };

  touchUp = (event) => {
    this.isDrawing = false;
    this.isTouch = false;
    console.log("stopped drawing");
  };

  touchMove = (event) => {
    const rect = this.cvs.getBoundingClientRect();
    this.oldPos = this.newPos;

    this.newPos = {
      x: event.touches[0].clientX - rect.left,
      y: event.touches[0].clientY - rect.top,
    }
  };

  draw = (event) => {
    if (this.isDrawing === true) {
      this.ctx.beginPath();

      this.ctx.strokeStyle = this.strokeStyle;
      this.ctx.lineWidth = this.linewidth;
      this.ctx.lineCap = this.lineCap;

      this.ctx.moveTo(this.oldPos.x, this.oldPos.y);
      this.ctx.lineTo(this.newPos.x, this.newPos.y);

      this.ctx.stroke();
      this.ctx.closePath();
    }
  };
}

class CVS {
  constructor(canvasId, uiId, clearButtonId) {
    this.id = canvasId;
    this.uiId = uiId;

    this.cvs = document.getElementById(this.id);
    this.ctx = this.cvs.getContext("2d");

    this.cvsHeight = this.cvs.height;
    this.cvsWidth = this.cvs.width;

    this.clearButton = new ClearButton(this.uiId, this.cvs, this.ctx, clearButtonId);
    this.tool = new Tool(this.cvs, this.ctx);

    this.canvasResize();
    window.addEventListener("resize", this.canvasResize);
    this.cvs.addEventListener('touchstart', this.preventScroll);
  }

  canvasResize = () => {
    this.cvs.height = this.cvsHeight = window.innerHeight;
    this.cvs.width = this.cvsWidth = window.innerWidth;
  };

  preventScroll = (event) => {
    event.preventDefault();
  };
}

const cvs = new CVS("cvs", "ui", "clearButton");
