import { get_recipe_id } from "./api.jsx";
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/Main.css"

export default function Main() {
  const [file, setFile] = useState(null);
  const [recipeText, setRecipeText] = useState(null);

  const handleapi = async () => {
    console.log("test");
    if (file) {
      try {
        const data = await get_recipe_id(file);
        console.log(data);
        setRecipeText(data);
      } catch (error) {
        console.error("Error in handleapi:", error);
      }
    }
  };

  const handleFileChange = (event) => {
    console.log(event);
    setFile(event.target.files[0]);
  };

  const navigate = useNavigate();
  const goToLogin = () => {
    navigate("/login");
  };

  const goToRegister = () => {
    navigate("/register");
  };

  return (
    <div className="page-container" >

      <nav className="navbar">
        <button className="nav-button" onClick={goToLogin}>Zaloguj się</button>
        <button className="nav-button" onClick={goToRegister}>Zarejestruj się</button>
      </nav>

      <input
        className="form-input"
        type="file"
        id="file"
        accept="image/*"
        onChange={handleFileChange}
      />

      <button className="form-button"
      onClick={handleapi}>Zatwierdź</button>

      {recipeText && <div>{recipeText}</div>} {}

    </div>
  );
}
