let respostas = {
    agua:0,
    fogo:0,
    trovao:0,
    vento:0
}

let perguntaAtual = 0

let perguntas = [

{
    pergunta:"Which of these qualities best fits you?",
    opcoes:[
        {texto:"Calm and strategic", tipo:"agua"},
        {texto:"Brave and determined", tipo:"fogo"},
        {texto:"Fast and precise", tipo:"trovao"},
        {texto:"Aggressive and unpredictable", tipo:"vento"}
    ]
},

{
    pergunta:"In a fight, you prefer:",
    opcoes:[
        {texto:"Analyze before acting", tipo:"agua"},
        {texto:"Attack head-on", tipo:"fogo"},
        {texto:"Wait for the perfect moment", tipo:"trovao"},
        {texto:"Attack from multiple angles", tipo:"vento"}
    ]
},

{
    pergunta:"Which element do you find coolest?",
    opcoes:[
        {texto:"Water", tipo:"agua"},
        {texto:"Fire", tipo:"fogo"},
        {texto:"Thunder", tipo:"trovao"},
        {texto:"Wind", tipo:"vento"}
    ]
},

{
    pergunta:"Which of these slayers do you like most?",
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
        texto="Your breathing style is: Water Breathing"
        img="/static/img/descubra/respAguaa.webp"
    }

    if(maior=="fogo"){
        texto="Your breathing style is: Flame Breathing"
        img="/static/img/descubra/respFogo.jpg"
    }

    if(maior=="trovao"){
        texto="Your breathing style is: Thunder Breathing"
        img="/static/img/descubra/respTrovao.webp"
    }

    if(maior=="vento"){
        texto="Your breathing style is: Wind Breathing"
        img="/static/img/descubra/respVento.jpg"
    }

    document.getElementById("respiracaoFinal").innerText = texto
    document.getElementById("imagemRespiracao").src = img

    const nomeRespiracao = texto.replace("Your breathing style is: ", "");
    
    fetch('/descubra/salvar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ respiracao: nomeRespiracao }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log("Result saved to profile!");
        }
    })
    .catch(error => console.error('Error sending result:', error));
}