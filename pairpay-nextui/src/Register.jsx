import { useState } from "react";
import { Input, Card, CardBody, Button } from "@nextui-org/react";
import { EyeFilledIcon } from "./EyeFilledIcon";
import { EyeSlashFilledIcon } from "./EyeSlashFilledIcon";
import { useNavigate  } from "react-router-dom";

export default function Register() {
  const [isVisible, setIsVisible] = useState(false);
  const [name, setName] = useState("");
  const [surname, setSurname] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  const toggleVisibility = () => setIsVisible(!isVisible);

  const navigate = useNavigate();
  const handleRegister = async () => {
    try {
      const response = await fetch("http://localhost:5000/api/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: name,
          surname: surname,
          mail: email,
          password: password,
        }),
      });
  
      const data = await response.json();
  
      if (response.ok) {
        localStorage.setItem("access_token", data.access_token);
        localStorage.setItem("refresh_token", data.refresh_token);
        alert("Utworzono konto!");
        navigate("/#"); 
      } else {
        setErrorMessage(data.message || "Rejestracja nie powiodła się");
      }
    } catch (error) {
      console.error("Błąd podczas rejestracji:", error);
      setErrorMessage("Wystąpił problem z połączeniem");
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gradient-to-b from-sky-900 to-slate-800">
      <Card className="w-full max-w-md shadow-lg">
        <CardBody>
          <h2 className="text-left text-xl font-semibold mb-5">Stwórz konto</h2>

          <Input
            type="name"
            label="Name"
            variant="bordered"
            placeholder="Enter your name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="max-w-xs mb-4"
          />

            <Input
            type="surname"
            label="Surname"
            variant="bordered"
            placeholder="Enter your surname"
            value={surname}
            onChange={(e) => setSurname(e.target.value)}
            className="max-w-xs mb-4"
          />

          <Input
            type="email"
            label="Email"
            variant="bordered"
            placeholder="Enter your email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="max-w-xs mb-4"
          />

          <Input
            label="Password"
            variant="bordered"
            placeholder="Enter your password"
            type={isVisible ? "text" : "password"}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            endContent={
              <button
                className="focus:outline-none"
                type="button"
                onClick={toggleVisibility}
                aria-label="toggle password visibility"
              >
                {isVisible ? (
                  <EyeSlashFilledIcon className="text-2xl text-default-400 pointer-events-none" />
                ) : (
                  <EyeFilledIcon className="text-2xl text-default-400 pointer-events-none" />
                )}
              </button>
            }
            className="max-w-xs mb-6"
          />

          {errorMessage && (
            <div className="text-red-500 text-xs mb-4">{errorMessage}</div>
          )}

          <Button
            color="primary"
            className="max-w-xs w-full font-semibold mb-5"
            onClick={handleRegister}>
            Zarejestruj się
          </Button>

        </CardBody>
      </Card>
    </div>
  );
}
