import { get_recipe_id } from "./api.jsx";
import React, { useState } from "react";

export default function Main_app() {
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

  return (
    <div>
      <input
        type="file"
        id="file"
        accept="image/*"
        onChange={handleFileChange}
      />
      <button type="button" name="login" onClick={handleapi}>
        Submit
      </button>
      {recipeText && <div>{recipeText}</div>} {/* Display the response data */}
    </div>
  );
}
