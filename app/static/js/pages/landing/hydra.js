// ---------- HYDRA ----------
const hydraCanvas = document.getElementById("hydraCanvas");
// Make canvas fill the screen at device resolution
hydraCanvas.width = window.innerWidth * window.devicePixelRatio;
hydraCanvas.height = window.innerHeight * window.devicePixelRatio;
hydraCanvas.style.width = "100%";
hydraCanvas.style.height = "100%";

const hydra = new Hydra({ 
    canvas: hydraCanvas, 
    detectAudio: false, 
    width: hydraCanvas.width,
    height: hydraCanvas.height,
});


function hydraWave() {
    // licensed with CC BY-NC-SA 4.0 https://creativecommons.org/licenses/by-nc-sa/4.0/
    //filet mignon
    // AFALFL
    // instagram/a_f_alfl 
    osc(100,-0.0018,0.17).diff(osc(20,0.00008).rotate(Math.PI/0.00003))
        .modulateScale(noise(1.5,0.18).modulateScale(osc(13).rotate(()=>Math.sin(time/22))),3)
        .color(11,0.5,0.4, 0.9, 0.2, 0.011, 5, 22,  0.5, -1).contrast(1.4)
        .add(src(o0).modulate(o0,.04),.6, .9)
        //.pixelate(0.4, 0.2, 0.1)
        .invert().brightness(0.0003, 2).contrast( 0.5, 2, 0.1, 2).color(4, -2, 0.1)
        .modulateScale(osc(2),-0.2, 2, 1, 0.3)
        .posterize(200) .rotate(1, 0.2, 0.01, 0.001)
        .color(22, -2, 0.5, 0.5, 0.0001,  0.1, 0.2, 8).contrast(0.18, 0.3, 0.1, 0.2, 0.03, 1) . brightness(0.0001, -1, 10)
            .out()
}

function hydraVoronoi() {
    // licensed with CC BY-NC-SA 4.0 https://creativecommons.org/licenses/by-nc-sa/4.0/
    //tropical juice
    //by Ritchse
    //instagram.com/ritchse
    voronoi(2,0.3,0.2).shift(0.5)
    .modulatePixelate(voronoi(4,0.2),32,2)
    .scale(()=>1+(Math.sin(time*2.5)*0.05))
    .diff(voronoi(3).shift(0.6))
    .diff(osc(2,0.15,1.1).rotate())
    .brightness(0.1).contrast(1.2).saturate(1.2)
        .out()
}

function hydraOjack() {
    // licensed with CC BY-NC-SA 4.0 https://creativecommons.org/licenses/by-nc-sa/4.0/
    // by Olivia Jack
    // https://ojack.github.io

    osc(4, 0.1, 0.8).color(1.04,0, -1.1).rotate(0.30, 0.1).pixelate(2, 20).modulate(noise(2.5), () => 1.5 * Math.sin(0.08 * time)).out(o0)
}

function hydraLines() {
    // licensed with CC BY-NC-SA 4.0 https://creativecommons.org/licenses/by-nc-sa/4.0/
    // ee_3 //LINES
    // e_e // @eerie_ear
    //
    //based on
    //@naoto_hieda
    //https://naotohieda.com/blog/hydra-book/
    //
    let n = 8
    let a = () => shape(4,0.25,0.009).rotate(()=>time/-40).repeat(n,n)
    a().add(a().scrollX(0.5/n).scrollY(0.5/n),1).modulate(o1,0.1).modulate(src(o1).color(10,10).add(solid(-14,-14)).rotate(()=>time/40),0.005).add(src(o1).scrollY(0.012,0.02),0.5).out(o1)
    src(o1).colorama(1.2).posterize(4).saturate(0.7).contrast(6).mult(solid(),0.15).out(o0)
}

function hydraRetro() {
    // licensed with CC BY-NC-SA 4.0 https://creativecommons.org/licenses/by-nc-sa/4.0/
    // by Zach Krall
    // http://zachkrall.online/
    
    osc(2, 0.9, 300)
    .color(0.9, 0.7, 0.8)
    .diff(
    osc(45, 0.3, 100)
    .color(0.9, 0.9, 0.9)
    .rotate(0.18)
    .pixelate(12)
    .kaleid()
    )
    .scrollX(10)
    .colorama()
    .luma()
    .repeatX(4)
    .repeatY(4)
    .modulate(
    osc(1, -0.9, 300)
    )
    .scale(2)

    .out()
}

function hydraLiquid() {
    // licensed with CC BY-NC-SA 4.0 https://creativecommons.org/licenses/by-nc-sa/4.0/
    // 3.0
    // by ΔNDR0M3DΔ
    // https://www.instagram.com/androm3_da/


    noise(3,0.3,3).thresh(0.3,0.03).diff(o3,0.3).out(o1)
    gradient([0.3,0.3,3]).diff(o0).blend(o1).out(o3)
    voronoi(33,3,30).rotate(3,0.3,0).modulateScale(o2,0.3).color(-3,3,0).brightness(3).out(o0)
    shape(30,0.3,1).invert(({time})=>Math.sin(time)*3).out(o2)
    render(o3)

}

function hydraKelid() {
    // licensed with CC BY-NC-SA 4.0 https://creativecommons.org/licenses/by-nc-sa/4.0/
    // "eye of the beholder"
    // Alexandre Rangel
    // www.alexandrerangel.art.br/hydra.html

    noise(6,.05)
    .mult( osc(9,0, ()=>Math.sin(time/1.5)+2 ) )
    .mult(
        noise(9,.03).brightness(1.2).contrast(2)
        .mult( osc(9,0, ()=>Math.sin(time/3)+13 ) )
    )
    .diff(
        noise(15,.04).brightness(.2).contrast(1.3)
        .mult( osc(9,0, ()=>Math.sin(time/5)+13 ) )
        .rotate( ()=>time/33 )
    )
    .scale( ()=>Math.sin(time/6.2)*.12+.15 )
    .modulateScale(
        osc(3,0,0).mult( osc(3,0,0).rotate(3.14/2) )
        .rotate( ()=>time/25 ).scale(.39).scale(1,.6,1).invert()
        , ()=>Math.sin(time/5.3)*1.5+3  )
    .rotate( ()=>time/22 )
    .mult( shape(100,.9,.01).scale(2.4,.6,1) )
    .out()
}

function hydraGreenZone() {
    // licensed with CC BY-NC-SA 4.0 https://creativecommons.org/licenses/by-nc-sa/4.0/
    //Flor de Fuego

    shape(200,0.5,1.5)
    .scale(0.5,0.5)
    .color([.1,0.1].smooth(1),0.3,0)
    .repeat(2,2)
    .modulateScale(osc(3,0.5),-0.6)
    .add(o0,0.5)
    .scale(0.9)
    .out()
}

function hydraLavaLamp() {
    // licensed with CC BY-NC-SA 4.0 https://creativecommons.org/licenses/by-nc-sa/4.0/
    // by Débora Falleiros Gonzales
    // https://www.gonzalesdebora.com/
    speed = 0.1
    osc(1).add(noise(5, 2)).color(0, 0, 3).colorama(0.4).out()
}


const hydraFuncs = [
    hydraWave, 
    hydraVoronoi, 
    hydraOjack, 
    hydraLines, 
    hydraRetro, 
    hydraLiquid, 
    hydraGreenZone, 
    hydraLavaLamp
];
const randomIndex = Math.floor(Math.random() * hydraFuncs.length);

// Get the random element
const randomHydra = hydraFuncs[randomIndex];
randomHydra();