let buttonRegister= document.getElementById('bt_register');
let divRegister = document.getElementById('registration');
let signUp = document.getElementById('registration_button');
let btnLogin= document.getElementById('bt_login');
let btnSignIn= document.getElementById('sign_in');

buttonRegister.onclick = () => {
    divRegister.style.display = "flex";
};

signUp.onclick = () => {
    divRegister.style.display = "none";
};

btnLogin.onclick = () => {
    btnSignIn.style.display = "flex";
};





