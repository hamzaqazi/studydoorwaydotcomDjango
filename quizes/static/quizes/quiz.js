console.log("hello Quiz.js") 

const url = window.location.href
const quizBox = document.getElementById('quiz-box')

const scoreBox = document.getElementById('score-box')
const resultBox = document.getElementById('result-box')

$.ajax({
	type: 'GET',
	url: `${url}data`,
	success:function(response){
		const data = response.data
		data.forEach(el => {
			for (const [question,answers] of Object.entries(el)){
				quizBox.innerHTML += `
					<h5 class="card-title">
						<ul>
							<li>${question}</li>
						</ul>
					</h5>
					<hr>
				`
				answers.forEach(answer => {
					quizBox.innerHTML += `
						<div class="card-text m-2">
							<input type="radio" class="ans" id="${question}-${answer}" name="${question}" value="${answer}">
							<label for="${question}">${answer}</label>
						</div>
					`
				})
			}
		});
	},
	error:function(error){
		console.log(error)
	},
})

const quizForm = document.getElementById('quiz-form')
const csrf = document.getElementsByName('csrfmiddlewaretoken')


const sendData = () => {
	const elements = [...document.getElementsByClassName('ans')]	
	const data = {}
	data['csrfmiddlewaretoken'] = csrf[0].value
	elements.forEach(el=>{
		if (el.checked) {
			data[el.name] = el.value
		} else {
			if (!data[el.name]) {
				data[el.name] = null
			}
		}
	})

	$.ajax({
		type: 'POST',
		url: `${url}save/`,
		data: data,
		success: function(response){
			//console.log(response)
			const results = response.results
			console.log(results)
			quizForm.classList.add('not-visible')

			scoreBox.innerHTML = `${response.passed ? '<div class="alert alert-success" role="alert">Congratulations! ' : '<div class="alert alert-danger" role="alert">You have failed '} Your result is ${response.score.toFixed(2)} %</div>`

			results.forEach(res=>{
				const resDiv = document.createElement('div')
				for (const [question, resp] of Object.entries(res)){
					// console.log(question)
					// console.log(resp)
					// console.log('*****')
					resDiv.innerHTML += question
					const cls = ['container', 'p-3', 'text-light', 'h6']
					resDiv.classList.add(...cls)

					if (resp=='not answered'){
						resDiv.innerHTML += '- not answered'
						resDiv.classList.add('bg-danger')
					}
					else {
						const answer = resp['answered']
						const correct = resp['correct_answer']

						if (answer == correct) {
							resDiv.classList.add('bg-success')
							resDiv.innerHTML += ` <span class="float-right">Answered: ${answer}</span>` 
						}else {
							resDiv.classList.add('bg-danger')
							resDiv.innerHTML += `  | Answered: ${answer}`
							resDiv.innerHTML += ` <span class="float-right">Correct answer: ${correct}</span>`
						}
					}
				}
				resultBox.append(resDiv)
			})
		},
		error: function(error){
			console.log(error)
		},
	})
} 

quizForm.addEventListener('submit', e=>{
	e.preventDefault()

	sendData()
})