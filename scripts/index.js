
// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.11.0/firebase-app.js";
import { getAuth, createUserWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/10.11.0/firebase-auth.js";

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
apiKey: "AIzaSyBxvWNK6GIpEsSZj3oxnkwSkPLIBwkdjVc",
authDomain: "solar-clone.firebaseapp.com",
projectId: "solar-clone",
storageBucket: "solar-clone.appspot.com",
messagingSenderId: "320016531095",
appId: "1:320016531095:web:63333aba43cdd238f7f3d2"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);


// grab button
const submit = document.getElementById("submit-btn")

//send data to firebase
submit.addEventListener("click", function(event){
	//grab inputs
	const email = document.getElementById("email").value;
	const password = document.getElementById("password").value;
	event.preventDefault()
	createUserWithEmailAndPassword(auth, email, password)
		.then((userCredential) => {
    // Signed up 
    const user = userCredential.user;
	window.location.href = "index.html"
    // ...
  })
  .catch((error) => {
    const errorCode = error.code;
    const errorMessage = error.message;
    // ..
  });
})