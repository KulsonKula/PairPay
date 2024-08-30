import axios from "axios";

const apiClient = axios.create({
  baseURL: "http://127.0.0.1:5000",
});

export const get_recipe_id = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await apiClient.post("/upload", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return response.data;
  } catch (error) {
    console.error(
      "Error uploading file:",
      error.response ? error.response.data : error.message
    );
    throw error;
  }
};
