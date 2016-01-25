function Matrix (fillValue, gridWidth) {
    this.gridWidth = gridWidth;
    this.grid = createMatrix(fillValue, gridWidth);

    function createMatrix(fillValue, gridWidth) {
        var total_size = gridWidth * gridWidth;
        var grid = new Array(total_size);
        grid.fill(fillValue);
        return grid;
    }
}

Matrix.prototype = {
    setValue: function(i, j, value) {
        this.grid[j*this.gridWidth + i] = value;
    },

    getValue: function(i, j) {
        return this.grid[j*this.gridWidth + i];
    },

    print: function() {
        for (var i = 0; i < this.gridWidth; i++) {
            for (var j = 0; j < this.gridWidth; j++) {
                document.write(this.getValue(j, i) + ", ");
            }
            document.write("<br />");
        }
    },

    exportData: function() {
        var data = new Array();

        for (var i = 0; i < this.gridWidth; i++) {
            for (var j = 0; j < this.gridWidth; j++) {
                var value = this.getValue(j, i);
                data.push({col: i, row: j, score: value});
            }
        }

        return data;
    },

    normalise: function() {
        var total = this.grid.reduce(function (a, b) {
            return a + b;
        });
        if (total > 0) {
            for (var i = 0; i < this.grid.length; i++) {
                this.grid[i] /= total;
            }
        }
    }
}

Distribution.prototype = new Matrix(0.0, 0);
Distribution.prototype.constructor = Distribution;

function Distribution (shapeSize, gridWidth) {
    this.shapeSize = shapeSize-1;
    Matrix.call(this, 0.0, gridWidth);
}

Distribution.prototype.resetGrid = function(){
    this.grid.fill(0);
}

Distribution.prototype.computeProbabilityFromBoard = function(board) {
    this.resetGrid();
    this.computeHorizontal(board);
    this.computeVertical(board);
    this.normalise();
}

Distribution.prototype.computeHorizontal = function(board) {
    for (var col = 0; col < this.gridWidth; col++) {
        for (var row = 0; row < this.gridWidth; row++) {
            var cannotFit = false;
            for (var k = col; k <= col+this.shapeSize; k++) {
                // check if the block crosses an already tested space
                // and it is within the bounds of the grid
                if (board.getValue(k, row) || k >= this.gridWidth) {
                    cannotFit = true;
                    break;
                }
            }

            // the block has passed all checks, it can fit here.
            if(!cannotFit) {
                for (var k = col; k <= col+this.shapeSize; k++) {
                    var value = this.getValue(k, row);
                    this.setValue(k, row, value+1);
                }

            }
        }
    }
}

Distribution.prototype.computeVertical = function(board) {
    for (var col = 0; col < this.gridWidth; col++) {
        for (var row = 0; row < this.gridWidth; row++) {
            var cannotFit = false;
            for (var k = row; k <= row+this.shapeSize; k++) {
                // check if the block crosses an already tested space
                // and it is within the bounds of the grid
                if (board.getValue(col, k) || k >= this.gridWidth) {
                    cannotFit = true;
                    break;
                }
            }

            // the block has passed all checks, it can fit here.
            if(!cannotFit) {
                for (var k = row; k <= row+this.shapeSize; k++) {
                    var value = this.getValue(col, k);
                    this.setValue(col, k, value+1);
                }

            }
        }
    }
}

JointDistribution.prototype = new Distribution(0, [0]);
JointDistribution.prototype.constructor = JointDistribution;

function JointDistribution (shipSizes, gridWidth) {
    this.distributions = shipSizes.map(function(size) {
        return new Distribution(size, gridWidth);
    });
    Distribution.call(this, 0, gridWidth);
}

JointDistribution.prototype.computeDistribution = function(board) {
    // compute each individual distribution
    this.distributions.forEach(function (item) {
        item.computeProbabilityFromBoard(board);
    });

    // sum probability across between each distribution
    this.sumAcrossBoards();
    this.normalise();
}

JointDistribution.prototype.sumAcrossBoards = function() {
    var parent = this;
    for(var i = 0; i < this.grid.length; i++) {
        this.distributions.forEach(function(item) {
            parent.grid[i] += item.grid[i];
        })
    }
}

JointDistribution.prototype.findMax = function() {
    console.log(this.grid);
    var index = this.grid.indexOf(Math.max.apply(Math, this.grid));
    return index;
}


function BattleshipAI() {
    this.GRID_SIZE = 10;
    this.REACTION_SPEED = 1000;
    this.SHIP_SIZES = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1];
    this.jdist = new JointDistribution(this.SHIP_SIZES, this.GRID_SIZE);
    this.lastMove = [0, 0]
    this.currentShip = []
    this.lastMoveWasHit = false;
}

BattleshipAI.prototype.runAI = function() {
    if (this.gameIsInWaitMode()) {
        console.log("wait mode");
    } else {
        var lastMoveWasHit = this.checkIfCellHit(this.lastMove[0], this.lastMove[1]);
        if (lastMoveWasHit) {
            this.currentShip = [this.lastMove];
            this.searchForShip();
        } else {
            var currentMove = this.evaluateBoard();
            this.playSquare(currentMove[0], currentMove[1]);
            this.lastMove = currentMove;
        }
    }

    var _this = this;
    setTimeout(function() { _this.runAI(); }, this.REACTION_SPEED);
}


BattleshipAI.prototype.searchForShip = function() {
    if(this.currentShip.length > 0) {
        var currentNode = this.currentShip.pop();
        var i = currentNode[0];
        var j = currentNode[1];

        this.addNeighbours(i, j);
        var direction = this.currentShip.pop();
        if (direction !== undefined) {

            this.playSquare(direction[0], direction[1]);
            this.lastMove = direction;

            var _this = this;
            setTimeout(function() { _this.searchForShip(); }, this.REACTION_SPEED);
        } else {
            this.currentShip = [];
            this.runAI();
        }
    } else {
        this.currentShip = [];
        this.runAI();
    }
}

BattleshipAI.prototype.addNeighbours = function(i, j) {
    var _this = this;
    var emptyOrNotHit = function(i, j) {
        return i >= 0 && j >= 0 && i < this.GRID_SIZE && j < this.GRID_SIZE
            && (_this.checkIfCellEmpty(i, j) || !_this.checkIfCellHit(i, j));
    }

    if (emptyOrNotHit(i+1, j)) this.currentShip.push([i+1, j]);
    if (emptyOrNotHit(i-1, j)) this.currentShip.push([i-1, j]);
    if (emptyOrNotHit(i, j+1)) this.currentShip.push([i, j+1]);
    if (emptyOrNotHit(i, j-1)) this.currentShip.push([i, j-1]);
}

BattleshipAI.prototype.checkIfCellHit = function(i, j) {
    var table = this.getBattleFieldTable();
    var item = this.getBattleFieldCell(table, i, j);
    return item.classList[1] === "battlefield-cell__hit";
}

BattleshipAI.prototype.checkIfCellEmpty = function(i, j) {
    var table = this.getBattleFieldTable();
    var item = this.getBattleFieldCell(table, i, j);
    return item.classList[1] === "battlefield-cell__empty";
}

BattleshipAI.prototype.createBoardFromRows = function() {
    var board = new Matrix(false, 10);
    var table = this.getBattleFieldTable();
    for (var i = 0, row; row = table.rows[i]; i++) {
        for (var j = 0, item; item = row.cells[j]; j++) {
            var state = item.classList[1] !== "battlefield-cell__empty";
            board.setValue(j, i, state);
        }
    }
    return board;
}

BattleshipAI.prototype.evaluateBoard = function() {
    var board = this.createBoardFromRows();
    this.jdist.computeDistribution(board);
    var index = this.jdist.findMax();
    var i = index % this.GRID_SIZE;
    var j = Math.floor(index / this.GRID_SIZE);
    return [i, j];
}

BattleshipAI.prototype.playSquare = function(i, j) {
    var table = this.getBattleFieldTable();
    console.log("Playing square at location x: "+i+" y: " + j);
    var square = this.getBattleFieldCell(table, i, j).children[0];
    square.click();
}

BattleshipAI.prototype.gameIsInWaitMode = function() {
    var battlefield = this.getBattleField();
    return battlefield.className.indexOf("battlefield__wait") > -1
}

BattleshipAI.prototype.getBattleFieldCell = function(table, i, j) {
    return table.rows[j].cells[i];
}

BattleshipAI.prototype.getBattleField = function() {
    return document.getElementsByClassName("battlefield__rival")[0];
}

BattleshipAI.prototype.getBattleFieldTable = function() {
    var battlefield = this.getBattleField();
    return battlefield.childNodes[1].childNodes[1].childNodes[0];
}

BattleshipAI.prototype.randomInteger = function(lower, upper) {
    return Math.floor(Math.random() * upper) + lower
}
