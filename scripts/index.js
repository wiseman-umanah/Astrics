
// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.11.0/firebase-app.js";
import { getDatabase, set, ref } from "https://www.gstatic.com/firebasejs/10.11.0/firebase-database.js";
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
const db = getDatabase();
const auth = getAuth(app);

// grab button
const submit = document.getElementById("submit-btn");
const email = document.getElementById("email");
const password = document.getElementById("password");
const firstname = document.getElementById("firstname");
const lastname = document.getElementById("lastname");
const MainForm = document.getElementById('submit-btn');

//send data to firebase
let RegisterUSer = event => {
	//grab inputs
	event.preventDefault();
	createUserWithEmailAndPassword(auth, email.value, password.value)
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
}

MainForm.addEventListener('click', RegisterUSer);