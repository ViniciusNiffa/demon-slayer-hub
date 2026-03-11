let respostas = {
    agua:0,
    fogo:0,
    trovao:0,
    vento:0
}

let perguntaAtual = 0

let perguntas = [

{
    pergunta:"Qual dessas qualidades mais combina com você?",
    opcoes:[
        {texto:"Calmo e estratégico", tipo:"agua"},
        {texto:"Corajoso e determinado", tipo:"fogo"},
        {texto:"Rápido e preciso", tipo:"trovao"},
        {texto:"Agressivo e imprevisível", tipo:"vento"}
    ]
},

{
    pergunta:"Em uma luta você prefere:",
    opcoes:[
        {texto:"Analisar antes de agir", tipo:"agua"},
        {texto:"Atacar com tudo", tipo:"fogo"},
        {texto:"Esperar o momento perfeito", tipo:"trovao"},
        {texto:"Atacar de vários ângulos", tipo:"vento"}
    ]
},

{
    pergunta:"Qual elemento você acha mais legal?",
    opcoes:[
        {texto:"Água", tipo:"agua"},
        {texto:"Fogo", tipo:"fogo"},
        {texto:"Trovão", tipo:"trovao"},
        {texto:"Vento", tipo:"vento"}
    ]
},

{
    pergunta:"Qual desses Hashiras você mais gosta?",
    opcoes:[
        {texto:"Tomioka", tipo:"agua"},
        {texto:"Rengoku", tipo:"fogo"},
        {texto:"Zenitsu", tipo:"trovao"},
        {texto:"Sanemi", tipo:"vento"}
    ]
}

]

function iniciarQuiz(){

    document.getElementById("inicio").style.display="none"
    document.getElementById("perguntaBox").style.display="block"

    mostrarPergunta()
}

function mostrarPergunta(){

    let pergunta = perguntas[perguntaAtual]

    document.getElementById("pergunta").innerText = pergunta.pergunta

    let opcoesHTML = ""

    for(let i=0;i<pergunta.opcoes.length;i++){

        opcoesHTML +=
        `<button onclick="responder('${pergunta.opcoes[i].tipo}')">
        ${pergunta.opcoes[i].texto}
        </button>`

    }

    document.getElementById("opcoes").innerHTML = opcoesHTML
}

function responder(tipo){

    respostas[tipo]++

    perguntaAtual++

    if(perguntaAtual < perguntas.length){

        mostrarPergunta()

    }else{

        mostrarResultado()

    }
}

function mostrarResultado(){

    document.getElementById("perguntaBox").style.display="none"
    document.getElementById("resultado").style.display="block"

    let maior="agua"

    for(let r in respostas){

        if(respostas[r] > respostas[maior]){
            maior = r
        }

    }

    let texto=""
    let img=""

    if(maior=="agua"){
        texto="Sua respiração é: Respiração da Água"
        img="img/tomioka.png"
    }

    if(maior=="fogo"){
        texto="Sua respiração é: Respiração das Chamas"
        img="img/rengoku.png"
    }

    if(maior=="trovao"){
        texto="Sua respiração é: Respiração do Trovão"
        img="img/zenitsu.png"
    }

    if(maior=="vento"){
        texto="Sua respiração é: Respiração do Vento"
        img="img/sanemi.png"
    }

    document.getElementById("respiracaoFinal").innerText = texto
    document.getElementById("imagemRespiracao").src = img
}