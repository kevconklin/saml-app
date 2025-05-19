export default function Home() {
  const login = () => {
    window.location.href = "http://localhost:8000/sso/login";  // FastAPI login redirect
  };

  return (
    <div>
      <h1>Welcome to the App</h1>
      <button onClick={login}>Login with SSO</button>
    </div>
  );
}
