const getQuote = document.getElementById("get-quote");
priceArray = [];

getQuote.addEventListener("click", async (e) => {
	getData();
	// setInterval(() => {
	// 	getData()
	// 	console.log(priceArray);
	// }, 10000)
});

const sendData = (data) => {
	fetch("/api", {
		method: "POST",
		headers: { "content-Type": "application/json" },
		body: JSON.stringify(data)
	})
}


const getData = () => {
	fetch("https://binance43.p.rapidapi.com/klines?symbol=BTCUSDT&interval=4h&limit=10", {
	"method": "GET",
	"headers": {
		"x-rapidapi-host": "binance43.p.rapidapi.com",
		"x-rapidapi-key": "e796e5b386msh092aba973e5001ap1f4c3djsn150ad429e4a2"
	}
}).then(response => {
	return response.json();
}).then(data => {
	console.log(data);
})
.catch(err => {
	console.error(err);
});
}