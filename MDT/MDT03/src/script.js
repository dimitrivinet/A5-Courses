class UI {
  constructor(uiId, cvs, ctx) {
    this.uiId = uiId;
    this.cvs = cvs;
    this.ctx = ctx;

    this.ui = document.getElementById(this.uiId)
  }
}

class ClearButton extends UI {
  constructor(uiId, cvs, ctx, sizeButtonId) {
    super(uiId, cvs, ctx);
    this.clearButtonId = sizeButtonId;
    this.clearButton = document.getElementById(this.clearButtonId);

    this.clearButton.addEventListener("mousedown", this.clearCanvas);
  }

  clearCanvas = () => {
    this.ctx.clearRect(0, 0, this.cvs.width, this.cvs.height);
  };
}

class ColorButton extends UI {
  constructor(uiId, cvs, ctx, colorPickerId) {
    super(uiId, cvs, ctx);
    this.colorPickerId = colorPickerId;

    this.colorPicker = document.getElementById(this.colorPickerId);

    this.colorPicker.addEventListener("input", this.changeColor);
  }

  changeColor = () => {
    this.ctx.strokeStyle = this.colorPicker.value;
  };
}

class SizeButton extends UI {
  constructor(uiId, cvs, ctx, sizeSliderId, sizeValueId) {
    super(uiId, cvs, ctx);
    this.sizeSliderId = sizeSliderId;
    this.sizeValueId = sizeValueId;

    this.sizeSlider = document.getElementById(this.sizeSliderId);
    this.sizeValue = document.getElementById(this.sizeValueId);


    this.sizeSlider.addEventListener("input", this.changeSize);
  }

  changeSize = () => {
    this.sizeValue.innerHTML = this.sizeSlider.value;
    this.ctx.lineWidth = this.sizeSlider.value;
  };
}

class Tool {
  constructor(cvs, ctx) {
    this.cvs = cvs;
    this.ctx = ctx;

    this.newPos = { x: 0, y: 0 };
    this.oldPos = { x: 0, y: 0 };
    this.isDrawing = false;
    this.isFirstTouch = true;

    this.defaultLineCap = "round";
    this.ctx.lineCap = this.defaultLineCap;

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
    this.isDrawing = true;
  };

  mouseUp = (event) => {
    this.isDrawing = false;
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
    if (this.isFirstTouch === true) {
      this.touchMove(event);
      this.isFirstTouch = false;
    }
    this.isDrawing = true;
  };

  touchUp = (event) => {
    this.isDrawing = false;
    this.isFirstTouch = true;
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

      this.ctx.lineCap = this.defaultLineCap;

      this.ctx.moveTo(this.oldPos.x, this.oldPos.y);
      this.ctx.lineTo(this.newPos.x, this.newPos.y);

      this.ctx.stroke();
      this.ctx.closePath();
    }
  };
}

class CVS {
  constructor(canvasId, uiId, clearButtonId, colorPickerId, sizeSliderId, sizeValueId) {
    this.id = canvasId;
    this.uiId = uiId;

    this.cvs = document.getElementById(this.id);
    this.ctx = this.cvs.getContext("2d");

    this.cvsHeight = this.cvs.height;
    this.cvsWidth = this.cvs.width;

    this.tool = new Tool(this.cvs, this.ctx);
    this.clearButton = new ClearButton(this.uiId, this.cvs, this.ctx, clearButtonId);
    this.colorButton = new ColorButton(this.uiId, this.cvs, this.ctx, colorPickerId);
    this.sizeButton = new SizeButton(this.uiId, this.cvs, this.ctx, sizeSliderId, sizeValueId);

    this.canvasResize();
    window.addEventListener("resize", this.canvasResize);
    this.cvs.addEventListener('touchstart', this.preventScroll);
  }

  canvasResize = () => {
    this.cvs.height = this.cvsHeight = window.innerHeight;
    this.cvs.width = this.cvsWidth = window.innerWidth;
    this.sizeButton.changeSize();
    this.colorButton.changeColor();
  };

  preventScroll = (event) => {
    event.preventDefault();
  };
}

class Menu {
  constructor(menuButtonId, menuItemsId) {
    this.menuButtonId = menuButtonId;
    this.menuItemsId = menuItemsId;
    this.menuButton = document.getElementById(this.menuButtonId);
    this.menuItems = document.getElementById(this.menuItemsId);

    this.menuButton.addEventListener("mousedown", this.toggleMenu);
  }

  toggleMenu = (event) => {
    let toHide = this.menuItems.querySelectorAll("*");
    for (let element of toHide) {
        element.hidden = !element.hidden;
    }
  }
}

const cvs = new CVS("cvs", "menuItems", "clearButton", "colorPicker", "sizeSlider", "sizeValue");

const menu = new Menu("menuButton", "menuItems");
menu.toggleMenu();
