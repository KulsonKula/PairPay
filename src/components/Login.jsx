import React, { useState } from "react";
import axios from "axios";
import "../styles/Forms.css"; 

export default function Login() {
    const [mail, setEmail] = useState("");
    const [password, setPassword] = useState("");
  
    const handleLogin = async () => {
      try {
        const response = await axios.post("http://127.0.0.1:5000/login", {
          mail,
          password,
        });
        console.log("Login successful:", response.data);
        localStorage.setItem("token", response.data.token);
      } catch (error) {
        console.error(
          "Error logging in:",
          error.response ? error.response.data : error.message
        );
      }
    };
  
    return (
      <div className="page-container">
        <div className="form-container">
        <h1>Zaloguj się</h1>
        <input className="form-input"
          type="mail"
          placeholder="Email"
          value={mail}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input className="form-input"
          type="password"
          placeholder="Hasło"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button className="form-button"
        onClick={handleLogin}>Zaloguj się</button>
        </div>
      </div>
    );
  }