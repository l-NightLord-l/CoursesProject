//menu
let mainMenuTriger = document.querySelector('.hamburger')
let mainMenuContainer = document.querySelector('.main-menu-container')

mainMenuTriger.addEventListener('change', function(){
	mainMenuContainer.classList.toggle('main-menu-opened')
})



//pages
let instagram = document.querySelector(".Instagram")
instagram.addEventListener('change', function(){
	let instagramInput = document.querySelector('#Instagram')
	let instagramImg = document.querySelector('#instagramImg')
	if(instagramInput.checked){
		instagramImg.src = '../static/img/icons/instagram_Active.png'
		window.open('https://www.instagram.com','_blank')
	}
	else{
		instagramImg.src = '../static/img/icons/instagram.png'
	}
})

let facebook = document.querySelector(".Facebook")
facebook.addEventListener('change', function(){
	let facebookInput = document.querySelector('#Facebook')
	let facebookImg = document.querySelector('#facebookImg')
	if(facebookInput.checked){
		facebookImg.src = '../static/img/icons/facebook_Active.png'
		window.open('https://www.facebook.com','_blank')
	}
	else{
		facebookImg.src = '../static/img/icons/facebook.png'
	}
})

let twitter = document.querySelector(".Twitter")
twitter.addEventListener('change', function(){
	let twitterInput = document.querySelector('#Twitter')
	let twitterImg = document.querySelector('#twitterImg')
	if(twitterInput.checked){
		twitterImg.src = '../static/img/icons/twitter_Active.png'
		window.open('https://www.twitter.com','_blank')
	}
	else{
		twitterImg.src = '../static/img/icons/twitter.png'
	}
})

function getData(){
	let xhr = new XMLHttpRequest()
	xhr.open("GET", "/api/get/data")
	xhr.responseType = "json"
	xhr.send()
	xhr.onload = function(){
		data = xhr.response
		console.log(data[0].user)
	}
}
getData()
