import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";
import {
  getAuth,
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  signInWithPopup,
  GoogleAuthProvider,
} from "https://www.gstatic.com/firebasejs/10.12.2/firebase-auth.js";

const firebaseConfig = {
  apiKey: "AIzaSyA9sbJT_mRnJ0L2nc2Z1fQWt04jAXcJ4ZE",
  authDomain: "taskflow-e11d4.firebaseapp.com",
  projectId: "taskflow-e11d4",
  storageBucket: "taskflow-e11d4.firebasestorage.app",
  messagingSenderId: "974663804319",
  appId: "1:974663804319:web:e324df352bb212d04bc9aa",
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

const form = document.getElementById("auth-form");
const errorBox = document.getElementById("error");
const googleBtn = document.getElementById("google-btn");
const mode = form.dataset.mode;

function friendlyError(code) {
  const messages = {
    "auth/invalid-credential": "Wrong email or password.",
    "auth/invalid-email": "Please enter a valid email address.",
    "auth/email-already-in-use": "An account with this email already exists. Try logging in.",
    "auth/weak-password": "Password must be at least 6 characters.",
    "auth/too-many-requests": "Too many attempts. Please try again later.",
    "auth/popup-closed-by-user": "Google sign-in was cancelled.",
    "auth/unauthorized-domain": "This website address is not allowed in Firebase yet.",
    "auth/operation-not-allowed": "This sign-in method is not enabled in Firebase.",
    "auth/popup-blocked": "Your browser blocked the popup. Please allow popups for this site.",
    "auth/network-request-failed": "Network problem. Check your internet connection.",
  };
  return messages[code] || "Something went wrong (" + code + "). Please try again.";
}

async function finishLogin(userCredential) {
  const idToken = await userCredential.user.getIdToken();
  const response = await fetch("/session-login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ idToken }),
  });
  if (response.ok) {
    window.location.href = "/tasks";
  } else {
    errorBox.textContent = "Login failed on the server. Please try again.";
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  errorBox.textContent = "";
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value;
  try {
    const credential =
      mode === "signup"
        ? await createUserWithEmailAndPassword(auth, email, password)
        : await signInWithEmailAndPassword(auth, email, password);
    await finishLogin(credential);
  } catch (error) {
    console.error(error);
    errorBox.textContent = friendlyError(error.code);
  }
});

googleBtn.addEventListener("click", async () => {
  errorBox.textContent = "";
  try {
    const credential = await signInWithPopup(auth, new GoogleAuthProvider());
    await finishLogin(credential);
  } catch (error) {
    console.error(error);
    errorBox.textContent = friendlyError(error.code);
  }
});