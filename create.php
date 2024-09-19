<html>
<head></head>
<body>
    <script>
      let perlin = {
    rand_vect: function(){
        let theta = Math.random() * 2 * Math.PI;
        return {x: Math.cos(theta), y: Math.sin(theta)};
    },
    dot_prod_grid: function(x, y, vx, vy){
        let g_vect;
        let d_vect = {x: x - vx, y: y - vy};
        if (this.gradients[[vx,vy]]){
            g_vect = this.gradients[[vx,vy]];
        } else {
            g_vect = this.rand_vect();
            this.gradients[[vx, vy]] = g_vect;
        }
        return d_vect.x * g_vect.x + d_vect.y * g_vect.y;
    },
    smootherstep: function(x){
        return 6*x**5 - 15*x**4 + 10*x**3;
    },
    interp: function(x, a, b){
        return a + this.smootherstep(x) * (b-a);
    },
    seed: function(){
        this.gradients = {};
        this.memory = {};
    },
    get: function(x, y) {
        if (this.memory.hasOwnProperty([x,y]))
            return this.memory[[x,y]];
        let xf = Math.floor(x);
        let yf = Math.floor(y);
        //interpolate
        let tl = this.dot_prod_grid(x, y, Math.floor(x),   Math.floor(y));
        let tr = this.dot_prod_grid(x, y, Math.floor(x)+1, Math.floor(y));
        let bl = this.dot_prod_grid(x, y, Math.floor(x),   Math.floor(y)+1);
        let br = this.dot_prod_grid(x, y, Math.floor(x)+1, Math.floor(y)+1);
        let xt = this.interp(x-Math.floor(x), tl, tr);
        let xb = this.interp(x-Math.floor(x), bl, br);
        let v = this.interp(y-Math.floor(y), xt, xb);
        this.memory[[x,y]] = v;
        return v;
    }
}
function generatePerlin(x,y) {
perlin.seed();

const GRID_SIZE = 4;
const RESOLUTION = 16;
const COLOR_SCALE = 250;

let num_pixels = GRID_SIZE / RESOLUTION;
var grid = [];
for (let y = 0; y < GRID_SIZE; y += 1/(y*GRID_SIZE)){
    var buffer = [];
    for (let x = 0; x < GRID_SIZE; x += 1/(x*GRID_SIZE)){
        buffer.push(Math.floor((parseInt(perlin.get(x, y) * COLOR_SCALE)/135)))
    }
    grid.push(buffer)
}
return grid;
}</script></body></html>