import { useState } from "react";
import { Input, Card, CardBody, Button } from "@nextui-org/react";
import { EyeFilledIcon } from "./EyeFilledIcon";
import { EyeSlashFilledIcon } from "./EyeSlashFilledIcon";
import { Link } from "react-router-dom";

export default function Login() {
  const [isVisible, setIsVisible] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  const toggleVisibility = () => setIsVisible(!isVisible);

  const handleLogin = async () => {
    const response = await fetch("http://localhost:5000/api/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        mail: email,
        password: password,
      }),
    });

    const data = await response.json();

    if (response.ok) {
      localStorage.setItem("access_token", data.access_token);
      localStorage.setItem("refresh_token", data.refresh_token);
      alert("Zalogowano pomyślnie!");
    } else {
      setErrorMessage(data.message || "Login failed");
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gradient-to-b from-sky-900 to-slate-800">
      <Card className="w-full max-w-md shadow-lg ">
        <CardBody>
          <h2 className="text-left text-xl font-semibold mb-5">Zaloguj się</h2>

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
            onClick={handleLogin}
          >
            Zaloguj się
          </Button>

          <div className="text-left">
            <Link to="/register" className="text-xs" style={{ color: 'blue' }}>
              Stwórz konto
            </Link>
          </div>
        </CardBody>
      </Card>
    </div>
  );
}
