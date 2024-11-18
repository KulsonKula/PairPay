import React, { useState } from "react";
import axios from "axios";
import "../styles/Forms.css"; 

export default function Register() {
  const [name, setName] = useState("");
  const [surname, setSurname] = useState("");
  const [mail, setMail] = useState("");
  const [password, setPassword] = useState("");

  const handleRegister = async () => {
    try {
      const response = await axios.post("http://127.0.0.1:5000/register", {
        mail,
        password,
      });
      console.log("Registration successful:", response.data);
    } catch (error) {
      console.error(
        "Error registering:",
        error.response ? error.response.data : error.message
      );
    }
  };

  return (
    <div className="page-container">
        <div className="form-container">
      <h1>Utwórz konto</h1>
      <input className="form-input"
        type="name"
        placeholder="Imię"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      <input className="form-input"
        type="surname"
        placeholder="Nazwisko"
        value={surname}
        onChange={(e) => setSurname(e.target.value)}
      />
      <input className="form-input"
        type="password"
        placeholder="Hasło"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
        <input className="form-input"
        type="mail"
        placeholder="Email"
        value={mail}
        onChange={(e) => setMail(e.target.value)}
      />
      <button 
      className="form-button"
      onClick={handleRegister}>Zarajestruj się
      </button>
      </div>
    </div>
  );
}
